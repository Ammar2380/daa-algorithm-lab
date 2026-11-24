import itertools
import random
import pytest
from algorithms.greedy import activity_selection, fractional_knapsack, huffman_coding, huffman_decode


def _compatible(acts, idxs):
    s = sorted(idxs, key=lambda i: acts[i][1])
    return all(acts[b][0] >= acts[a][1] for a, b in zip(s, s[1:]))


def test_activity_textbook():
    acts = [(1, 4), (3, 5), (0, 6), (5, 7), (3, 9), (5, 9), (6, 10), (8, 11), (8, 12), (2, 14), (12, 16)]
    sel = activity_selection(acts)["selected"]
    assert len(sel) == 4 and _compatible(acts, sel)


def test_activity_edge_cases():
    assert activity_selection([])["selected"] == []
    assert activity_selection([(1, 2)])["selected"] == [0]
    assert len(activity_selection([(1, 3), (1, 3), (1, 3)])["selected"]) == 1   # duplicates
    assert len(activity_selection([(1, 2), (2, 3), (3, 4)])["selected"]) == 3   # touching ends allowed
    assert len(activity_selection([(-5, -1), (-1, 3)])["selected"]) == 2        # negative times


def test_activity_optimal_vs_brute_force():
    rng = random.Random(2)
    for _ in range(40):
        acts = []
        for _ in range(rng.randint(1, 8)):
            s = rng.randint(0, 10)
            acts.append((s, s + rng.randint(0, 5)))
        best = max(r for r in range(len(acts) + 1)
                   for c in itertools.combinations(range(len(acts)), r) if _compatible(acts, c))
        assert len(activity_selection(acts)["selected"]) == best


def test_activity_invalid():
    with pytest.raises(ValueError):
        activity_selection([(5, 2)])
    with pytest.raises(ValueError):
        activity_selection([(1, 2, 3)])


def test_knapsack_textbook():
    r = fractional_knapsack([(60, 10), (100, 20), (120, 30)], 50)
    assert r["total_value"] == pytest.approx(240.0)
    assert r["taken"][-1][1] == pytest.approx(2 / 3)


def test_knapsack_edge_cases():
    assert fractional_knapsack([], 10)["total_value"] == 0
    assert fractional_knapsack([(10, 5)], 0)["total_value"] == 0
    assert fractional_knapsack([(10, 5)], 100)["total_value"] == pytest.approx(10)   # all fit
    assert fractional_knapsack([(10, 5)], 2.5)["total_value"] == pytest.approx(5)
    assert fractional_knapsack([(0, 5), (7, 1)], 1)["total_value"] == pytest.approx(7)


def test_knapsack_invalid():
    with pytest.raises(ValueError):
        fractional_knapsack([(10, 0)], 5)
    with pytest.raises(ValueError):
        fractional_knapsack([(10, 5)], -1)
    with pytest.raises(ValueError):
        fractional_knapsack([(-1, 5)], 5)


def test_huffman_roundtrip_and_prefix_free():
    for text in ["abracadabra", "aabbbcccc", "hello world", "a", "aaaa", "ab", "The quick brown fox"]:
        r = huffman_coding(text)
        assert huffman_decode(r["encoded"], r["tree"]) == text
        codes = list(r["codes"].values())
        for a, b in itertools.permutations(codes, 2):
            assert not b.startswith(a)                       # prefix-free


def test_huffman_optimal_length_known():
    # Frequencies 5,9,12,13,16,45 -> optimal weighted length is 224 bits
    text = "a" * 5 + "b" * 9 + "c" * 12 + "d" * 13 + "e" * 16 + "f" * 45
    assert len(huffman_coding(text)["encoded"]) == 224


def test_huffman_frequent_chars_get_shorter_codes():
    r = huffman_coding("aaaaaaaabbbc")
    assert len(r["codes"]["a"]) <= len(r["codes"]["c"])


def test_huffman_invalid():
    with pytest.raises(ValueError):
        huffman_coding("")
    with pytest.raises(TypeError):
        huffman_coding(123)
