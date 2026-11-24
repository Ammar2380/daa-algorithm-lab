"""
ui_components.py - Streamlit pieces shared by all pages:
  * show_algorithm_info(name)  -> the 'Learn' tabs of the Algorithm Explorer
  * step_player(...)           -> Reset / Prev / Next / Play / Pause controls + step slider
"""
import importlib
import inspect
import time

import streamlit as st

from core.complexity import ALGORITHM_INFO
from visualizations.graph_visualizer import count_leaves, huffman_tree_figure
from visualizations.layout import callout


def show_algorithm_info(name):
    """The 'Learn' content for one algorithm: overview, steps, pseudocode, complexity, source, example."""
    info = ALGORITHM_INFO[name]
    tabs = st.tabs(["Overview", "How it works", "Pseudocode", "Complexity", "Python code", "Example"])
    with tabs[0]:
        callout(info["problem"], "info", title="Problem")
        callout(info["input_output"], "info", title="Input and output")
        callout(info["application"], "info", title="Real-world use")
    with tabs[1]:
        for i, step in enumerate(info["how_it_works"], 1):
            st.markdown(f"**{i}.** {step}")
    with tabs[2]:
        st.code(info["pseudocode"], language="text")
    with tabs[3]:
        st.markdown(f"- **Best case:** {info['best']}\n- **Average case:** {info['average']}\n"
                    f"- **Worst case:** {info['worst']}\n- **Auxiliary space:** {info['space']}")
        callout(info["notes"], "info", title="Analysis notes")
    with tabs[4]:
        module_name, func_name = info["function"].rsplit(".", 1)
        func = getattr(importlib.import_module(module_name), func_name)
        st.caption(f"`{info['function']}` in `{module_name.replace('.', '/')}.py`")
        st.code(inspect.getsource(func), language="python")
    with tabs[5]:
        callout(info["example"], "info", title="Worked example")


def step_player(key, total, render, delay=0.8):
    """Show step controls and call render(index) to draw the chosen step (index is 0-based).

    Reset/Prev/Next change the slider. Play runs through the remaining steps automatically;
    pressing Pause (or touching any widget) stops it at the current step; Play again resumes from there.
    The slider is 1-based (Step 1 ... Step N) so it matches the "Step n of N" banner.
    """
    if total <= 0:
        st.warning("There are no steps to show.")
        return
    slider_key, pending_key, play_key = f"{key}_slider", f"{key}_pending", f"{key}_play"
    if pending_key in st.session_state:                  # apply position saved by a previous Play
        st.session_state[slider_key] = st.session_state.pop(pending_key) + 1
    st.session_state[slider_key] = min(max(st.session_state.get(slider_key, 1), 1), total)

    def go_to(pos):
        st.session_state[slider_key] = pos

    def go_next():
        st.session_state[slider_key] = min(st.session_state[slider_key] + 1, total)

    def go_prev():
        st.session_state[slider_key] = max(st.session_state[slider_key] - 1, 1)

    def start_play():
        st.session_state[play_key] = True

    with st.container(key=f"{key}_controls"):          # styled as a compact, wrapping toolbar (style.css)
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.button("⏮ Reset", key=f"{key}_reset", on_click=go_to, args=(1,))
        c2.button("◀ Prev", key=f"{key}_prev", on_click=go_prev)
        c3.button("Next ▶", key=f"{key}_next", on_click=go_next)
        c4.button("▶ Play / Resume", key=f"{key}_playbtn", on_click=start_play)
        c5.button("⏸ Pause", key=f"{key}_pause")
    idx = (st.slider("Step", 1, total, key=slider_key) - 1) if total > 1 else 0
    area = st.empty()
    with area.container():
        render(idx)
    if st.session_state.pop(play_key, False):
        start = 0 if idx >= total - 1 else idx + 1
        for i in range(start, total):
            st.session_state[pending_key] = i
            with area.container():
                render(i)
            time.sleep(delay)
        st.session_state[pending_key] = total - 1
        st.rerun()


def show_huffman_tree(root):
    """Draw a Huffman tree centred, with a width that grows with the number of leaves."""
    share = min(1.0, max(0.35, count_leaves(root) / 9))
    side = (1 - share) / 2
    columns = st.columns([side, share, side]) if side > 0 else [None, st.container(), None]
    with columns[1]:
        st.pyplot(huffman_tree_figure(root))
