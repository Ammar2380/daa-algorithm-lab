"""Divide and Conquer page: Strassen's matrix multiplication."""
import numpy as np
import streamlit as st

from algorithms.divide_conquer import classical_matrix_multiply, next_power_of_two, strassen
from core.step_tracker import StepTracker
from core.validation import parse_matrix
from visualizations.layout import (
    callout, complexity_strip, matrix_table, page_header, result_card, section, stat_cards, step_banner,
    stop_page)
from visualizations.ui_components import show_algorithm_info, step_player

NAME = "Strassen's Matrix Multiplication"
page_header("🧩", "Divide and Conquer",
            "Split a problem into smaller parts, solve them, and combine the answers. "
            "Strassen multiplies matrices with 7 recursive products instead of 8.",
            tags=["Strassen's Matrix Multiplication"])
complexity_strip(NAME)
tab_viz, tab_learn = st.tabs(["▶  Visualizer", "📘  Learn"])

with tab_learn:
    show_algorithm_info(NAME)

with tab_viz:
    callout("Enter two square matrices of the same size (rows on separate lines, numbers separated by spaces). "
            "If the size is not a power of two (e.g. 3x3), zeros are added up to the next power of two and "
            "removed again from the final answer.", "info", title="Input rules")

    if "mat_a" not in st.session_state:
        st.session_state.mat_a = "1 2 3 4\n5 6 7 8\n9 10 11 12\n13 14 15 16"
        st.session_state.mat_b = "1 0 0 1\n0 1 1 0\n1 0 1 0\n0 1 0 1"

    def make_random():
        rng = np.random.default_rng()
        n = st.session_state.mat_n
        for key in ("mat_a", "mat_b"):
            m = rng.integers(0, 10, (n, n))
            st.session_state[key] = "\n".join(" ".join(map(str, row)) for row in m)

    with st.container(border=True):
        section("Input matrices")
        c1, c2 = st.columns(2)
        c1.text_area("Matrix A", key="mat_a", height=150)
        c2.text_area("Matrix B", key="mat_b", height=150)
        r1, r2 = st.columns([1, 3])
        r1.number_input("Random size", 1, 8, 4, key="mat_n")
        r2.write("")
        r2.write("")
        r2.button("🎲 Generate random matrices", on_click=make_random)

    try:
        A, B = parse_matrix(st.session_state.mat_a), parse_matrix(st.session_state.mat_b)
        if len(A) > 8:
            raise ValueError("Please use matrices up to 8x8 for the step-by-step view.")
        tracker = StepTracker()
        result = strassen(A, B, tracker)
    except (ValueError, TypeError) as e:
        st.error(f"Invalid input: {e}")
        stop_page()

    n = len(A)
    if next_power_of_two(n) != n:
        callout(f"Size {n}x{n} is not a power of two: padding to {next_power_of_two(n)}x{next_power_of_two(n)}.",
                "warning", title="Padding applied")

    with st.container(border=True):
        section("Recursion steps", "Shown for the first two recursion levels; deeper levels follow the same pattern.")

        def render(i):
            step = tracker.steps[i]
            step_banner(i, len(tracker.steps), step["description"])
            items = list(step["data"].items())
            for start in range(0, len(items), 4):
                for col, (title, matrix) in zip(st.columns(4), items[start:start + 4]):
                    with col:
                        matrix_table(matrix, title)

        step_player("strassen", len(tracker.steps), render, delay=1.2)

    section("Result", "C = A × B")
    matrix_table(result.tolist())
    classical = classical_matrix_multiply(A, B)
    if np.array_equal(result, classical):
        result_card("Verification", "Matches the classical multiplication",
                    "Strassen's result equals the classical triple-loop result.")
    else:
        result_card("Verification", "Mismatch with the classical result", "Please report this as a bug.", "error")
    stat_cards([("Multiplications (Strassen)", tracker.operations,
                 "counted on the padded size", "violet"),
                ("Multiplications (classical)", n ** 3, "n³ for the original size", "blue")])
