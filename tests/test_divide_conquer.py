import numpy as np
import pytest
from algorithms.divide_conquer import strassen, classical_matrix_multiply, next_power_of_two
from core.step_tracker import StepTracker


def test_known_2x2():
    assert strassen([[1, 2], [3, 4]], [[5, 6], [7, 8]]).tolist() == [[19, 22], [43, 50]]


def test_1x1():
    assert strassen([[3]], [[4]]).tolist() == [[12]]


@pytest.mark.parametrize("n", [1, 2, 3, 4, 5, 6, 7, 8, 9, 16])
def test_matches_classical_including_non_power_of_two(n):
    rng = np.random.default_rng(n)
    A = rng.integers(-9, 10, (n, n))
    B = rng.integers(-9, 10, (n, n))
    result = strassen(A, B)
    assert result.shape == (n, n)
    assert np.array_equal(result, classical_matrix_multiply(A, B))
    assert np.array_equal(result, A @ B)                   # independent check only in tests


def test_identity_and_zero():
    A = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    I = np.eye(3, dtype=int)
    assert np.array_equal(strassen(A, I), np.array(A))
    assert not strassen(A, np.zeros((3, 3), dtype=int)).any()


def test_float_matrices():
    A, B = [[1.5, 2], [0, 1]], [[2, 0], [1, 1]]
    assert np.allclose(strassen(A, B), np.array(A) @ np.array(B))


def test_leaf_size():
    A = np.arange(16).reshape(4, 4)
    assert np.array_equal(strassen(A, A, leaf_size=2), A @ A)


def test_fewer_multiplications_than_classical():
    A = np.ones((8, 8), dtype=int)
    s, c = StepTracker(False), StepTracker(False)
    strassen(A, A, s)
    classical_matrix_multiply(A, A, c)
    assert s.operations == 7 ** 3 and c.operations == 8 ** 3


@pytest.mark.parametrize("A,B,exc", [
    ([[1, 2, 3]], [[1, 2, 3]], ValueError),                # not square
    ([[1, 2], [3, 4]], [[1]], ValueError),                 # different sizes
    ([], [], ValueError),                                  # empty
    ([1, 2, 3], [1, 2, 3], ValueError),                    # 1-D
    ([["a", "b"], ["c", "d"]], [[1, 2], [3, 4]], TypeError),
])
def test_invalid_inputs(A, B, exc):
    with pytest.raises(exc):
        strassen(A, B)


def test_steps_have_seven_products():
    t = StepTracker()
    strassen([[1, 2], [3, 4]], [[5, 6], [7, 8]], t)
    assert any(len(s.get("data", {})) == 7 for s in t.steps)


def test_next_power_of_two():
    assert [next_power_of_two(n) for n in (1, 2, 3, 5, 8, 9)] == [1, 2, 4, 8, 8, 16]
