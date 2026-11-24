"""
validation.py
-------------
Turns text typed by the user into Python data, with clear error messages.
No Streamlit code here, so it can be unit-tested.
"""
import math
import re


def _to_number(tok, allow_float=True):
    try:
        return int(tok)
    except ValueError:
        pass
    if not allow_float:
        raise ValueError(f"'{tok}' is not a whole number.")
    try:
        val = float(tok)
    except ValueError:
        raise ValueError(f"'{tok}' is not a number.")
    if not math.isfinite(val):
        raise ValueError(f"'{tok}' is not a finite number.")
    return val


def parse_number_list(text, allow_float=True, min_len=0, max_len=None):
    """'5, 3  8;1' -> [5, 3, 8, 1]"""
    tokens = [t for t in re.split(r"[,\s;]+", text.strip()) if t]
    nums = [_to_number(t, allow_float) for t in tokens]
    if len(nums) < min_len:
        raise ValueError(f"Please enter at least {min_len} value(s).")
    if max_len is not None and len(nums) > max_len:
        raise ValueError(f"Please enter at most {max_len} values (got {len(nums)}).")
    return nums


def parse_matrix(text):
    """Rows separated by new lines or ';', numbers by spaces or commas."""
    rows = [r for r in re.split(r"[\n;]+", text.strip()) if r.strip()]
    if not rows:
        raise ValueError("The matrix is empty.")
    matrix = [parse_number_list(r, min_len=1) for r in rows]
    width = len(matrix[0])
    if any(len(r) != width for r in matrix):
        raise ValueError("All rows of the matrix must have the same length.")
    return matrix


def parse_rows(text, ncols, allow_float=True, max_rows=None):
    """Each non-empty line must contain exactly `ncols` numbers."""
    lines = [l for l in text.strip().splitlines() if l.strip()]
    rows = []
    for number, line in enumerate(lines, 1):
        vals = parse_number_list(line, allow_float)
        if len(vals) != ncols:
            raise ValueError(f"Line {number}: expected {ncols} numbers, got {len(vals)}.")
        rows.append(tuple(vals))
    if max_rows is not None and len(rows) > max_rows:
        raise ValueError(f"Please use at most {max_rows} rows.")
    return rows


def parse_vertices(text):
    verts = [v.strip() for v in re.split(r"[,\s]+", text.strip()) if v.strip()]
    if len(set(verts)) != len(verts):
        raise ValueError("Vertex names must be unique.")
    return verts


def parse_edges(text):
    """Lines like 'A B 4' (weight optional, default 1) -> [('A','B',4)]"""
    edges = []
    for number, line in enumerate([l for l in text.strip().splitlines() if l.strip()], 1):
        parts = [p for p in re.split(r"[,\s]+", line.strip()) if p]
        if len(parts) not in (2, 3):
            raise ValueError(f"Edge line {number}: write 'u v weight'.")
        weight = _to_number(parts[2]) if len(parts) == 3 else 1
        edges.append((parts[0], parts[1], weight))
    return edges
