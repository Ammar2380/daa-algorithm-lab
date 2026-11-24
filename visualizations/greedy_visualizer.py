"""greedy_visualizer.py - timeline for Activity Selection and stacked bars for Fractional Knapsack."""
import plotly.graph_objects as go

from visualizations.theme import PALETTE as P, style_figure

ACTIVITY_LEGEND = [(P["emerald"], "selected"), (P["rose"], "skipped (overlaps)"),
                   (P["slate"], "not examined yet"), (P["amber"], "current activity (outline)")]
KNAPSACK_LEGEND = [(P["emerald"], "weight taken"), (P["slate"], "weight left behind")]


def activity_figure(activities, step):
    sel, rej, cur = set(step["selected"]), set(step["rejected"]), step["current"]
    fig = go.Figure()
    for idx in step["order"]:
        s, f = activities[idx]
        color = P["emerald"] if idx in sel else P["rose"] if idx in rej else P["slate"]
        fig.add_trace(go.Bar(y=[f"Activity {idx}"], x=[max(f - s, 0.15)], base=[s], orientation="h",
                             marker=dict(color=color, line=dict(color=P["amber"] if idx == cur else color,
                                                               width=3 if idx == cur else 0)),
                             hovertemplate=f"Activity {idx}: {s} to {f}<extra></extra>", showlegend=False))
    style_figure(fig, height=max(260, 30 * len(step["order"]) + 90))
    fig.update_layout(margin=dict(l=8, r=8, t=8, b=8), bargap=0.3)
    fig.update_xaxes(title_text="time")
    fig.update_yaxes(autorange="reversed", showgrid=False)
    return fig


def knapsack_figure(items, step):
    fractions = {i: f for i, f in step["taken"]}
    labels = [f"Item {i}" for i in step["order"]]
    taken_w = [items[i][1] * fractions.get(i, 0) for i in step["order"]]
    left_w = [items[i][1] * (1 - fractions.get(i, 0)) for i in step["order"]]
    fig = go.Figure()
    fig.add_bar(y=labels, x=taken_w, name="weight taken", orientation="h", marker_color=P["emerald"])
    fig.add_bar(y=labels, x=left_w, name="weight left behind", orientation="h", marker_color=P["slate"])
    style_figure(fig, height=max(260, 30 * len(labels) + 90))
    fig.update_layout(barmode="stack", margin=dict(l=8, r=8, t=8, b=8), showlegend=False, bargap=0.3)
    fig.update_xaxes(title_text="weight")
    fig.update_yaxes(autorange="reversed", showgrid=False)
    return fig
