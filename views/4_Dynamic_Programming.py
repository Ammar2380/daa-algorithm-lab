"""Dynamic Programming page: Matrix Chain Multiplication and LCS."""
import streamlit as st

from algorithms.dynamic_programming import lcs, matrix_chain_order
from core.step_tracker import StepTracker
from core.validation import parse_number_list
from visualizations.dp_visualizer import LEGEND, dp_table, table_height
from visualizations.layout import (
    algorithm_picker, callout, complexity_strip, legend, page_header, result_card, section, step_banner, stop_page)
from visualizations.ui_components import show_algorithm_info, step_player

page_header("🧮", "Dynamic Programming",
            "Solve each overlapping subproblem once and store the answer in a table. "
            "Watch the table fill in, one cell at a time.")
name = algorithm_picker(["Matrix Chain Multiplication", "Longest Common Subsequence (LCS)"])
complexity_strip(name)
tab_viz, tab_learn = st.tabs(["▶  Visualizer", "📘  Learn"])

with tab_learn:
    show_algorithm_info(name)


def calculation_rows(detail):
    """Turn the recorded 'k=..: formula = cost' lines into table rows and mark the cheapest split."""
    rows, costs = [], []
    for line in detail:
        head, rest = line.split(": ", 1)
        formula, cost = rest.rsplit(" = ", 1)
        rows.append({"Split": head, "Calculation": formula, "Cost": int(cost)})
        costs.append(int(cost))
    if costs:
        rows[costs.index(min(costs))]["Best"] = "✓ minimum"
    return rows


with tab_viz:
    if name == "Matrix Chain Multiplication":
        st.latex(r"m[i][j]=\min_{i\le k<j}\left(m[i][k]+m[k+1][j]+p_{i-1}\,p_k\,p_j\right),\quad m[i][i]=0")
        with st.container(border=True):
            section("Input", "Dimensions p0, p1, ..., pn: matrix Ai has size p(i-1) x p(i). "
                             "Example: 30, 35, 15, 5, 10, 20, 25 means 6 matrices.")
            text = st.text_input("Dimensions", "30, 35, 15, 5, 10, 20, 25")
        try:
            dims = parse_number_list(text, allow_float=False, min_len=2, max_len=9)
            tracker = StepTracker()
            res = matrix_chain_order(dims, tracker)
        except ValueError as e:
            st.error(f"Invalid input: {e}")
            stop_page()
        n = len(dims) - 1
        labels = [f"A{i}" for i in range(1, n + 1)]

        with st.container(border=True):
            section("Visualization", "Cells are filled by increasing chain length.")
            legend(LEGEND)

            def render(i):
                step = tracker.steps[i]
                step_banner(i, len(tracker.steps), step["description"])
                st.dataframe(dp_table(step["table"], labels, labels, step["cell"]), height=table_height(n))
                if step.get("detail"):
                    st.markdown("**Intermediate calculations - every possible split k**")
                    st.dataframe(calculation_rows(step["detail"]), hide_index=True)

            step_player("mcm", len(tracker.steps), render, delay=0.8)

        section("Result")
        c1, c2 = st.columns(2)
        with c1:
            result_card("Minimum multiplications", res["min_cost"])
        with c2:
            result_card("Best parenthesization", res["parenthesization"])
        t1, t2 = st.columns(2)
        t1.markdown("**Final cost table m**")
        t1.dataframe([[res["m"][i][j] if j >= i else None for j in range(1, n + 1)] for i in range(1, n + 1)],
                     hide_index=True, height=table_height(n))
        t2.markdown("**Split table s (best k)**")
        t2.dataframe([[res["s"][i][j] if j > i else None for j in range(1, n + 1)] for i in range(1, n + 1)],
                     hide_index=True, height=table_height(n))
        callout("The table was filled by increasing chain length. Each cell reused two smaller, already-solved "
                "cells instead of recomputing them. That reuse is dynamic programming.", "info", title="What happened")
    else:
        st.latex(r"L[i][j]=\begin{cases}L[i-1][j-1]+1 & X_i=Y_j\\ \max(L[i-1][j],\,L[i][j-1]) & X_i\ne Y_j\end{cases}")
        with st.container(border=True):
            section("Input", "Two strings of at most 12 characters each.")
            c1, c2 = st.columns(2)
            x = c1.text_input("String X", "ABCBDAB")
            y = c2.text_input("String Y", "BDCABA")
        if len(x) > 12 or len(y) > 12:
            st.error("Please use strings of at most 12 characters for the step-by-step table.")
            stop_page()
        tracker = StepTracker()
        res = lcs(x, y, tracker)
        rows = ["0: ∅"] + [f"{i}: {c}" for i, c in enumerate(x, 1)]     # unique labels (letters can repeat)
        cols = ["0: ∅"] + [f"{j}: {c}" for j, c in enumerate(y, 1)]

        with st.container(border=True):
            section("Visualization", "A match extends the diagonal; otherwise the better of top / left is copied.")
            legend(LEGEND)

            def render(i):
                step = tracker.steps[i]
                step_banner(i, len(tracker.steps), step["description"])
                st.dataframe(dp_table(step["table"], rows, cols, step["cell"], step["path"]),
                             height=table_height(len(rows)))

            step_player("lcs", len(tracker.steps), render, delay=0.5)

        section("Result")
        c1, c2 = st.columns(2)
        with c1:
            result_card("LCS length", res["length"])
        with c2:
            result_card("One longest common subsequence", f"'{res['lcs']}'")
        callout("Every cell compares two characters. A match extends the diagonal value; otherwise the best of the "
                "top / left values is copied. Backtracking from the corner recovers the string.",
                "info", title="What happened")
