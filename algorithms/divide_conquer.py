"""
divide_conquer.py - Strassen's matrix multiplication (and classical, for comparison).

Non-power-of-two sizes: the matrices are padded with zeros up to the next power of two
(documented approach), multiplied, and the result is cut back to the original size.
tracker.operations counts scalar multiplications.
"""
import numpy as np
from core.step_tracker import ensure


def _to_matrix(M, name):
    arr = np.asarray(M)
    if arr.ndim != 2 or arr.size == 0:
        raise ValueError(f"Matrix {name} must be a non-empty 2-D matrix.")
    if arr.dtype == bool or not np.issubdtype(arr.dtype, np.number):
        raise TypeError(f"Matrix {name} must contain numbers only.")
    return arr


def _validate_pair(A, B):
    A, B = _to_matrix(A, "A"), _to_matrix(B, "B")
    if A.shape[0] != A.shape[1] or B.shape[0] != B.shape[1]:
        raise ValueError("Both matrices must be square.")
    if A.shape != B.shape:
        raise ValueError("Both matrices must have the same size.")
    return A, B


def next_power_of_two(n):
    p = 1
    while p < n:
        p *= 2
    return p


def _pad(M, size):
    out = np.zeros((size, size), dtype=M.dtype)
    out[:M.shape[0], :M.shape[1]] = M
    return out


def _classical(A, B):
    """Plain triple loop on Python lists."""
    n = A.shape[0]
    a, b = A.tolist(), B.tolist()
    c = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            total = 0
            for k in range(n):
                total += a[i][k] * b[k][j]
            c[i][j] = total
    return np.array(c, dtype=np.result_type(A.dtype, B.dtype))


def classical_matrix_multiply(A, B, tracker=None):
    """Standard O(n^3) multiplication (used to verify Strassen and to compare)."""
    t = ensure(tracker)
    A, B = _validate_pair(A, B)
    t.op(A.shape[0] ** 3)
    return _classical(A, B)


def strassen(A, B, tracker=None, leaf_size=1):
    """Multiply two square matrices with Strassen's 7-multiplication recursion."""
    t = ensure(tracker)
    A, B = _validate_pair(A, B)
    if leaf_size < 1:
        raise ValueError("leaf_size must be at least 1.")
    n = A.shape[0]
    m = next_power_of_two(n)
    if t.recording:
        msg = (f"Matrices are {n}x{n}. " + (f"Padding with zeros to {m}x{m} (next power of two)."
               if m != n else "Size is already a power of two, no padding needed."))
        t.add(msg, depth=0, size=m, data={"A (padded)": _pad(A, m).tolist(),
                                          "B (padded)": _pad(B, m).tolist()})
    C = _strassen(_pad(A, m), _pad(B, m), t, 0, leaf_size)
    result = C[:n, :n]
    if t.recording:
        t.add(f"Remove the padding: final {n}x{n} result.", depth=0, size=n,
              data={"A x B": result.tolist()})
    return result


def _strassen(A, B, t, depth, leaf):
    n = A.shape[0]
    if n <= leaf:
        t.op(n ** 3)
        return A * B if n == 1 else _classical(A, B)
    h = n // 2
    A11, A12, A21, A22 = A[:h, :h], A[:h, h:], A[h:, :h], A[h:, h:]
    B11, B12, B21, B22 = B[:h, :h], B[:h, h:], B[h:, :h], B[h:, h:]
    show = t.recording and depth <= 1
    if show:
        t.add(f"Level {depth}: divide the {n}x{n} matrices into four {h}x{h} quadrants each.",
              depth=depth, size=n,
              data={"A11": A11.tolist(), "A12": A12.tolist(), "A21": A21.tolist(), "A22": A22.tolist(),
                    "B11": B11.tolist(), "B12": B12.tolist(), "B21": B21.tolist(), "B22": B22.tolist()})
    M1 = _strassen(A11 + A22, B11 + B22, t, depth + 1, leaf)
    M2 = _strassen(A21 + A22, B11, t, depth + 1, leaf)
    M3 = _strassen(A11, B12 - B22, t, depth + 1, leaf)
    M4 = _strassen(A22, B21 - B11, t, depth + 1, leaf)
    M5 = _strassen(A11 + A12, B22, t, depth + 1, leaf)
    M6 = _strassen(A21 - A11, B11 + B12, t, depth + 1, leaf)
    M7 = _strassen(A12 - A22, B21 + B22, t, depth + 1, leaf)
    if show:
        t.add(f"Level {depth}: seven recursive products (instead of eight) computed.",
              depth=depth, size=n,
              data={"M1=(A11+A22)(B11+B22)": M1.tolist(), "M2=(A21+A22)B11": M2.tolist(),
                    "M3=A11(B12-B22)": M3.tolist(), "M4=A22(B21-B11)": M4.tolist(),
                    "M5=(A11+A12)B22": M5.tolist(), "M6=(A21-A11)(B11+B12)": M6.tolist(),
                    "M7=(A12-A22)(B21+B22)": M7.tolist()})
    C11 = M1 + M4 - M5 + M7
    C12 = M3 + M5
    C21 = M2 + M4
    C22 = M1 - M2 + M3 + M6
    C = np.block([[C11, C12], [C21, C22]])
    if show:
        t.add(f"Level {depth}: combine. C11=M1+M4-M5+M7, C12=M3+M5, C21=M2+M4, C22=M1-M2+M3+M6.",
              depth=depth, size=n, data={"C11": C11.tolist(), "C12": C12.tolist(),
                                         "C21": C21.tolist(), "C22": C22.tolist(), "C": C.tolist()})
    return C
