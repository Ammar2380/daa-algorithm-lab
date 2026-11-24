"""performance_charts.py - Plotly charts for benchmark results, in the shared theme."""
import plotly.graph_objects as go

from visualizations.theme import SERIES, style_figure


def _series(rows, label, key):
    pts = sorted((r["n"], r[key]) for r in rows if r["Algorithm"] == label)
    return [p[0] for p in pts], [p[1] for p in pts]


def _labels(rows):
    return list(dict.fromkeys(r["Algorithm"] for r in rows))


def time_chart(rows, theory=None, log_scale=False, show_theory=True):
    """Measured median time per algorithm; optional dotted theoretical curve scaled to pass
    through the measured value at the largest n (it shows the SHAPE of the growth only)."""
    fig = go.Figure()
    for i, label in enumerate(_labels(rows)):
        color = SERIES[i % len(SERIES)]
        xs, ys = _series(rows, label, "Median time (ms)")
        fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines+markers", name=label, legendgroup=label,
                                 line=dict(color=color, width=3), marker=dict(size=8, color=color),
                                 hovertemplate=f"{label}<br>n=%{{x}}<br>%{{y:.4f}} ms<extra></extra>"))
        if show_theory and theory and label in theory and len(xs) >= 2 and ys[-1] > 0:
            notation, fn = theory[label]
            c = ys[-1] / fn(xs[-1])
            fig.add_trace(go.Scatter(x=xs, y=[c * fn(x) for x in xs], mode="lines", legendgroup=label,
                                     line=dict(dash="dot", width=1.5, color=color), opacity=0.8,
                                     name=f"{label} - theory {notation}", hoverinfo="skip"))
    style_figure(fig, height=440, legend_bottom=True)
    fig.update_layout(xaxis_title="input size n", yaxis_title="median time (ms)",
                      margin=dict(l=8, r=8, t=16, b=8), hovermode="x unified")
    if log_scale:
        fig.update_xaxes(type="log")
        fig.update_yaxes(type="log")
    return fig


def ops_chart(rows, log_scale=False):
    fig = go.Figure()
    for i, label in enumerate(_labels(rows)):
        color = SERIES[i % len(SERIES)]
        xs, ys = _series(rows, label, "Total operations")
        fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines+markers", name=label,
                                 line=dict(color=color, width=3), marker=dict(size=8, color=color)))
    style_figure(fig, height=420, legend_bottom=True)
    fig.update_layout(xaxis_title="input size n", yaxis_title="operations (comparisons + swaps + other)",
                      margin=dict(l=8, r=8, t=16, b=8), hovermode="x unified")
    if log_scale:
        fig.update_xaxes(type="log")
        fig.update_yaxes(type="log")
    return fig
