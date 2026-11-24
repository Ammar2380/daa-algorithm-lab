"""Performance Analyzer: measured time and operation counts versus theory."""
import pandas as pd
import streamlit as st

from core.benchmark import SUITES, run_suite
from visualizations.layout import callout, page_header, section, stat_cards, stop_page
from visualizations.performance_charts import ops_chart, time_chart

page_header("⏱️", "Performance Analyzer",
            "Algorithms of the same category run on identical inputs. Each is timed several times and the "
            "median is reported. Every number is measured on your computer when you press the button.",
            tags=["Measured time", "Operation counts", "Theory vs experiment"])

suite_name = st.selectbox("Category", list(SUITES))
suite = SUITES[suite_name]
st.caption(suite.description)

with st.container(border=True):
    section("Benchmark settings")
    c1, c2, c3 = st.columns(3)
    scenario = c1.selectbox("Input scenario", suite.scenarios)
    repeats = c2.slider("Repetitions per measurement", 1, 15, 5)
    seed = c3.number_input("Random seed", 0, 10 ** 6, 42)
    size_text = st.text_input(f"Input sizes ({suite.size_label}), comma separated, max {suite.max_size}",
                              ", ".join(map(str, suite.default_sizes)))
    try:
        sizes = sorted({int(s) for s in size_text.replace(";", ",").split(",") if s.strip()})
        if not sizes:
            raise ValueError("Enter at least one size.")
        if sizes[0] < 1 or sizes[-1] > suite.max_size:
            raise ValueError(f"Sizes must be between 1 and {suite.max_size}.")
    except ValueError as e:
        st.error(f"Invalid sizes: {e}")
        stop_page()
    if suite_name == "Sorting" and sizes[-1] > 3000:
        st.warning("Insertion Sort is O(n^2); large sizes with many repetitions can take a while.")

    key = (suite_name, scenario, tuple(sizes), repeats, seed)
    run = st.button("▶ Run benchmark", type="primary")
if run:
    bar = st.progress(0.0, text="Running...")
    st.session_state["bench"] = (key, run_suite(suite, scenario, sizes, repeats, int(seed),
                                                progress=lambda f: bar.progress(f, text="Running...")))
    bar.empty()

stored = st.session_state.get("bench")
if not stored or stored[0][0] != suite_name:
    callout("Press Run benchmark to measure. Nothing is shown until you do, because nothing is pre-recorded.",
            "info", title="Ready")
    stop_page()
if stored[0] != key:
    st.warning("Settings changed since the last run - press Run benchmark to update. Showing the previous results.")
rows = stored[1]
df = pd.DataFrame(rows)

# ------------------------------------------------------------------ headline numbers (all computed from the rows)
largest = df[df["n"] == df["n"].max()]
fastest = largest.loc[largest["Median time (ms)"].idxmin()]
slowest = largest.loc[largest["Median time (ms)"].idxmax()]
fewest = largest.loc[largest["Total operations"].idxmin()]
ratio = slowest["Median time (ms)"] / fastest["Median time (ms)"] if fastest["Median time (ms)"] > 0 else float("nan")
section(f"Summary at the largest size (n = {int(df['n'].max())})")
stat_cards([
    ("Fastest", fastest["Algorithm"], f"{fastest['Median time (ms)']:.4f} ms (median)", "green"),
    ("Slowest", slowest["Algorithm"], f"{slowest['Median time (ms)']:.4f} ms (median)", "rose"),
    ("Slowest / fastest", f"{ratio:.1f}x" if ratio == ratio else "n/a", "ratio of median times", "amber"),
    ("Fewest operations", fewest["Algorithm"], f"{int(fewest['Total operations']):,} operations", "blue"),
])

tab_time, tab_ops, tab_table = st.tabs(["⏱  Execution time", "🔢  Operation counts", "📋  Results table"])
with tab_time:
    with st.container(border=True):
        o1, o2 = st.columns(2)
        log = o1.checkbox("Log-log scale (straight lines reveal polynomial growth)", value=False)
        theory_on = o2.checkbox("Show theoretical curve (dotted, scaled to the last measurement)", value=True)
        st.plotly_chart(time_chart(rows, suite.theory, log, theory_on), key="time_chart")
with tab_ops:
    with st.container(border=True):
        st.plotly_chart(ops_chart(rows, log), key="ops_chart")
with tab_table:
    st.dataframe(df.style.format({"Median time (ms)": "{:.4f}", "Min time (ms)": "{:.4f}"}), hide_index=True)
    st.download_button("⬇ Download CSV", df.to_csv(index=False), "benchmark_results.csv", "text/csv")

section("Theoretical versus experimental complexity")
stat_cards([(label, notation, None, "violet", True) for label, (notation, _) in suite.theory.items()])
callout("Theory counts basic steps and ignores constants; it describes how the cost grows with n. "
        "Experiments include constants, Python overhead, memory effects and timer noise, so small inputs can "
        "contradict the theory. Operation counts are exact and repeatable, so they follow the theory more cleanly "
        "than times. The dotted curves are scaled to touch the largest measurement: compare their shape, not their "
        "height. On a log-log chart, a straight line with slope k means time grows like n^k.",
        "info", title="How to read these charts")
if suite_name == "Divide and Conquer":
    callout("Strassen performs fewer multiplications, but it creates many small matrices and additions. In Python "
            "this overhead is large, so classical multiplication may still be faster at these sizes. Compare the "
            "operation counts to see the theoretical advantage.", "warning", title="Why Strassen may look slower")
