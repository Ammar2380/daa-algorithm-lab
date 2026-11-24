"""
benchmark.py - fair, repeatable timing of algorithms.

Fairness rules used:
* For each input size the SAME dataset (made with a fixed random seed) is given to every
  algorithm of the suite.
* Each algorithm is run `repeats` times and the MEDIAN time is reported (the minimum is also
  stored) to reduce timing noise.
* Operation counts come from one separate instrumented run (StepTracker without step
  recording), so counting does not disturb the timing runs.
No results are hard-coded: every number is measured when you press the button.
"""
import random
import statistics
import time
from dataclasses import dataclass, field

import numpy as np

from algorithms.dynamic_programming import lcs, matrix_chain_order
from algorithms.divide_conquer import classical_matrix_multiply, strassen
from algorithms.graph_algorithms import bfs, build_adjacency, dfs, dijkstra, kruskal
from algorithms.greedy import activity_selection, fractional_knapsack, huffman_coding
from algorithms.searching import binary_search, linear_search
from algorithms.sorting import heap_sort, insertion_sort, merge_sort, quick_sort
from core.complexity import f_logn, f_n, f_n2, f_n3, f_nlogn, f_strassen
from core.step_tracker import StepTracker


@dataclass
class Suite:
    name: str
    description: str
    scenarios: list
    default_sizes: list
    max_size: int
    size_label: str
    make_data: callable                 # (size, scenario, seed) -> data
    algorithms: dict                    # label -> callable(data, tracker)
    theory: dict = field(default_factory=dict)   # label -> (notation, function)


# ------------------------------------------------------------------ data makers
def _sorting_data(n, scenario, seed):
    rng = random.Random(seed)
    if scenario == "Already sorted":
        return list(range(n))
    if scenario == "Reverse sorted":
        return list(range(n, 0, -1))
    if scenario == "Many duplicates":
        return [rng.randint(0, 9) for _ in range(n)]
    return [rng.randint(0, 10 * n) for _ in range(n)]


