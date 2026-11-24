"""Searching page: Linear Search and Binary Search."""
import random

import streamlit as st

from algorithms.searching import binary_search, is_sorted, linear_search
from algorithms.sorting import merge_sort
from core.step_tracker import StepTracker
from core.validation import parse_number_list
from visualizations.layout import (
    algorithm_picker, callout, complexity_strip, legend, page_header, result_card, section, stat_cards, step_banner, stop_page)
from visualizations.searching_visualizer import LEGEND, searching_figure
from visualizations.ui_components import show_algorithm_info, step_player

page_header("🔍", "Searching Algorithms",
            "Locate a target value in a collection. Compare checking every item with repeatedly halving a sorted array.")
name = algorithm_picker(["Linear Search", "Binary Search"])
complexity_strip(name)
tab_viz, tab_learn = st.tabs(["▶  Visualizer", "📘  Learn"])

with tab_learn:
    show_algorithm_info(name)

with tab_viz:
    if name == "Binary Search":
        callout("Binary Search requires a sorted array. It inspects the middle item and discards half of the "
                "array each time. On unsorted data it can discard the half that contains the target.",
                "warning", title="Requires sorted input")

    if "search_text" not in st.session_state:
        st.session_state.search_text = "2, 5, 8, 12, 16, 23, 38, 56, 72, 91"

    def make_random():
        st.session_state.search_text = ", ".join(
            str(random.randint(1, 99)) for _ in range(st.session_state.search_n))

    with st.container(border=True):
        section("Input", "Type numbers separated by commas, or generate a random array.")
        left, right = st.columns([3, 1])
        left.text_input("Array", key="search_text")
        right.number_input("Random size", 1, 40, 10, key="search_n")
        right.button("🎲 Random array", on_click=make_random)
        target = st.number_input("Target value", value=23, step=1)

    try:
        arr = parse_number_list(st.session_state.search_text, max_len=40)
    except ValueError as e:
        st.error(f"Invalid array: {e}")
        stop_page()
    if not arr:
        st.error("Please enter at least one number.")
        stop_page()

    if name == "Binary Search" and not is_sorted(arr):
        st.error("This array is NOT sorted, so Binary Search cannot be trusted on it.")
        if st.checkbox("Sort it first (using Merge Sort from this project)", value=True):
            arr = merge_sort(arr)
            callout(f"Sorted array: {arr}", "info", title="Sorted for you")
        else:
            stop_page()

    tracker = StepTracker()
    func = linear_search if name == "Linear Search" else binary_search
    result = func(arr, target, tracker)

    with st.container(border=True):
        section("Visualization", "Step through the search with the controls below.")
        legend(LEGEND)

        def render(i):
            step = tracker.steps[i]
            st.plotly_chart(searching_figure(step, target, binary=(name == "Binary Search")),
                            key=f"search_fig_{i}")
            step_banner(i, len(tracker.steps), step["description"])

        step_player("search", len(tracker.steps), render)

    section("Result")
    if result == -1:
        result_card("Search result", f"{target} was not found", "Every possible position was ruled out.", "warning")
    else:
        result_card("Search result", f"{target} found at index {result}")
    stat_cards([("Comparisons made", tracker.comparisons, None, "amber"), ("Array size n", len(arr), None, "blue")])
    callout(f"{name} compared the target with {tracker.comparisons} item(s). " + (
        "Linear Search checks items from left to right, so the work grows in step with n."
        if name == "Linear Search" else
        "Binary Search halves the range each time, so about log2(n) comparisons are enough."),
        "info", title="What happened")
