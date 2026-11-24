"""
searching.py - Linear Search and Binary Search (implemented by hand).

Every function takes an optional `tracker` (see core/step_tracker.py) that
records comparisons and step-by-step snapshots for the visualizer.
Step state keys: array, index (item being checked), low, high, found (index or None), done.
"""
from core.step_tracker import ensure


def _check_list(arr):
    if not isinstance(arr, (list, tuple)):
        raise TypeError("Input must be a list or tuple of values.")


def is_sorted(arr):
    """True if arr is in non-decreasing order."""
    return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))


def linear_search(arr, target, tracker=None):
    """Return the index of the first occurrence of target, or -1."""
    t = ensure(tracker)
    _check_list(arr)
    n = len(arr)
    if t.recording:
        t.add("Start: check the items one by one from the left.", array=list(arr),
              index=None, low=0, high=n - 1, found=None, done=False)
    for i in range(n):
        t.compare()
        if t.recording:
            t.add(f"Compare arr[{i}] = {arr[i]} with target {target}.", array=list(arr),
                  index=i, low=0, high=n - 1, found=None, done=False)
        if arr[i] == target:
            if t.recording:
                t.add(f"Match! Target found at index {i}.", array=list(arr),
                      index=i, low=0, high=n - 1, found=i, done=True)
            return i
    if t.recording:
        t.add("Every item was checked. Target is not in the array.", array=list(arr),
              index=None, low=0, high=n - 1, found=None, done=True)
    return -1


def binary_search(arr, target, tracker=None):
    """Return an index of target in the SORTED list arr, or -1.

    Precondition: arr must be sorted ascending. (Not checked here, because the
    check itself would cost O(n) and hide the O(log n) behaviour. The pages
    check it with is_sorted() before calling.)
    Each loop does one three-way comparison, counted as 1 comparison.
    """
    t = ensure(tracker)
    _check_list(arr)
    low, high = 0, len(arr) - 1
    if t.recording:
        t.add("Start: the search range is the whole array.", array=list(arr),
              index=None, low=low, high=high, found=None, done=False)
    while low <= high:
        mid = (low + high) // 2
        t.compare()
        if arr[mid] == target:
            if t.recording:
                t.add(f"mid = {mid}, arr[{mid}] = {arr[mid]} equals target. Found!",
                      array=list(arr), index=mid, low=low, high=high, found=mid, done=True)
            return mid
        if arr[mid] < target:
            if t.recording:
                t.add(f"mid = {mid}, arr[{mid}] = {arr[mid]} < {target}: discard the left half.",
                      array=list(arr), index=mid, low=low, high=high, found=None, done=False)
            low = mid + 1
        else:
            if t.recording:
                t.add(f"mid = {mid}, arr[{mid}] = {arr[mid]} > {target}: discard the right half.",
                      array=list(arr), index=mid, low=low, high=high, found=None, done=False)
            high = mid - 1
    if t.recording:
        t.add("The search range is empty. Target is not in the array.", array=list(arr),
              index=None, low=low, high=high, found=None, done=True)
    return -1
