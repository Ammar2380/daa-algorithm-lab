import pytest
from algorithms.searching import linear_search, binary_search, is_sorted
from core.step_tracker import StepTracker

BOTH = [linear_search, binary_search]


@pytest.mark.parametrize("f", BOTH)
def test_found_and_missing(f):
    arr = [1, 3, 5, 7, 9, 11]
    assert arr[f(arr, 7)] == 7
    assert f(arr, 4) == -1
    assert f(arr, 100) == -1 and f(arr, -5) == -1


@pytest.mark.parametrize("f", BOTH)
def test_empty_and_single(f):
    assert f([], 1) == -1
    assert f([5], 5) == 0
    assert f([5], 6) == -1


@pytest.mark.parametrize("f", BOTH)
def test_negative_values_and_ends(f):
    arr = [-10, -3, 0, 4, 8]
    assert f(arr, -10) == 0 and f(arr, 8) == 4 and f(arr, -3) == 1


def test_duplicates():
    arr = [2, 2, 2, 5, 5]
    assert linear_search(arr, 2) == 0              # first occurrence
    assert arr[binary_search(arr, 5)] == 5


@pytest.mark.parametrize("f", BOTH)
def test_invalid_input(f):
    with pytest.raises(TypeError):
        f("not a list", 1)
    with pytest.raises(TypeError):
        f(None, 1)


def test_binary_search_all_positions():
    arr = list(range(0, 40, 2))
    for i, v in enumerate(arr):
        assert binary_search(arr, v) == i


def test_comparison_counts():
    t = StepTracker()
    linear_search([1, 2, 3, 4], 4, t)
    assert t.comparisons == 4
    t = StepTracker()
    binary_search(list(range(1024)), -1, t)
    assert t.comparisons <= 11                    # about log2(n) + 1


def test_steps_recorded():
    t = StepTracker()
    binary_search([1, 2, 3], 3, t)
    assert t.steps[-1]["found"] == 2 and t.steps[-1]["done"]


def test_is_sorted():
    assert is_sorted([]) and is_sorted([1]) and is_sorted([1, 1, 2])
    assert not is_sorted([2, 1])
