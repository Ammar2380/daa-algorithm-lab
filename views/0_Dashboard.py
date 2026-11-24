"""Dashboard (home page): hero, statistics, category cards, highlights, complexity cheat sheet."""
from html import escape

import streamlit as st

from core.algorithm_registry import (CATEGORIES, count_implemented, count_total,
                                     get_algorithms_by_category)
from visualizations.layout import cheat_sheet, feature, section, stat_cards

# ------------------------------------------------------------------ hero
st.markdown(
    '<div class="hero"><span class="eyebrow">Design and Analysis of Algorithms</span>'
    '<h1>See how algorithms <span class="gradient-text">think, compare and scale.</span></h1>'
    '<p>An interactive lab for 16 classic algorithms. Run them on your own input, step through every comparison '
    'and table update, read the pseudocode and complexity, then measure real performance on your machine.</p></div>',
    unsafe_allow_html=True)
c1, c2, _ = st.columns([1.1, 1.4, 2.6])
with c1, st.container(key="cta-primary"):
    st.page_link("views/2_Sorting.py", label="Start with Sorting", icon=":material/play_arrow:")
with c2, st.container(key="cta-secondary"):
    st.page_link("views/7_Performance_Analyzer.py", label="Open Performance Analyzer", icon=":material/speed:")

# ------------------------------------------------------------------ statistics
st.write("")
stat_cards([
    ("Algorithms", count_total(), "implemented by hand", "blue"),
    ("Categories", len(CATEGORIES), "from searching to graphs", "violet"),
    ("Implemented & tested", f"{count_implemented()} / {count_total()}", "each has its own tests", "green"),
    ("Interactive modules", len(CATEGORIES) + 1, "6 visualizers + analyzer", "amber"),
])

# ------------------------------------------------------------------ categories
section("Algorithm categories", "Choose a module to open its visualizer, theory and source code.")
names = list(CATEGORIES)
for start in range(0, len(names), 3):
    for col, name in zip(st.columns(3), names[start:start + 3]):
        info, algos = CATEGORIES[name], get_algorithms_by_category(name)
        chips = "".join(f'<span class="chip">{escape(a.name.split(" (")[0])}</span>' for a in algos)
        with col:
            with st.container(border=True, key=f"card-{name.lower().replace(' ', '-')}"):
                st.markdown(f'<div class="cat-icon">{info["icon"]}</div><div class="cat-title">{escape(name)}</div>'
                            f'<div class="cat-desc">{escape(info["description"])}</div><div class="chips">{chips}</div>',
                            unsafe_allow_html=True)
                st.write("")
                st.page_link(info["page"], label=f"Open {name}", icon=":material/arrow_forward:")

# ------------------------------------------------------------------ highlights
section("What makes it different")
cols = st.columns(4)
features = [("🎬", "Step-by-step visualizer", "Reset, step, play and pause through every comparison, swap and table update."),
            ("📘", "Theory next to code", "Pseudocode, best / average / worst case and the real Python source of each algorithm."),
            ("⏱️", "Honest benchmarks", "Same input for every algorithm, repeated runs, median time. Measured live, never faked."),
            ("✅", "Verified correct", "Algorithms are cross-checked against brute force in an automated test suite.")]
for col, (icon, title, text) in zip(cols, features):
    with col, st.container(border=True, key=f"card-feature-{title.split()[0].lower()}"):
        feature(icon, title, text)

# ------------------------------------------------------------------ how it works
section("How to use it")
cols = st.columns(3)
steps = [("Pick an algorithm", "Open a category and choose an algorithm with the selector at the top."),
         ("Enter your own input", "Type numbers, matrices, strings or graph edges, or generate random data."),
         ("Watch and compare", "Play the visualization, read the analysis, then benchmark it in the Performance Analyzer.")]
for i, (col, (title, text)) in enumerate(zip(cols, steps), 1):
    col.markdown(f'<div class="feature"><div class="f-t"><span class="step-no">{i}</span>{escape(title)}</div>'
                 f'<div class="f-d">{escape(text)}</div></div>', unsafe_allow_html=True)

# ------------------------------------------------------------------ cheat sheet
section("Complexity cheat sheet", "Generated from the same documentation data that the algorithm pages use.")
cheat_sheet()
