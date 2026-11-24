"""graph_visualizer.py - draws graphs (Plotly) and Huffman trees (Matplotlib) in the shared theme."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx
import plotly.graph_objects as go

from visualizations.theme import PALETTE as P, style_figure

LEGENDS = {
    "traversal": [(P["amber"], "current"), (P["emerald"], "visited"), (P["blue"], "in queue / stack"),
                  (P["slate"], "not reached yet")],
    "dijkstra": [(P["amber"], "current vertex"), (P["emerald"], "settled"), (P["slate"], "unsettled"),
                 (P["blue"], "shortest path")],
    "kruskal": [(P["emerald"], "accepted edge"), (P["rose"], "rejected (would form a cycle)"),
                (P["amber"], "edge being examined"), (P["slate"], "not examined")],
}


def legend_items(kind):
    return LEGENDS["traversal" if kind in ("bfs", "dfs") else kind]


def graph_layout(vertices, edges, seed=7):
    G = nx.Graph()
    G.add_nodes_from(vertices)
    G.add_edges_from((u, v) for u, v, _ in edges)
    return nx.spring_layout(G, seed=seed, k=1.2 / max(len(vertices), 1) ** 0.5 + 0.1)


def _key(u, v):
    return frozenset((u, v))


def graph_figure(vertices, edges, pos, step=None, highlight_path=None):
    """Draw the graph. `step` supplies visited/current/frontier/tree_edges/accepted/... ."""
    step = step or {}
    tree = {_key(*e[:2]) for e in step.get("tree_edges", [])}
    tree |= {_key(*e[:2]) for e in step.get("accepted", [])}
    rejected = {_key(*e[:2]) for e in step.get("rejected", [])}
    cur_edge = step.get("current") if isinstance(step.get("current"), tuple) else None
    considered = step.get("considered")
    path_edges = {_key(a, b) for a, b in zip(highlight_path or [], (highlight_path or [])[1:])}
    fig = go.Figure()
    for u, v, w in edges:
        k = _key(u, v)
        color, width, dash = P["border_strong"], 2, "solid"
        if k in tree:
            color, width = P["emerald"], 5
        elif k in rejected:
            color, dash = P["rose"], "dot"
        if k in path_edges:
            color, width = P["blue"], 6
        if (cur_edge and k == _key(*cur_edge[:2])) or (considered and k == _key(*considered)):
            color, width = P["amber"], 5
        fig.add_trace(go.Scatter(x=[pos[u][0], pos[v][0]], y=[pos[u][1], pos[v][1]], mode="lines",
                                 line=dict(color=color, width=width, dash=dash), hoverinfo="skip"))
        fig.add_annotation(x=(pos[u][0] + pos[v][0]) / 2, y=(pos[u][1] + pos[v][1]) / 2, text=str(w),
                           showarrow=False, font=dict(size=11, color=P["text"]),
                           bgcolor=P["surface2"], bordercolor=P["border_strong"], borderwidth=1, borderpad=3)
    visited = set(step.get("visited", []))
    frontier = set(step.get("frontier", []))
    current = step.get("current") if not isinstance(step.get("current"), tuple) else None
    dist = step.get("dist")
    on_path = set(highlight_path or [])
    colors, labels, text_colors = [], [], []
    for v in vertices:
        if v == current:
            colors.append(P["amber"])
        elif v in on_path:
            colors.append(P["blue"])
        elif v in visited:
            colors.append(P["emerald"])
        elif v in frontier:
            colors.append(P["blue"])
        else:
            colors.append(P["slate"])
        text_colors.append(P["bg"] if colors[-1] in (P["amber"], P["emerald"]) else "#FFFFFF")
        if dist is not None:
            labels.append(f"{v}<br><span style='font-size:10px'>{'∞' if dist.get(v) is None else dist[v]}</span>")
        else:
            labels.append(str(v))
    fig.add_trace(go.Scatter(x=[pos[v][0] for v in vertices], y=[pos[v][1] for v in vertices],
                             mode="markers+text", text=labels, textposition="middle center",
                             marker=dict(size=46, color=colors, line=dict(color=P["bg"], width=3)),
                             textfont=dict(color=text_colors, size=13, family="Inter, sans-serif"),
                             hoverinfo="skip"))
    style_figure(fig, height=460)
    fig.update_layout(showlegend=False, margin=dict(l=8, r=8, t=8, b=8))
    fig.update_xaxes(visible=False, showgrid=False)
    fig.update_yaxes(visible=False, showgrid=False)
    return fig


def count_leaves(node):
    """Number of leaves of a Huffman tree (used to size the drawing)."""
    return 1 if node.is_leaf() else count_leaves(node.left) + count_leaves(node.right)


def huffman_tree_figure(root):
    """Draw a Huffman tree: leaves are spaced evenly, parents sit above their children."""
    positions, leaf_counter = {}, [0]

    def layout(node, depth):
        if node.is_leaf():
            x = leaf_counter[0]
            leaf_counter[0] += 1
        else:
            x = (layout(node.left, depth + 1) + layout(node.right, depth + 1)) / 2
        positions[id(node)] = (x, -depth)
        return x

    layout(root, 0)
    fig, ax = plt.subplots(figsize=(max(5, leaf_counter[0] * 0.95), 4))
    fig.patch.set_facecolor(P["surface"])
    ax.set_facecolor(P["surface"])
    ax.axis("off")

    def draw(node):
        x, y = positions[id(node)]
        for child, bit in ((node.left, "0"), (node.right, "1")):
            if child is not None:
                cx, cy = positions[id(child)]
                ax.plot([x, cx], [y, cy], color=P["border_strong"], linewidth=1.6, zorder=1)
                ax.text((x + cx) / 2 + 0.06, (y + cy) / 2, bit, color=P["amber"], fontsize=11,
                        ha="center", va="center", fontweight="bold")
                draw(child)
        label = f"'{node.char}'\n{node.freq}" if node.is_leaf() else str(node.freq)
        ax.scatter([x], [y], s=1100, color=P["emerald"] if node.is_leaf() else P["blue"], zorder=2,
                   edgecolors=P["surface"], linewidths=2)
        ax.text(x, y, label, color=P["bg"] if node.is_leaf() else "white", ha="center", va="center",
                fontsize=8, fontweight="bold", zorder=3)

    draw(root)
    ax.margins(0.12)
    fig.tight_layout()
    return fig
