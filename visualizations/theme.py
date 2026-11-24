"""
theme.py - the ONE place where the design palette lives (no Streamlit code here).

* PALETTE feeds both the CSS (as :root variables, see layout.inject_theme) and every chart.
* style_figure() gives all Plotly charts the same premium dark look.
"""

PALETTE = {
    "bg": "#0B1020",          # app background (deep navy)
    "sidebar": "#0D1328",
    "surface": "#111833",     # cards
    "surface2": "#161F3F",    # raised / hover
    "border": "#232C4D",
    "border_strong": "#33406B",
    "text": "#E8ECF8",
    "muted": "#8D97B8",
    "faint": "#5C6684",
    "blue": "#5B8CFF",        # primary accent
    "violet": "#8B6CF6",      # secondary accent
    "amber": "#F5B83D",       # comparing / current
    "rose": "#F2566B",        # swapped / rejected
    "emerald": "#34D399",     # done / selected / found
    "slate": "#4B5675",       # neutral bars
    "cyan": "#38BDF8",
}

# Colours of the algorithm series in comparison charts
SERIES = [PALETTE["blue"], PALETTE["violet"], PALETTE["emerald"], PALETTE["amber"],
          PALETTE["rose"], PALETTE["cyan"]]

FONT_STACK = "Inter, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
MONO_STACK = "'JetBrains Mono', 'Fira Code', Consolas, Menlo, monospace"


def rgba(hex_color, alpha):
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


def style_figure(fig, height=None, legend_bottom=False):
    """Apply the shared dark look to any Plotly figure and return it."""
    p = PALETTE
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family=FONT_STACK, color=p["muted"], size=12),
        colorway=SERIES,
        hoverlabel=dict(bgcolor=p["surface2"], bordercolor=p["border_strong"],
                        font=dict(family=FONT_STACK, color=p["text"])),
        legend=dict(font=dict(color=p["text"], size=12), bgcolor="rgba(0,0,0,0)",
                    **(dict(orientation="h", y=-0.28, x=0) if legend_bottom else {})),
        title=dict(font=dict(color=p["text"], size=14)),
    )
    if height:
        fig.update_layout(height=height)
    fig.update_xaxes(gridcolor=p["border"], zerolinecolor=p["border"], linecolor=p["border"],
                     tickfont=dict(color=p["muted"]), title_font=dict(color=p["muted"], size=12))
    fig.update_yaxes(gridcolor=p["border"], zerolinecolor=p["border"], linecolor=p["border"],
                     tickfont=dict(color=p["muted"]), title_font=dict(color=p["muted"], size=12))
    return fig
