"""Sorting page: visualizer and a quick comparison of the four sorting algorithms."""
import random
import time

import streamlit as st

from algorithms.sorting import heap_sort, insertion_sort, merge_sort, quick_sort
from core.step_tracker import StepTracker
from core.validation import parse_number_list
from visualizations.layout import (
    algorithm_picker, callout, complexity_strip, legend, page_header, result_card, section, stat_cards, step_banner, stop_page)
from visualizations.sorting_visualizer import LEGEND, sorting_figure
from visualizations.ui_components import show_algorithm_info, step_player

page_header("📊", "Sorting Algorithms",
            "Arrange data in order. Watch elements being compared and moved, then compare four classic strategies.")
SORTS = {"Insertion Sort": insertion_sort, "Merge Sort": merge_sort,
         "Quick Sort": quick_sort, "Heap Sort": heap_sort}
name = algorithm_picker(list(SORTS))
complexity_strip(name)
tab_viz, tab_learn = st.tabs(["▶  Visualizer", "📘  Learn"])

with tab_learn:
    show_algorithm_info(name)

with tab_viz:
    if "sort_text" not in st.session_state:
        st.session_state.sort_text = "29, 10, 14, 37, 13, 5, 22, 8"

    def make_random():
        st.session_state.sort_text = ", ".join(
            str(random.randint(1, 99)) for _ in range(st.session_state.sort_n))

    with st.container(border=True):
        section("Input", "Numbers separated by commas (up to 40), or generate a random array.")
        left, right = st.columns([3, 1])
        left.text_input("Array", key="sort_text")
        right.number_input("Random size", 1, 40, 10, key="sort_n")
        right.button("🎲 Random array", on_click=make_random)

    try:
        data = parse_number_list(st.session_state.sort_text, max_len=40)
    except ValueError as e:
        st.error(f"Invalid array: {e}")
        stop_page()
    if not data:
        st.error("Please enter at least one number.")
        stop_page()

    tracker = StepTracker()
    result = SORTS[name](data, tracker)

    with st.container(border=True):
        section("Visualization", "Bars show the array; triangles mark the bars being compared or moved.")
        legend(LEGEND)

        def render(i):
            step = tracker.steps[i]
            st.plotly_chart(sorting_figure(step), key=f"sort_fig_{i}")
            step_banner(i, len(tracker.steps), step["description"])

        step_player("sort", len(tracker.steps), render, delay=0.5)

    section("Result")
    result_card("Sorted array", ", ".join(map(str, result)))
    stat_cards([("Comparisons", tracker.comparisons, None, "amber"),
                ("Swaps / moves", tracker.swaps, None, "rose"),
                ("Steps recorded", len(tracker.steps), None, "blue")])

    section("Compare all four on this array", "Same input for every algorithm; counts are exact.")
    rows = []
    for label, fn in SORTS.items():
        t = StepTracker(record_steps=False)
        start = time.perf_counter()
        fn(data, t)
        elapsed = (time.perf_counter() - start) * 1000
        rows.append({"Algorithm": label, "Comparisons": t.comparisons, "Swaps/moves": t.swaps,
                     "Time (ms, single run)": round(elapsed, 4)})
    st.dataframe(rows, hide_index=True)
    callout("Tiny arrays give noisy times. For fair timing on larger inputs with repeats, "
            "use the Performance Analyzer.", "info", title="Tip")
    st.page_link("views/7_Performance_Analyzer.py", label="Open Performance Analyzer", icon=":material/speed:")
