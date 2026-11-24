"""
dynamic_programming.py - Matrix Chain Multiplication and LCS (bottom-up tables).
Step state keys: table (2-D list, None = not computed yet), cell (row, col), path (optional).
"""
from core.step_tracker import ensure

INF = float("inf")


def _parenthesize(s, i, j):
    if i == j:
        return f"A{i}"
    k = s[i][j]
    return f"({_parenthesize(s, i, k)} x {_parenthesize(s, k + 1, j)})"


def matrix_chain_order(dims, tracker=None):
    """dims = [p0, p1, ..., pn]: matrix Ai has size p(i-1) x p(i).
    Returns dict(min_cost, parenthesization, m, s) with 1-indexed tables."""
    t = ensure(tracker)
    if not isinstance(dims, (list, tuple)) or len(dims) < 2:
        raise ValueError("dims must be a list with at least 2 numbers.")
    for d in dims:
        if isinstance(d, bool) or not isinstance(d, int) or d <= 0:
            raise ValueError("All dimensions must be positive integers.")
    n = len(dims) - 1
    m = [[0] * (n + 1) for _ in range(n + 1)]
    s = [[0] * (n + 1) for _ in range(n + 1)]

    # cells not yet computed are shown as None
    computed = {(i, i) for i in range(1, n + 1)}

    def snap():
        return [[(m[i][j] if (i, j) in computed else None) for j in range(1, n + 1)]
                for i in range(1, n + 1)]

    if t.recording:
        t.add("Start: a single matrix needs 0 multiplications (diagonal = 0).",
              table=snap(), cell=None)
    for length in range(2, n + 1):
        for i in range(1, n - length + 2):
            j = i + length - 1
            m[i][j] = INF
            parts = []
            for k in range(i, j):
                cost = m[i][k] + m[k + 1][j] + dims[i - 1] * dims[k] * dims[j]
                t.op()
                t.compare()
                parts.append(f"k={k}: m[{i},{k}] + m[{k + 1},{j}] + {dims[i - 1]}*{dims[k]}*{dims[j]} = {cost}")
                if cost < m[i][j]:
                    m[i][j] = cost
                    s[i][j] = k
            computed.add((i, j))
            if t.recording:
                t.add(f"m[{i},{j}] = min over k of "
                      f"m[i,k] + m[k+1,j] + p(i-1)*p(k)*p(j)  ->  {m[i][j]} (best split k={s[i][j]})",
                      table=snap(), cell=(i - 1, j - 1), detail=parts)
    result = {"min_cost": m[1][n], "parenthesization": _parenthesize(s, 1, n), "m": m, "s": s}
    if t.recording:
        t.add(f"Done. Minimum multiplications = {m[1][n]}; order: {result['parenthesization']}",
              table=snap(), cell=(0, n - 1), detail=[])
    return result


def lcs(X, Y, tracker=None):
    """Longest Common Subsequence. Returns dict(length, lcs, table)."""
    t = ensure(tracker)
    if not isinstance(X, str) or not isinstance(Y, str):
        raise TypeError("Both inputs must be strings.")
    m, n = len(X), len(Y)
    L = [[0] * (n + 1) for _ in range(m + 1)]
    done = {(i, 0) for i in range(m + 1)} | {(0, j) for j in range(n + 1)}

    def snap():
        return [[(L[i][j] if (i, j) in done else None) for j in range(n + 1)] for i in range(m + 1)]

    if t.recording:
        t.add("Start: row 0 and column 0 are 0 (an empty string has no common subsequence).",
              table=snap(), cell=None, path=[])
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            t.compare()
            if X[i - 1] == Y[j - 1]:
                L[i][j] = L[i - 1][j - 1] + 1
                text = f"X[{i}]='{X[i - 1]}' == Y[{j}]='{Y[j - 1]}': L[{i}][{j}] = L[{i - 1}][{j - 1}] + 1 = {L[i][j]}"
            else:
                L[i][j] = max(L[i - 1][j], L[i][j - 1])
                text = (f"X[{i}]='{X[i - 1]}' != Y[{j}]='{Y[j - 1]}': "
                        f"L[{i}][{j}] = max(L[{i - 1}][{j}], L[{i}][{j - 1}]) = {L[i][j]}")
            done.add((i, j))
            if t.recording:
                t.add(text, table=snap(), cell=(i, j), path=[])
    # Backtrack to build the actual subsequence
    i, j, chars, path = m, n, [], []
    while i > 0 and j > 0:
        path.append((i, j))
        if X[i - 1] == Y[j - 1]:
            chars.append(X[i - 1])
            i -= 1
            j -= 1
        elif L[i - 1][j] >= L[i][j - 1]:
            i -= 1
        else:
            j -= 1
    result = "".join(chars[::-1])
    if t.recording:
        t.add(f"Backtrack from the bottom-right corner. LCS = '{result}' (length {L[m][n]}).",
              table=snap(), cell=(m, n), path=path)
    return {"length": L[m][n], "lcs": result, "table": L}
