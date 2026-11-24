"""Graph page: BFS, DFS, Dijkstra, Kruskal."""
import json
from pathlib import Path

import streamlit as st

from algorithms.graph_algorithms import (INF, bfs, build_adjacency, dfs, dijkstra, kruskal,
                                         shortest_path)
from core.step_tracker import StepTracker
from core.validation import parse_edges, parse_vertices
from visualizations.graph_visualizer import graph_figure, graph_layout, legend_items
from visualizations.layout import (
    algorithm_picker, complexity_strip, legend, page_header, result_card, section, step_banner, stop_page)
from visualizations.ui_components import show_algorithm_info, step_player

page_header("🕸️", "Graph Algorithms",
            "Traverse networks, find shortest paths and build minimum spanning trees on predefined or custom graphs.")
NAMES = {"BFS": "Breadth-First Search (BFS)", "DFS": "Depth-First Search (DFS)",
         "Dijkstra": "Dijkstra's Shortest Path", "Kruskal": "Kruskal's Minimum Spanning Tree"}
choice = algorithm_picker(list(NAMES))
complexity_strip(NAMES[choice])
tab_viz, tab_learn = st.tabs(["▶  Visualizer", "📘  Learn"])

with tab_learn:
    show_algorithm_info(NAMES[choice])

with tab_viz:
    SAMPLES = json.loads((Path(__file__).resolve().parent.parent / "data" / "sample_graphs.json").read_text())
    with st.container(border=True):
        section("Graph", "Use a predefined graph or create your own with weighted edges.")
        source = st.radio("Graph source", ["Predefined graph", "Create my own"], horizontal=True)
        if source == "Predefined graph":
            gname = st.selectbox("Predefined graph", list(SAMPLES))
            vertices = SAMPLES[gname]["vertices"]
            edges = [tuple(e) for e in SAMPLES[gname]["edges"]]
        else:
            c1, c2 = st.columns(2)
            vtext = c1.text_input("Vertices (separated by commas)", "A, B, C, D")
            etext = c2.text_area("Weighted edges, one per line: u v weight", "A B 4\nA C 2\nB C 1\nC D 7", height=130)
            try:
                vertices = parse_vertices(vtext)
                if not 1 <= len(vertices) <= 20:
                    raise ValueError("Use between 1 and 20 vertices.")
                edges = parse_edges(etext)
                build_adjacency(vertices, edges)            # validates the graph
            except ValueError as e:
                st.error(f"Invalid graph: {e}")
                stop_page()
        adj = build_adjacency(vertices, edges)
        pos = graph_layout(vertices, edges)
        start = None
        if choice != "Kruskal":
            start = st.selectbox("Start vertex", vertices)

    tracker = StepTracker()
    try:
        if choice == "BFS":
            result = bfs(adj, start, tracker)
        elif choice == "DFS":
            result = dfs(adj, start, tracker)
        elif choice == "Dijkstra":
            result = dijkstra(adj, start, tracker)
        else:
            result = kruskal(vertices, edges, tracker)
    except ValueError as e:
        st.error(str(e))
        stop_page()

    with st.container(border=True):
        section("Visualization", "Step through the algorithm and watch the graph change.")
        legend(legend_items(choice.lower()))

        def render(i):
            step = tracker.steps[i]
            st.plotly_chart(graph_figure(vertices, edges, pos, step), key=f"graph_fig_{i}")
            step_banner(i, len(tracker.steps), step["description"])
            if choice in ("BFS", "DFS"):
                label = "Queue" if choice == "BFS" else "Current path (stack)"
                st.caption(f"Visited: {step['visited']}   ·   {label}: {step['frontier']}")

        if not tracker.steps:
            st.warning("Nothing to show: the graph has no steps.")
        else:
            step_player("graph", len(tracker.steps), render)

    section("Result")
    if choice in ("BFS", "DFS"):
        result_card("Visiting order", " → ".join(map(str, result)))
        unreached = [v for v in vertices if v not in result]
        if unreached:
            st.warning(f"Not reachable from {start} (disconnected graph): {unreached}")
    elif choice == "Dijkstra":
        dist = result["dist"]
        st.dataframe([{"Vertex": v, "Distance": "∞ (unreachable)" if d == INF else d,
                       "Path": " → ".join(map(str, shortest_path(result["prev"], start, v))) or "-"}
                      for v, d in dist.items()], hide_index=True)
        target = st.selectbox("Highlight the shortest path to", vertices, index=len(vertices) - 1)
        path = shortest_path(result["prev"], start, target)
        if path:
            with st.container(border=True):
                st.plotly_chart(graph_figure(vertices, edges, pos, tracker.steps[-1], path), key="dijkstra_path")
        else:
            st.warning(f"{target} cannot be reached from {start}.")
    else:
        result_card("Total MST weight", result["total_weight"], f"{len(result['mst_edges'])} edges selected")
        st.dataframe([{"Edge": f"{u} - {v}", "Weight": w} for u, v, w in result["mst_edges"]], hide_index=True)
        if not result["connected"]:
            st.warning("The graph is disconnected, so the result is a minimum spanning FOREST (one tree per component).")
