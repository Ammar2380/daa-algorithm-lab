"""
algorithm_registry.py - the list of categories and algorithms shown on the dashboard.

`implemented` is True only for algorithms that are coded AND covered by passing tests
(see tests/). The dashboard counts are computed from this file.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Algorithm:
    name: str
    category: str
    implemented: bool = False
    test_file: str = ""


CATEGORIES = {
    "Searching": {"icon": "🔍", "page": "views/1_Searching.py",
                  "description": "Find a target value in a collection: check items one by one, or halve a sorted list."},
    "Sorting": {"icon": "📊", "page": "views/2_Sorting.py",
                "description": "Arrange data in order and compare simple, divide-and-conquer and heap-based methods."},
    "Divide and Conquer": {"icon": "🧩", "page": "views/3_Divide_Conquer.py",
                           "description": "Split a problem, solve the parts, combine the answers (Strassen's matrix product)."},
    "Dynamic Programming": {"icon": "🧮", "page": "views/4_Dynamic_Programming.py",
                            "description": "Solve overlapping subproblems once and store results in a table."},
    "Greedy Algorithms": {"icon": "🎯", "page": "views/5_Greedy.py",
                          "description": "Make the best-looking choice at each step to build a global solution."},
    "Graph Algorithms": {"icon": "🕸️", "page": "views/6_Graph_Algorithms.py",
                         "description": "Traverse networks, find shortest paths and minimum spanning trees."},
}

_T = {"Searching": "tests/test_searching.py", "Sorting": "tests/test_sorting.py",
      "Divide and Conquer": "tests/test_divide_conquer.py",
      "Dynamic Programming": "tests/test_dynamic_programming.py",
      "Greedy Algorithms": "tests/test_greedy.py", "Graph Algorithms": "tests/test_graph_algorithms.py"}


def _a(name, category):
    return Algorithm(name, category, implemented=True, test_file=_T[category])


ALGORITHMS = [
    _a("Linear Search", "Searching"), _a("Binary Search", "Searching"),
    _a("Insertion Sort", "Sorting"), _a("Merge Sort", "Sorting"),
    _a("Quick Sort", "Sorting"), _a("Heap Sort", "Sorting"),
    _a("Strassen's Matrix Multiplication", "Divide and Conquer"),
    _a("Matrix Chain Multiplication", "Dynamic Programming"),
    _a("Longest Common Subsequence (LCS)", "Dynamic Programming"),
    _a("Activity Selection", "Greedy Algorithms"), _a("Fractional Knapsack", "Greedy Algorithms"),
    _a("Huffman Coding", "Greedy Algorithms"),
    _a("Breadth-First Search (BFS)", "Graph Algorithms"), _a("Depth-First Search (DFS)", "Graph Algorithms"),
    _a("Dijkstra's Shortest Path", "Graph Algorithms"), _a("Kruskal's Minimum Spanning Tree", "Graph Algorithms"),
]


def get_algorithms_by_category(category):
    return [a for a in ALGORITHMS if a.category == category]


def count_total():
    return len(ALGORITHMS)


def count_implemented():
    return sum(1 for a in ALGORITHMS if a.implemented)
