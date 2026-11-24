"""
sorting.py - Insertion, Merge, Quick and Heap Sort (implemented by hand).

Each function returns a NEW sorted list (the input is not modified).
Step state keys: array (snapshot), comparing (indices), moved (indices written/swapped),
sorted (indices already in final place), range (optional active (lo, hi) slice).
tracker.swap counts swaps or element moves/writes.
"""
from core.step_tracker import ensure


def _prepare(arr):
    if not isinstance(arr, (list, tuple)):
        raise TypeError("Input must be a list or tuple of numbers.")
    for x in arr:
        if isinstance(x, bool) or not isinstance(x, (int, float)):
            raise TypeError(f"All items must be numbers, found {x!r}.")
    return list(arr)


def _snap(t, text, a, comparing=(), moved=(), sorted_=(), rng=None):
    if t.recording:
        t.add(text, array=list(a), comparing=list(comparing), moved=list(moved),
              sorted=list(sorted_), range=rng)


def insertion_sort(arr, tracker=None):
    t = ensure(tracker)
    a = _prepare(arr)
    n = len(a)
    _snap(t, "Start. The first element alone is already 'sorted'.", a, sorted_=range(min(n, 1)))
    for i in range(1, n):
        key = a[i]
        j = i - 1
        _snap(t, f"Take key = a[{i}] = {key} and insert it into the sorted part.", a,
              comparing=[i], sorted_=range(i))
        while j >= 0:
            t.compare()
            if a[j] > key:
                a[j + 1] = a[j]
                t.swap()
                _snap(t, f"{a[j]} > {key}: shift {a[j]} one place right.", a,
                      comparing=[j], moved=[j + 1], sorted_=range(i))
                j -= 1
            else:
                break
        a[j + 1] = key
        _snap(t, f"Place key {key} at index {j + 1}.", a, moved=[j + 1], sorted_=range(i + 1))
    _snap(t, "Done. The array is sorted.", a, sorted_=range(n))
    return a


def merge_sort(arr, tracker=None):
    t = ensure(tracker)
    a = _prepare(arr)
    n = len(a)
    _snap(t, "Start. Split the array in halves until single elements remain.", a)

    def merge(lo, mid, hi):
        left, right = a[lo:mid], a[mid:hi]
        i = j = 0
        k = lo
        while i < len(left) and j < len(right):
            t.compare()
            if left[i] <= right[j]:
                a[k] = left[i]
                i += 1
            else:
                a[k] = right[j]
                j += 1
            t.swap()
            _snap(t, f"Merge: write {a[k]} to index {k}.", a, moved=[k], rng=(lo, hi))
            k += 1
        for value in left[i:] + right[j:]:
            a[k] = value
            t.swap()
            _snap(t, f"Merge: copy leftover {value} to index {k}.", a, moved=[k], rng=(lo, hi))
            k += 1

    def sort(lo, hi):            # sorts a[lo:hi]
        if hi - lo <= 1:
            return
        mid = (lo + hi) // 2
        sort(lo, mid)
        sort(mid, hi)
        merge(lo, mid, hi)

    sort(0, n)
    _snap(t, "Done. The array is sorted.", a, sorted_=range(n))
    return a


def quick_sort(arr, tracker=None):
    """Lomuto partition, last element as pivot. Uses an explicit stack instead of
    recursion so that already-sorted inputs (worst case) cannot hit Python's
    recursion limit."""
    t = ensure(tracker)
    a = _prepare(arr)
    n = len(a)
    done = set()
    _snap(t, "Start. Choose the last element of each range as the pivot.", a)
    stack = [(0, n - 1)]
    while stack:
        lo, hi = stack.pop()
        if lo > hi:
            continue
        if lo == hi:
            done.add(lo)
            continue
        pivot = a[hi]
        _snap(t, f"Partition a[{lo}..{hi}] around pivot {pivot}.", a, comparing=[hi],
              sorted_=done, rng=(lo, hi + 1))
        i = lo - 1
        for j in range(lo, hi):
            t.compare()
            if a[j] <= pivot:
                i += 1
                if i != j:
                    a[i], a[j] = a[j], a[i]
                    t.swap()
                    _snap(t, f"{a[i]} <= pivot {pivot}: swap positions {i} and {j}.", a,
                          comparing=[j], moved=[i, j], sorted_=done, rng=(lo, hi + 1))
        p = i + 1
        if p != hi:
            a[p], a[hi] = a[hi], a[p]
            t.swap()
        done.add(p)
        _snap(t, f"Pivot {pivot} is now at its final index {p}.", a, moved=[p],
              sorted_=done, rng=(lo, hi + 1))
        stack.append((p + 1, hi))
        stack.append((lo, p - 1))       # left part is processed first
    _snap(t, "Done. The array is sorted.", a, sorted_=range(n))
    return a


def heap_sort(arr, tracker=None):
    t = ensure(tracker)
    a = _prepare(arr)
    n = len(a)
    _snap(t, "Start. First build a max-heap from the array.", a)

    def sift_down(root, size, final):
        while True:
            child = 2 * root + 1
            if child >= size:
                break
            if child + 1 < size:
                t.compare()
                if a[child + 1] > a[child]:
                    child += 1
            t.compare()
            if a[root] < a[child]:
                a[root], a[child] = a[child], a[root]
                t.swap()
                _snap(t, f"Sift down: swap parent {root} with larger child {child}.", a,
                      comparing=[root, child], moved=[root, child], sorted_=final)
                root = child
            else:
                break

    for start in range(n // 2 - 1, -1, -1):
        sift_down(start, n, [])
    _snap(t, "Max-heap built. The largest value is at index 0.", a)
    for end in range(n - 1, 0, -1):
        a[0], a[end] = a[end], a[0]
        t.swap()
        _snap(t, f"Move the maximum {a[end]} to its final index {end}.", a,
              moved=[0, end], sorted_=range(end, n))
        sift_down(0, end, range(end, n))
    _snap(t, "Done. The array is sorted.", a, sorted_=range(n))
    return a
