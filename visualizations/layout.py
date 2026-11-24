"""
layout.py - reusable UI components (Streamlit) used by every page.

Pages never write HTML or CSS themselves; they call these functions, so the whole app
looks consistent and a design change is made in one place.
All dynamic text is HTML-escaped before it is placed inside markup.
"""
from html import escape
from pathlib import Path

import streamlit as st

from core.complexity import ALGORITHM_INFO
from visualizations.theme import FONT_STACK, MONO_STACK, PALETTE

ASSETS = Path(__file__).resolve().parent.parent / "assets"
_e = escape


def _html(markup):
    st.markdown(markup, unsafe_allow_html=True)


# ------------------------------------------------------------------ theme / chrome
def inject_theme():
    """Load assets/style.css once per run, with the palette injected as CSS variables."""
    variables = "".join(f"--{k}:{v};" for k, v in PALETTE.items())
    css = (f":root{{{variables}--font:{FONT_STACK};--mono:{MONO_STACK};}}\n"
           + (ASSETS / "style.css").read_text(encoding="utf-8"))
    _html(f"<style>{css}</style>")


def stop_page():
    """Use instead of st.stop() inside pages: draws the footer first.
    (Streamlit renders nothing after st.stop(), so a try/finally in app.py cannot do this.)"""
    footer()
    st.stop()


def sidebar_extras():
    _html('<div class="side-card"><b>How to use</b><br>Pick an algorithm, read the <b>Learn</b> tab, '
          'then press <b>Play</b> in the Visualizer to watch it run step by step.</div>')
    _html('<div class="side-card">Every number in the Performance Analyzer is measured live '
          'on your computer. Nothing is pre-recorded.</div>')


def footer():
    _html('<div class="app-footer"><span><b>DAA Algorithm Lab</b> · Design and Analysis of Algorithms project</span>'
          '<span>Python · Streamlit · Plotly · NetworkX · NumPy</span></div>')


# ------------------------------------------------------------------ headings
def page_header(icon, title, subtitle, tags=()):
    chips = "".join(f'<span class="chip">{_e(t)}</span>' for t in tags)
    _html(f'<div class="page-header"><div class="ph-row"><div class="ph-icon">{icon}</div><h1>{_e(title)}</h1></div>'
          f'<p class="ph-sub">{_e(subtitle)}</p>{chips}</div>')


def section(title, caption=None):
    cap = f'<div class="st-c">{_e(caption)}</div>' if caption else ""
    _html(f'<div class="section-title"><div class="st-t">{_e(title)}</div>{cap}</div>')


# ------------------------------------------------------------------ cards and callouts
def stat_cards(items):
    """items: list of (label, value) or (label, value, hint) or (label, value, hint, tone[, mono])."""
    cards = []
    for item in items:
        label, value = item[0], item[1]
        hint = item[2] if len(item) > 2 else None
        tone = item[3] if len(item) > 3 else ""
        mono = " mono" if len(item) > 4 and item[4] else ""
        hint_html = f'<div class="stat-hint">{_e(str(hint))}</div>' if hint else ""
        cards.append(f'<div class="stat-card tone-{tone}"><div class="stat-label">{_e(str(label))}</div>'
                     f'<div class="stat-value{mono}">{_e(str(value))}</div>{hint_html}</div>')
    _html(f'<div class="stat-grid">{"".join(cards)}</div>')


def _split(text, seps=(" - ", "; ", " (", " for ")):
    """'O(1) - target is first' -> ('O(1)', 'target is first')"""
    for sep in seps:
        if sep in text:
            head, tail = text.split(sep, 1)
            return head, (tail.rstrip(")") if sep in (" (", " for ") else tail)
    if "), " in text:                       # 'O(n + k log k), k = distinct characters'
        head, tail = text.split("), ", 1)
        return head + ")", tail
    return text, ""


def complexity_strip(name):
    """Best / average / worst time and auxiliary space of an algorithm, as four cards."""
    info = ALGORITHM_INFO[name]
    cards = []
    for label, key, tone in (("Best case", "best", "green"), ("Average case", "average", "blue"),
                             ("Worst case", "worst", "rose"), ("Auxiliary space", "space", "violet")):
        value, hint = _split(info[key])
        cards.append((label, value, hint, tone, True))
    stat_cards(cards)


def callout(text, kind="info", title=None):
    titles = {"info": "Info", "success": "Success", "warning": "Note", "error": "Problem"}
    _html(f'<div class="callout {kind}"><div><div class="co-title">{_e(title or titles[kind])}</div>'
          f'<div class="co-body">{_e(text)}</div></div></div>')


def step_banner(index, total, text):
    callout(text, "info", title=f"Step {index + 1} of {total}")


def result_card(title, value, detail=None, kind="success"):
    d = f'<div class="rc-detail">{_e(detail)}</div>' if detail else ""
    _html(f'<div class="result-card {kind}"><div class="rc-title">{_e(title)}</div>'
          f'<div class="rc-value">{_e(str(value))}</div>{d}</div>')


def legend(items):
    """items: list of (hex_colour, label)."""
    _html('<div class="legend">' + "".join(
        f'<span class="legend-item"><i style="background:{c}"></i>{_e(l)}</span>' for c, l in items) + "</div>")


def feature(icon, title, text):
    _html(f'<div class="feature"><div class="f-ico">{icon}</div><div class="f-t">{_e(title)}</div>'
          f'<div class="f-d">{_e(text)}</div></div>')


def cheat_sheet():
    """Complexity table of all algorithms, generated from core/complexity.py."""
    rows = []
    for info in ALGORITHM_INFO.values():
        cells = "".join(f'<td class="mono">{_e(_split(info[k])[0])}</td>' for k in ("best", "average", "worst", "space"))
        rows.append(f'<tr><td>{_e(info["name"])}</td><td class="cat">{_e(info["category"])}</td>{cells}</tr>')
    _html('<div class="table-wrap"><table class="cheat"><thead><tr><th>Algorithm</th><th>Category</th><th>Best</th>'
          f'<th>Average</th><th>Worst</th><th>Space</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>')


def _fmt(value):
    return f"{value:g}" if isinstance(value, float) else str(value)


def matrix_table(matrix, title=None):
    """A matrix drawn with brackets (no row/column headers, unlike a spreadsheet table)."""
    rows = "".join("<tr>" + "".join(f"<td>{_e(_fmt(v))}</td>" for v in row) + "</tr>" for row in matrix)
    heading = f'<div class="mx-title">{_e(title)}</div>' if title else ""
    _html(f'<div class="mx-wrap">{heading}<table class="mx">{rows}</table></div>')


def algorithm_picker(options, label="Algorithm", key=None):
    """Segmented-pill selector (a styled st.radio)."""
    return st.radio(label, options, horizontal=True, key=key, label_visibility="collapsed")
