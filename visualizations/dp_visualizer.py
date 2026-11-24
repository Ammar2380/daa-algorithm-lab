"""dp_visualizer.py - DP tables as styled pandas Stylers (shown with st.dataframe)."""
import pandas as pd

from visualizations.theme import PALETTE as P, rgba

LEGEND = [(P["amber"], "cell being computed"), (rgba(P["blue"], 0.55), "already computed"),
          (P["emerald"], "backtracking path")]


def table_height(n_rows):
    """Pixel height that shows all rows without an inner scrollbar."""
    return 38 + 35 * n_rows


def dp_table(table, row_labels, col_labels, cell=None, path=None):
    """Return a Styler. Computed cells are tinted blue, the cell being updated is amber,
    backtrack-path cells are green. Empty cells have not been computed yet."""
    df = pd.DataFrame(table, index=row_labels, columns=col_labels, dtype=object)   # object: keep ints as ints
    df = df.map(lambda v: "" if v is None or pd.isna(v) else str(v))
    path = set(path or [])

    def style(frame):
        css = pd.DataFrame("", index=frame.index, columns=frame.columns)
        for r in range(frame.shape[0]):
            for c in range(frame.shape[1]):
                if frame.iloc[r, c] != "":
                    css.iloc[r, c] = (f"background-color:{rgba(P['blue'], 0.16)};color:{P['text']};"
                                      "text-align:center")
                else:
                    css.iloc[r, c] = f"color:{P['faint']};text-align:center"
        for (r, c) in path:
            css.iloc[r, c] = f"background-color:{P['emerald']};color:{P['bg']};font-weight:700;text-align:center"
        if cell is not None:
            css.iloc[cell[0], cell[1]] = (f"background-color:{P['amber']};color:{P['bg']};"
                                          "font-weight:700;text-align:center")
        return css

    return df.style.apply(style, axis=None)
