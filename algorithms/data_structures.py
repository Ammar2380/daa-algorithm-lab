"""
data_structures.py
------------------
Small helper structures written by hand (instead of heapq / sorted):
MinHeap, UnionFind and a stable merge sort that sorts by a key.
"""
from core.step_tracker import ensure


class MinHeap:
    """Binary min-heap. Items are compared with <, so use tuples like (priority, id, data)."""

    def __init__(self):
        self.data = []

    def __len__(self):
        return len(self.data)

    def push(self, item):
        a = self.data
        a.append(item)
        i = len(a) - 1
        while i > 0:
            parent = (i - 1) // 2
            if a[i] < a[parent]:
                a[i], a[parent] = a[parent], a[i]
                i = parent
            else:
                break

    def pop(self):
        a = self.data
        if not a:
            raise IndexError("pop from empty heap")
        top = a[0]
        last = a.pop()
        if a:
            a[0] = last
            i, n = 0, len(a)
            while True:
                left, right, small = 2 * i + 1, 2 * i + 2, i
                if left < n and a[left] < a[small]:
                    small = left
                if right < n and a[right] < a[small]:
                    small = right
                if small == i:
                    break
                a[i], a[small] = a[small], a[i]
                i = small
        return top

    def peek(self):
        return self.data[0]


class UnionFind:
    """Disjoint sets with path compression and union by rank."""

    def __init__(self, items):
        self.parent = {x: x for x in items}
        self.rank = {x: 0 for x in items}

    def find(self, x):
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[x] != root:          # path compression
            self.parent[x], x = root, self.parent[x]
        return root

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        return True


def merge_sort_by(items, key, tracker=None):
    """Stable merge sort of `items` by key(item). Returns a new list. O(n log n)."""
    t = ensure(tracker)
    items = list(items)
    if len(items) <= 1:
        return items
    mid = len(items) // 2
    left = merge_sort_by(items[:mid], key, t)
    right = merge_sort_by(items[mid:], key, t)
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        t.compare()
        if key(left[i]) <= key(right[j]):
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    out.extend(left[i:])
    out.extend(right[j:])
    return out
