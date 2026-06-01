import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from matplotlib.colors import to_rgb

def to_py_numeric_list(series):
    return [int(v) if isinstance(v, np.integer)
            else float(v) if isinstance(v, np.floating)
            else v for v in series]


def plot_quality_history(
    df_report: pd.DataFrame,
    initial_score: float = None,
    optimal_initial_score: float = None,
    x_column: str = "#Improved",
    name_color: str = None,
    name_symbol: str = None,
    reverse_colors: bool = False,
    skip_first_color: bool = False,
    x_vline: int = -1
):
    if x_vline < 0:
        x_vline = 5
        if x_column == "#Improved":
            x_vline = 500

    # Remove special results (ideal initial threshold)
    df = df_report[df_report["#Improved"] >= 0]

    colors = px.colors.qualitative.Set1
    markers = ["circle", "square", "diamond", "cross", "x", "triangle-up", "triangle-down", "triangle-left"]
    group_by_columns = []
    if name_color is not None and name_symbol is not None:
        group_by_columns = [name_color, name_symbol]
    elif name_color is not None:
        group_by_columns = [name_color]
    n_colors = 1
    if len(group_by_columns) != 0:
        groups = list(df.groupby(group_by_columns))
        n_colors = len(groups)
    if (name_color is not None and "Thr" in name_color) or n_colors > len(colors):
        colors = px.colors.sample_colorscale("Plasma",
                                         [n / max((n_colors - 1), 1) for n in range(n_colors)], colortype='tuple')
    # if "F1-score-min" in df.columns and name_color is not None:
    if name_color is not None:
        traces = []
        if skip_first_color:
            colors = colors[1:n_colors+1]  # For XOR
        else:
            colors = colors[:n_colors]
        markers = markers[:n_colors]
        if reverse_colors:
            colors.reverse()
            markers.reverse()
        for i, group in enumerate(groups):
            k = group[0]
            # k = k[::-1]  # Reverse tuple values for display in the legend
            d = group[1]
            x = to_py_numeric_list(d[x_column])
            y = to_py_numeric_list(d["F1-score"])
            fillcolor = colors[i]
            if isinstance(fillcolor, str) and fillcolor.startswith('#'):
                fillcolor = to_rgb(fillcolor)
            if isinstance(fillcolor, str) and fillcolor.startswith('rgb'):
                fillcolor = fillcolor
            else:
                fillcolor = 'rgb' + str(fillcolor)
            traces.append(go.Scatter(x=x, y=y,
                                     name=str(k),
                                     marker=dict(symbol=markers[i % len(markers)], size=8),
                                     line=dict(color=fillcolor),
                                     ))
            # fillcolor = str(to_rgb(colors[i])).replace(')', ', 0.3)')
            if "F1-score-min" in df.columns:
                y_upper = to_py_numeric_list(d["F1-score-max"])
                y_lower = to_py_numeric_list(d["F1-score-min"])
                fillcolor = fillcolor.replace(')', ', 0.3)')
                fillcolor = fillcolor.replace('rgb', 'rgba')
                traces.insert(0, go.Scatter(x=x + x[::-1], y=y_upper + y_lower[::-1],
                                            fill='toself',
                                            # fillcolor='rgba(0.0,0.0,1.0,0.5)',
                                            fillcolor=fillcolor,
                                            # fillcolor=fillcolor,
                                            line=dict(color='rgba(255,255,255,0)'),
                                            hoverinfo="skip",
                                            showlegend=False))
        quality_history = go.Figure(traces)
        # quality_history.update_layout()
    else:
        if name_color is not None and name_symbol is not None:
            quality_history = px.line(
                df,
                x=x_column,
                y="F1-score",
                color=name_color,
                symbol=name_symbol,
                markers=True
            )
        elif name_color is not None:
            quality_history = px.line(
                df, x=x_column, y="F1-score", color=name_color, markers=True
            )
        else:
            quality_history = px.line(
                df, x=x_column, y=["recall", "precision", "F1-score"], markers=True
            )

    quality_history.add_vline(x=x_vline, line=dict(color="Gray", width=2, dash="dot"))
    if initial_score:
        quality_history.add_hline(
            y=initial_score,
            line=dict(color="Grey", width=2, dash="dash"),
            annotation_text="Initial score",
            annotation_position="top left",
            annotation_font_size=12,
        )
    if optimal_initial_score:
        quality_history.add_hline(
            y=optimal_initial_score,
            line=dict(color="Green", width=2, dash="dash"),
            annotation_text="Optimal initial score",
            annotation_position="top left",
            annotation_font_size=12,
        )
    quality_history.update_layout(
        xaxis=dict(tickmode='array', tickvals=df[x_column].tolist(),
                   ticktext=df["#Improved"].tolist())
    )
    return quality_history
