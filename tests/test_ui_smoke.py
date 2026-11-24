"""Headless UI smoke tests: every page and every algorithm option must render without an exception."""
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

PAGES = ["0_Dashboard", "1_Searching", "2_Sorting", "3_Divide_Conquer", "4_Dynamic_Programming",
         "5_Greedy", "6_Graph_Algorithms", "7_Performance_Analyzer"]


@pytest.fixture
def app():
    return AppTest.from_file(str(Path(__file__).resolve().parent.parent / "app.py"), default_timeout=90).run()


def open_page(app, name):
    return app.switch_page(f"views/{name}.py").run()


@pytest.mark.parametrize("page", PAGES)
def test_page_renders(app, page):
    at = open_page(app, page)
    assert not at.exception


@pytest.mark.parametrize("page,options", [
    ("1_Searching", ["Linear Search", "Binary Search"]),
    ("2_Sorting", ["Insertion Sort", "Merge Sort", "Quick Sort", "Heap Sort"]),
    ("4_Dynamic_Programming", ["Matrix Chain Multiplication", "Longest Common Subsequence (LCS)"]),
    ("5_Greedy", ["Activity Selection", "Fractional Knapsack", "Huffman Coding"]),
    ("6_Graph_Algorithms", ["BFS", "DFS", "Dijkstra", "Kruskal"]),
])
def test_every_algorithm_option(app, page, options):
    at = open_page(app, page)
    for option in options:
        at.radio[0].set_value(option).run()
        assert not at.exception, option


def test_invalid_input_shows_error_not_crash(app):
    at = open_page(app, "1_Searching")
    at.text_input[0].set_value("1, two, 3").run()
    assert not at.exception and at.error


def test_binary_search_unsorted_warns(app):
    at = open_page(app, "1_Searching")
    at.radio[0].set_value("Binary Search").run()
    at.text_input[0].set_value("9, 3, 7").run()
    assert not at.exception and at.error      # "array is NOT sorted" message


def test_non_square_matrix_rejected(app):
    at = open_page(app, "3_Divide_Conquer")
    at.text_area[0].set_value("1 2 3").run()
    assert not at.exception and at.error


def test_disconnected_graph_page(app):
    at = open_page(app, "6_Graph_Algorithms")
    at.selectbox[0].set_value("Disconnected graph (two parts)").run()
    assert not at.exception


def test_benchmark_button_runs(app):
    at = open_page(app, "7_Performance_Analyzer")
    at.text_input[0].set_value("10, 20").run()
    at.button[0].click().run()
    assert not at.exception and not at.error


# ---- drive every visualizer through (almost) all of its steps: the step renderers are where UI bugs hide
STEP_CASES = [
    ("1_Searching", None, "search_slider"), ("1_Searching", "Binary Search", "search_slider"),
    ("2_Sorting", None, "sort_slider"), ("2_Sorting", "Merge Sort", "sort_slider"),
    ("2_Sorting", "Quick Sort", "sort_slider"), ("2_Sorting", "Heap Sort", "sort_slider"),
    ("3_Divide_Conquer", None, "strassen_slider"),
    ("4_Dynamic_Programming", None, "mcm_slider"),
    ("4_Dynamic_Programming", "Longest Common Subsequence (LCS)", "lcs_slider"),
    ("5_Greedy", None, "act_slider"), ("5_Greedy", "Fractional Knapsack", "knap_slider"),
    ("5_Greedy", "Huffman Coding", "huff_slider"),
    ("6_Graph_Algorithms", None, "graph_slider"), ("6_Graph_Algorithms", "DFS", "graph_slider"),
    ("6_Graph_Algorithms", "Dijkstra", "graph_slider"), ("6_Graph_Algorithms", "Kruskal", "graph_slider"),
]


@pytest.mark.parametrize("page,option,slider_key", STEP_CASES)
def test_every_step_renders(app, page, option, slider_key):
    at = open_page(app, page)
    if option:
        at.radio[0].set_value(option).run()
    total = at.slider(key=slider_key).max
    assert total > 1
    for step in sorted({1, 2, 3, total // 2, total - 1, total}):
        at.slider(key=slider_key).set_value(step).run()
        assert not at.exception, f"step {step} of {total}"
