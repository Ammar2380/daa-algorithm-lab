"""Greedy page: Activity Selection, Fractional Knapsack, Huffman Coding."""
import streamlit as st

from algorithms.greedy import activity_selection, fractional_knapsack, huffman_coding, huffman_decode
from core.step_tracker import StepTracker
from core.validation import parse_rows
from visualizations.greedy_visualizer import (ACTIVITY_LEGEND, KNAPSACK_LEGEND, activity_figure,
                                              knapsack_figure)
from visualizations.layout import (
    algorithm_picker, callout, complexity_strip, legend, page_header, result_card, section, stat_cards, step_banner, stop_page)
from visualizations.ui_components import show_algorithm_info, show_huffman_tree, step_player

page_header("🎯", "Greedy Algorithms",
            "Make the best-looking choice at every step and build a global solution from local choices.")
name = algorithm_picker(["Activity Selection", "Fractional Knapsack", "Huffman Coding"])
complexity_strip(name)
tab_viz, tab_learn = st.tabs(["▶  Visualizer", "📘  Learn"])

with tab_learn:
    show_algorithm_info(name)

with tab_viz:
    if name == "Activity Selection":
        callout("Greedy rule: always pick the compatible activity that finishes first.", "info", title="Strategy")
        with st.container(border=True):
            section("Input", "One activity per line: start finish")
            text = st.text_area("Activities", "1 4\n3 5\n0 6\n5 7\n3 9\n5 9\n6 10\n8 11\n8 12\n2 14\n12 16", height=200)
        try:
            acts = parse_rows(text, 2, max_rows=20)
            if not acts:
                raise ValueError("Enter at least one activity.")
            tracker = StepTracker()
            res = activity_selection(acts, tracker)
        except ValueError as e:
            st.error(f"Invalid input: {e}")
            stop_page()

        with st.container(border=True):
            section("Visualization", "Activities are examined in order of finishing time.")
            legend(ACTIVITY_LEGEND)

            def render(i):
                step = tracker.steps[i]
                st.plotly_chart(activity_figure(acts, step), key=f"act_fig_{i}")
                step_banner(i, len(tracker.steps), step["description"])

            step_player("act", len(tracker.steps), render)
        section("Result")
        result_card(f"Selected {len(res['selected'])} activities",
                    ", ".join(f"#{i} ({acts[i][0]}-{acts[i][1]})" for i in res["selected"]))

    elif name == "Fractional Knapsack":
        callout("Greedy rule: take the items with the highest value / weight ratio first. Items may be split.",
                "info", title="Strategy")
        with st.container(border=True):
            section("Input", "One item per line: value weight")
            c1, c2 = st.columns([3, 1])
            text = c1.text_area("Items", "60 10\n100 20\n120 30", height=150)
            capacity = c2.number_input("Capacity", min_value=0.0, value=50.0)
        try:
            items = parse_rows(text, 2, max_rows=20)
            if not items:
                raise ValueError("Enter at least one item.")
            tracker = StepTracker()
            res = fractional_knapsack(items, capacity, tracker)
        except ValueError as e:
            st.error(f"Invalid input: {e}")
            stop_page()
        st.dataframe([{"Item": i, "Value": v, "Weight": w, "Value/Weight": round(v / w, 3)}
                      for i, (v, w) in enumerate(items)], hide_index=True)

        with st.container(border=True):
            section("Visualization", "Items are taken in order of value / weight ratio.")
            legend(KNAPSACK_LEGEND)

            def render(i):
                step = tracker.steps[i]
                st.plotly_chart(knapsack_figure(items, step), key=f"knap_fig_{i}")
                step_banner(i, len(tracker.steps), step["description"])
                if "remaining" in step:
                    stat_cards([("Remaining capacity", round(step["remaining"], 3), None, "blue"),
                                ("Value so far", round(step["total"], 3), None, "green")])

            step_player("knap", len(tracker.steps), render)
        section("Result")
        result_card("Maximum value", f"{res['total_value']:.3f}")
        st.dataframe([{"Item": i, "Fraction taken": round(f, 3)} for i, f in res["taken"]], hide_index=True)

    else:
        callout("The two least frequent nodes are merged repeatedly. Left edge = 0, right edge = 1.",
                "info", title="Strategy")
        with st.container(border=True):
            section("Input")
            text = st.text_input("Text to encode (up to 200 characters)", "abracadabra")
        if len(text) > 200:
            st.error("Please use at most 200 characters.")
            stop_page()
        try:
            tracker = StepTracker()
            res = huffman_coding(text, tracker)
        except ValueError as e:
            st.error(f"Invalid input: {e}")
            stop_page()

        with st.container(border=True):
            section("Visualization", "The min-heap shrinks as the two smallest nodes merge into one.")

            def render(i):
                step = tracker.steps[i]
                step_banner(i, len(tracker.steps), step["description"])
                st.markdown("**Nodes currently in the min-heap (frequency, label)**")
                st.dataframe([{"Frequency": f, "Node": lab} for f, lab in step["forest"]], hide_index=True)
                if "merged" in step:
                    show_huffman_tree(step["merged"])

            step_player("huff", len(tracker.steps), render, delay=1.0)

        section("Final Huffman tree and codes")
        with st.container(border=True):
            show_huffman_tree(res["tree"])
        st.dataframe([{"Character": repr(ch), "Frequency": res["freq"][ch], "Code": code, "Bits": len(code)}
                      for ch, code in sorted(res["codes"].items(), key=lambda kv: (len(kv[1]), kv[0]))],
                     hide_index=True)
        st.code(res["encoded"], language="text")
        saved = 100 * (1 - len(res["encoded"]) / (8 * len(text)))
        stat_cards([("Original (8 bits/char)", f"{8 * len(text)} bits", None, "blue"),
                    ("Encoded", f"{len(res['encoded'])} bits", None, "violet"),
                    ("Saved", f"{saved:.1f}%", None, "green")])
        if huffman_decode(res["encoded"], res["tree"]) == text:
            result_card("Verification", "Decoding the bits returns the original text")
        else:
            result_card("Verification", "Decode mismatch", None, "error")