def _search_data(n, scenario, seed):
    arr = list(range(0, 2 * n, 2))      # sorted even numbers
    target = {"Target absent (worst case)": -1, "Target at first position": arr[0],
              "Target in the middle": arr[n // 2], "Target at last position": arr[-1]}[scenario]
    return arr, target


def _matrix_data(n, scenario, seed):
    rng = np.random.default_rng(seed)
    return rng.integers(0, 10, (n, n)), rng.integers(0, 10, (n, n))


def _dp_data(n, scenario, seed):
    rng = random.Random(seed)
    dims = [rng.randint(5, 50) for _ in range(n + 1)]
    x = "".join(rng.choice("ACGT") for _ in range(n))
    y = "".join(rng.choice("ACGT") for _ in range(n))
    return dims, x, y


def _greedy_data(n, scenario, seed):
    rng = random.Random(seed)
    acts = []
    for _ in range(n):
        s = rng.randint(0, 10 * n)
        acts.append((s, s + rng.randint(1, 20)))
    items = [(rng.randint(1, 100), rng.randint(1, 50)) for _ in range(n)]
    text = "".join(rng.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(n))
    return acts, items, sum(w for _, w in items) // 2, text


def _graph_data(n, scenario, seed):
    rng = random.Random(seed)
    vertices = list(range(n))
    edge_set = set()
    for v in range(1, n):                       # random spanning tree -> connected
        edge_set.add((rng.randrange(v), v))
    target = min(3 * n, n * (n - 1) // 2)
    while len(edge_set) < target:
        a, b = rng.sample(vertices, 2) if n > 1 else (0, 0)
        edge_set.add((min(a, b), max(a, b)))
    edges = [(a, b, rng.randint(1, 20)) for a, b in sorted(edge_set)]
    return vertices, edges, build_adjacency(vertices, edges)


SUITES = {
    "Sorting": Suite(
        "Sorting", "Insertion, Merge, Quick and Heap sort on the same array.",
        ["Random", "Already sorted", "Reverse sorted", "Many duplicates"],
        [100, 200, 400, 800, 1600], 5000, "array length n", _sorting_data,
        {"Insertion Sort": lambda d, t: insertion_sort(d, t), "Merge Sort": lambda d, t: merge_sort(d, t),
         "Quick Sort": lambda d, t: quick_sort(d, t), "Heap Sort": lambda d, t: heap_sort(d, t)},
        {"Insertion Sort": ("O(n^2) avg/worst, O(n) best", f_n2), "Merge Sort": ("O(n log n)", f_nlogn),
         "Quick Sort": ("O(n log n) avg, O(n^2) worst", f_nlogn), "Heap Sort": ("O(n log n)", f_nlogn)}),
    "Searching": Suite(
        "Searching", "Linear vs Binary search on the same SORTED array.",
        ["Target absent (worst case)", "Target in the middle", "Target at first position",
         "Target at last position"],
        [1000, 5000, 20000, 100000, 400000], 1000000, "array length n", _search_data,
        {"Linear Search": lambda d, t: linear_search(d[0], d[1], t),
         "Binary Search": lambda d, t: binary_search(d[0], d[1], t)},
        {"Linear Search": ("O(n)", f_n), "Binary Search": ("O(log n)", f_logn)}),
    "Divide and Conquer": Suite(
        "Divide and Conquer", "Classical O(n^3) multiplication vs Strassen on the same matrices.",
        ["Random integer matrices"], [2, 4, 8, 16, 32, 64], 64, "matrix dimension n", _matrix_data,
        {"Classical": lambda d, t: classical_matrix_multiply(d[0], d[1], t),
         "Strassen": lambda d, t: strassen(d[0], d[1], t)},
        {"Classical": ("Theta(n^3)", f_n3), "Strassen": ("Theta(n^2.81)", f_strassen)}),
    "Dynamic Programming": Suite(
        "Dynamic Programming",
        "Matrix Chain (n matrices) and LCS (two strings of length n). Different problems, same size n.",
        ["Random input"], [10, 20, 40, 80, 120], 200, "n (matrices / string length)", _dp_data,
        {"Matrix Chain Multiplication": lambda d, t: matrix_chain_order(d[0], t),
         "LCS": lambda d, t: lcs(d[1], d[2], t)},
        {"Matrix Chain Multiplication": ("Theta(n^3)", f_n3), "LCS": ("Theta(n^2)", f_n2)}),
    "Greedy Algorithms": Suite(
        "Greedy Algorithms", "Activity Selection, Fractional Knapsack and Huffman Coding (n items / n characters).",
        ["Random input"], [100, 500, 1000, 2000, 5000], 20000, "n (activities / items / characters)",
        _greedy_data,
        {"Activity Selection": lambda d, t: activity_selection(d[0], t),
         "Fractional Knapsack": lambda d, t: fractional_knapsack(d[1], d[2], t),
         "Huffman Coding": lambda d, t: huffman_coding(d[3], t)},
        {"Activity Selection": ("O(n log n)", f_nlogn), "Fractional Knapsack": ("O(n log n)", f_nlogn),
         "Huffman Coding": ("O(n + k log k), k=26 fixed ~ O(n)", f_n)}),
    "Graph Algorithms": Suite(
        "Graph Algorithms", "BFS, DFS, Dijkstra and Kruskal on the same random connected graph (V=n, E~3n).",
        ["Random connected graph"], [50, 100, 200, 400, 800], 3000, "number of vertices V",
        _graph_data,
        {"BFS": lambda d, t: bfs(d[2], 0, t), "DFS": lambda d, t: dfs(d[2], 0, t),
         "Dijkstra": lambda d, t: dijkstra(d[2], 0, t), "Kruskal": lambda d, t: kruskal(d[0], d[1], t)},
        {"BFS": ("O(V + E)", f_n), "DFS": ("O(V + E)", f_n),
         "Dijkstra": ("O((V + E) log V)", f_nlogn), "Kruskal": ("O(E log E)", f_nlogn)}),
}


def time_function(func, repeats):
    """Run func() `repeats` times; return (median_ms, min_ms)."""
    times = []
    for _ in range(repeats):
        start = time.perf_counter()
        func()
        times.append((time.perf_counter() - start) * 1000)
    return statistics.median(times), min(times)


def run_suite(suite, scenario, sizes, repeats=5, seed=42, progress=None):
    """Return a list of result rows (dicts), one per (size, algorithm)."""
    if repeats < 1:
        raise ValueError("repeats must be at least 1.")
    if not sizes:
        raise ValueError("Choose at least one input size.")
    if scenario not in suite.scenarios:
        raise ValueError(f"Unknown scenario {scenario!r}.")
    rows, total, done = [], len(sizes) * len(suite.algorithms), 0
    for n in sizes:
        if n < 1 or n > suite.max_size:
            raise ValueError(f"Size {n} is outside 1..{suite.max_size} for this suite.")
        data = suite.make_data(n, scenario, seed)          # same data for every algorithm
        for label, fn in suite.algorithms.items():
            tracker = StepTracker(record_steps=False)
            fn(data, tracker)                              # instrumented run (operation counts)
            median_ms, min_ms = time_function(lambda: fn(data, None), repeats)
            rows.append({"Algorithm": label, "n": n, "Median time (ms)": median_ms,
                         "Min time (ms)": min_ms, "Comparisons": tracker.comparisons,
                         "Swaps/moves": tracker.swaps, "Other operations": tracker.operations,
                         "Total operations": tracker.total_operations()})
            done += 1
            if progress:
                progress(done / total)
    return rows
