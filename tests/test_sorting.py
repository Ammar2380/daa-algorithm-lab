import random
import pytest
from algorithms.sorting import insertion_sort, merge_sort, quick_sort, heap_sort
from core.step_tracker import StepTracker

SORTS = [insertion_sort, merge_sort, quick_sort, heap_sort]


@pytest.mark.parametrize("f", SORTS)
@pytest.mark.parametrize("data", [
    [], [1], [2, 1], [5, 3, 8, 1, 9, 2], [3, 3, 3, 3], [1, 2, 3, 4, 5], [5, 4, 3, 2, 1],
    [-5, 0, -1, 7, -5], [2.5, -1.5, 2.5, 0], [1, 2, 1, 2, 1, 2],
])
def test_sorts_correctly(f, data):
    assert f(data) == sorted(data)


@pytest.mark.parametrize("f", SORTS)
def test_input_not_modified(f):
    data = [3, 1, 2]
    f(data)
    assert data == [3, 1, 2]


@pytest.mark.parametrize("f", SORTS)
def test_random_arrays(f):
    rng = random.Random(1)
    for _ in range(100):
        data = [rng.randint(-50, 50) for _ in range(rng.randint(0, 40))]
        assert f(data) == sorted(data)


@pytest.mark.parametrize("f", SORTS)
def test_large_sorted_and_reverse(f):
    assert f(list(range(1500))) == list(range(1500))       # quick sort worst case, no recursion error
    assert f(list(range(1500, 0, -1))) == list(range(1, 1501))


@pytest.mark.parametrize("f", SORTS)
def test_invalid_input(f):
    with pytest.raises(TypeError):
        f("abc")
    with pytest.raises(TypeError):
        f([1, "a", 3])
    with pytest.raises(TypeError):
        f(5)


@pytest.mark.parametrize("f", SORTS)
def test_steps_end_sorted(f):
    t = StepTracker()
    f([4, 2, 9, 1], t)
    assert t.steps[-1]["array"] == [1, 2, 4, 9]
    assert t.steps[-1]["sorted"] == [0, 1, 2, 3]


def test_complexity_shape_insertion_sort():
    n = 100
    best, worst = StepTracker(), StepTracker()
    insertion_sort(list(range(n)), best)
    insertion_sort(list(range(n, 0, -1)), worst)
    assert best.comparisons == n - 1                       # O(n) best case
    assert worst.comparisons == n * (n - 1) // 2           # O(n^2) worst case


def test_merge_sort_comparisons_bound():
    t = StepTracker(record_steps=False)
    merge_sort(list(range(256, 0, -1)), t)
    assert t.comparisons <= 256 * 8
