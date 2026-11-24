"""
app.py - entry point and router of the DAA Algorithm Lab.   Run:  streamlit run app.py

Owns everything shared by all pages: page configuration, theme, logo, sidebar navigation,
sidebar tips and the footer. The pages live in views/ (not pages/: that folder name triggers
Streamlit's legacy auto-navigation, which bypasses this router on direct URL loads).
"""
import streamlit as st

from visualizations.layout import ASSETS, footer, inject_theme, sidebar_extras

st.set_page_config(page_title="DAA Algorithm Lab", page_icon="🧪", layout="wide",
                   initial_sidebar_state="auto")
inject_theme()
st.logo(str(ASSETS / "logo.svg"), size="large")

navigation = st.navigation({
    "Overview": [
        st.Page("views/0_Dashboard.py", title="Dashboard", icon=":material/home:", default=True),
    ],
    "Algorithms": [
        st.Page("views/1_Searching.py", title="Searching", icon=":material/search:"),
        st.Page("views/2_Sorting.py", title="Sorting", icon=":material/sort:"),
        st.Page("views/3_Divide_Conquer.py", title="Divide and Conquer", icon=":material/grid_view:"),
        st.Page("views/4_Dynamic_Programming.py", title="Dynamic Programming", icon=":material/calculate:"),
        st.Page("views/5_Greedy.py", title="Greedy Algorithms", icon=":material/bolt:"),
        st.Page("views/6_Graph_Algorithms.py", title="Graph Algorithms", icon=":material/hub:"),
    ],
    "Analysis": [
        st.Page("views/7_Performance_Analyzer.py", title="Performance Analyzer", icon=":material/speed:"),
    ],
})

with st.sidebar:
    sidebar_extras()

navigation.run()
footer()              # pages that stop early call layout.stop_page(), which draws the footer itself
