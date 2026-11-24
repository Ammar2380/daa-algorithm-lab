"""sorting_visualizer.py - bars for one sorting step, with pointers above the active bars."""
import plotly.graph_objects as go

from visualizations.theme import PALETTE as P, style_figure

LEGEND = [(P["amber"], "comparing"), (P["rose"], "moved / swapped"), (P["blue"], "active range"),
          (P["emerald"], "final position"), (P["slate"], "untouched")]


def sorting_figure(step):
    arr = step["array"]
    n = len(arr)
    lo, hi = step["range"] if step.get("range") else (None, None)
    colors = []
    for i in range(n):
        if i in step["moved"]:
            colors.append(P["rose"])
        elif i in step["comparing"]:
            colors.append(P["amber"])
        elif i in step["sorted"]:
            colors.append(P["emerald"])
        elif lo is not None and lo <= i < hi:
            colors.append(P["blue"])
        else:
            colors.append(P["slate"])
    top = max(max(arr, default=1), 1)
    fig = go.Figure(go.Bar(x=list(range(n)), y=arr, marker=dict(color=colors, line=dict(width=0)),
                           text=arr if n <= 25 else None, textposition="outside",
                           textfont=dict(color=P["text"], size=12), cliponaxis=False,
                           hovertemplate="index %{x}: %{y}<extra></extra>"))
    try:                                              # rounded bar tops (newer Plotly only)
        fig.update_traces(marker_cornerradius=6)
    except ValueError:
        pass
    # pointer triangles above the bars that are being compared or moved
    pointers = [(i, P["rose"]) for i in step["moved"]] + [(i, P["amber"]) for i in step["comparing"]
                                                         if i not in step["moved"]]
    if pointers and top > 0:
        fig.add_trace(go.Scatter(x=[i for i, _ in pointers], y=[top * 1.22] * len(pointers), mode="markers",
                                 marker=dict(symbol="triangle-down", size=11, color=[c for _, c in pointers]),
                                 hoverinfo="skip"))
    style_figure(fig, height=370)
    fig.update_layout(showlegend=False, bargap=0.22, margin=dict(l=8, r=8, t=26, b=8))
    fig.update_xaxes(title_text="index", dtick=1 if n <= 25 else None, showgrid=False)
    fig.update_yaxes(range=[min(0, min(arr, default=0)) * 1.2, top * 1.32], showgrid=True, zeroline=True)
    return fig
