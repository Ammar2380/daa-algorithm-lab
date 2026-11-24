import itertools
import random
import pytest
from algorithms.dynamic_programming import matrix_chain_order, lcs
from core.step_tracker import StepTracker


def test_mcm_textbook_example():
    r = matrix_chain_order([30, 35, 15, 5, 10, 20, 25])
    assert r["min_cost"] == 15125
    assert r["parenthesization"] == "((A1 x (A2 x A3)) x ((A4 x A5) x A6))"


def test_mcm_small_cases():
    assert matrix_chain_order([10, 20])["min_cost"] == 0            # one matrix
    assert matrix_chain_order([10, 20, 30])["min_cost"] == 6000     # two matrices
    assert matrix_chain_order([10, 100, 5, 50])["min_cost"] == 7500


def _brute(d, i, j):
    if i == j:
        return 0
    return min(_brute(d, i, k) + _brute(d, k + 1, j) + d[i - 1] * d[k] * d[j] for k in range(i, j))


def test_mcm_matches_brute_force():
    rng = random.Random(3)
    for _ in range(30):
        d = [rng.randint(1, 20) for _ in range(rng.randint(2, 8))]
        assert matrix_chain_order(d)["min_cost"] == _brute(d, 1, len(d) - 1)


@pytest.mark.parametrize("bad", [[], [5], [3, 0, 2], [3, -1, 2], [1.5, 2, 3], "abc", None])
def test_mcm_invalid(bad):
    with pytest.raises(ValueError):
        matrix_chain_order(bad)


def test_lcs_known():
    r = lcs("ABCBDAB", "BDCABA")
    assert r["length"] == 4 and r["lcs"] in {"BCBA", "BDAB", "BCAB"}


def test_lcs_edge_cases():
    assert lcs("", "abc")["lcs"] == "" and lcs("abc", "")["length"] == 0
    assert lcs("", "")["length"] == 0
    assert lcs("a", "a")["lcs"] == "a"
    assert lcs("abc", "xyz")["length"] == 0
    assert lcs("abc", "abc")["lcs"] == "abc"
    assert lcs("aaaa", "aa")["lcs"] == "aa"


def _is_subsequence(s, t):
    it = iter(t)
    return all(ch in it for ch in s)


def _brute_lcs_len(x, y):
    best = 0
    for r in range(len(x) + 1):
        for combo in itertools.combinations(x, r):
            if _is_subsequence(combo, y):
                best = max(best, r)
    return best


def test_lcs_random_vs_brute_force():
    rng = random.Random(5)
    for _ in range(40):
        x = "".join(rng.choice("abc") for _ in range(rng.randint(0, 8)))
        y = "".join(rng.choice("abc") for _ in range(rng.randint(0, 8)))
        r = lcs(x, y)
        assert r["length"] == _brute_lcs_len(x, y)
        assert len(r["lcs"]) == r["length"]
        assert _is_subsequence(r["lcs"], x) and _is_subsequence(r["lcs"], y)


def test_lcs_invalid():
    with pytest.raises(TypeError):
        lcs(123, "abc")
    with pytest.raises(TypeError):
        lcs("abc", None)


def test_steps_recorded():
    t = StepTracker()
    lcs("AB", "AB", t)
    assert t.steps[-1]["path"] and t.comparisons == 4
    t = StepTracker()
    matrix_chain_order([2, 3, 4, 5], t)
    assert t.steps[-1]["table"][0][2] == 64
