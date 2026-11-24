"""searching_visualizer.py - array cells with low / mid / high pointers and the search range."""
import plotly.graph_objects as go

from visualizations.theme import PALETTE as P, style_figure

LEGEND = [(P["amber"], "item being compared"), (P["emerald"], "found"),
          (P["slate"], "still possible"), (P["border"], "eliminated")]


def searching_figure(step, target, binary=True):
    arr = step["array"]
    n = len(arr)
    low, high, idx, found = step["low"], step["high"], step["index"], step["found"]
    colors = []
    for i in range(n):
        if found is not None and i == found:
            colors.append(P["emerald"])
        elif i == idx:
            colors.append(P["amber"])
        elif low <= i <= high:
            colors.append(P["slate"])
        else:
            colors.append(P["border"])                # outside the remaining search range
    text_colors = [P["bg"] if c in (P["amber"], P["emerald"]) else
                   (P["faint"] if c == P["border"] else P["text"]) for c in colors]
    fig = go.Figure(go.Bar(x=list(range(n)), y=[1] * n, marker=dict(color=colors, line=dict(width=0)),
                           text=[str(v) for v in arr], textposition="inside", insidetextanchor="middle",
                           textfont=dict(size=16 if n <= 20 else 11, color=text_colors),
                           hovertemplate="index %{x}: %{text}<extra></extra>"))
    try:
        fig.update_traces(marker_cornerradius=8)
    except ValueError:
        pass
    # pointer labels under the cells: Binary Search shows low / mid / high, Linear Search shows i
    labels = {}
    if binary:
        for pos, name in ((low, "low"), (high, "high")):
            if 0 <= pos < n:
                labels.setdefault(pos, []).append(name)
    if idx is not None:
        labels.setdefault(idx, []).insert(1 if binary and labels.get(idx) else 0, "mid" if binary else "i")
    for pos, names in labels.items():
        fig.add_annotation(x=pos, y=0, yshift=-22, text="▲<br>" + "/".join(names), showarrow=False,
                           font=dict(size=11, color=P["blue"]), align="center")
    style_figure(fig, height=250)
    fig.update_layout(showlegend=False, bargap=0.14, margin=dict(l=8, r=8, t=34, b=44),
                      title=dict(text=f"Target = {target}", x=0.01, font=dict(size=14, color=P["text"])))
    fig.update_yaxes(visible=False, range=[0, 1.05])
    fig.update_xaxes(title_text=None, dtick=1 if n <= 30 else None, showgrid=False)
    return fig

