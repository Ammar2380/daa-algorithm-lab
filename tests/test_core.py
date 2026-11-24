import pytest
from core.benchmark import SUITES, run_suite
from core.validation import (parse_number_list, parse_matrix, parse_rows, parse_edges, parse_vertices)
from core.algorithm_registry import ALGORITHMS, CATEGORIES, count_total, count_implemented
from core.complexity import ALGORITHM_INFO


@pytest.mark.parametrize("name", list(SUITES))
def test_every_suite_runs_on_small_input(name):
    suite = SUITES[name]
    rows = run_suite(suite, suite.scenarios[0], [4, 8], repeats=2)
    assert len(rows) == 2 * len(suite.algorithms)
    assert all(r["Median time (ms)"] >= 0 and r["Total operations"] >= 0 for r in rows)


def test_same_seed_gives_same_data_and_counts():
    s = SUITES["Sorting"]
    a = run_suite(s, "Random", [50], repeats=1, seed=7)
    b = run_suite(s, "Random", [50], repeats=1, seed=7)
    assert [r["Comparisons"] for r in a] == [r["Comparisons"] for r in b]


def test_benchmark_validation():
    s = SUITES["Sorting"]
    with pytest.raises(ValueError):
        run_suite(s, "Random", [], 1)
    with pytest.raises(ValueError):
        run_suite(s, "Random", [10], 0)
    with pytest.raises(ValueError):
        run_suite(s, "Random", [10 ** 9], 1)
    with pytest.raises(ValueError):
        run_suite(s, "Nope", [10], 1)


def test_parsers():
    assert parse_number_list("5, 3  8;1.5") == [5, 3, 8, 1.5]
    assert parse_number_list("") == []
    assert parse_matrix("1 2\n3 4") == [[1, 2], [3, 4]]
    assert parse_rows("1 4\n3 5", 2) == [(1, 4), (3, 5)]
    assert parse_edges("A B 4\nB C") == [("A", "B", 4), ("B", "C", 1)]
    assert parse_vertices("A, B C") == ["A", "B", "C"]


@pytest.mark.parametrize("call", [
    lambda: parse_number_list("1, x"), lambda: parse_number_list("nan"),
    lambda: parse_number_list("1 2 3", max_len=2), lambda: parse_number_list("", min_len=1),
    lambda: parse_matrix("1 2\n3"), lambda: parse_matrix(""), lambda: parse_rows("1 2 3", 2),
    lambda: parse_edges("A"), lambda: parse_edges("A B x"), lambda: parse_vertices("A A"),
])
def test_parser_errors(call):
    with pytest.raises(ValueError):
        call()


def test_registry_and_docs_consistent():
    assert count_total() == 16 and len(CATEGORIES) == 6
    assert count_implemented() == 16
    assert {a.name for a in ALGORITHMS} == set(ALGORITHM_INFO)
    for info in ALGORITHM_INFO.values():
        for key in ("problem", "pseudocode", "best", "average", "worst", "space", "example"):
            assert info[key]
