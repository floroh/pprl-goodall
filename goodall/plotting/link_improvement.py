from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from matplotlib.colors import to_rgba_array, to_rgb

def plotly_dual_axis(fig1, fig2, title="", y1="", y2=""):
    # Create subplot with secondary axis
    subplot_fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Put Dataframe in fig1 and fig2
    # fig1 = px.line(data1)
    # fig2 = px.line(data2)
    # Change the axis for fig2
    fig2.update_traces(yaxis="y2")

    # Add the figs to the subplot figure
    # subplot_fig.add_traces(fig1.data + fig2.data)
    subplot_fig.add_traces(fig1.data)
    subplot_fig.add_traces(fig2.data)

    # FORMAT subplot figure
    subplot_fig.update_layout(
        yaxis=dict(title=y1, range=[0.91, 0.96]), yaxis2=dict(title=y2, range=[0, 800])
    )
    subplot_fig.update_layout(xaxis=dict(title="Updated uncertain pairs in layer n=0"))

    # RECOLOR so as not to have overlapping colors
    # subplot_fig.for_each_trace(lambda t: t.update(line=dict(color=t.marker.color)))
    return subplot_fig


def plot_quality_history(
        df_report: pd.DataFrame,
        initial_score: float,
        optimal_initial_score: float,
        x_column: str = "#Improved",
        name_color: str = None,
        name_symbol: str = None
):
    x_vline = 5
    if x_column == "#Improved":
        x_vline = 500
        # x_column = "#Reviewed pairs in top layer"

    df = df_report[df_report["#Improved"] >= 0]

    # colors = px.colors.qualitative.D3
    colors = px.colors.qualitative.Set1
    # colors = px.colors.qualitative.Dark24
    # colors = px.colors.sequential.Viridis
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
                                         [n / (n_colors - 1) for n in range(n_colors)], colortype='tuple')
    if "F1-score-min" in df.columns and name_color is not None:
        traces = []
        # colors = (colors[1], colors[2], colors[3])  # For XOR
        colors = colors[:n_colors]
        markers = markers[:n_colors]
        # colors.reverse()
        # markers.reverse()
        for i, group in enumerate(groups):
            k = group[0]
            d = group[1]
            x = d[x_column].tolist()
            y = d["F1-score"].tolist()
            y_upper = d["F1-score-max"].tolist()
            y_lower = d["F1-score-min"].tolist()
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
        quality_history.update_layout()
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

    # quality_history.add_hline(
    #     y=optimal_initial_score, line=dict(color="Green", width=2, dash="dot")
    # )
    # quality_history.add_hline(y=initial_score, line=dict(color="Gray", width=2, dash="dot"))
    # quality_history.add_vline(x=x_vline, line=dict(color="Gray", width=2, dash="dot"))

    quality_history.update_layout(
        xaxis=dict(tickmode='array', tickvals=df[x_column].tolist(),
                   ticktext=df["#Improved"].tolist())
    )
    # fig_ppcr_counts = px.bar(df, xCol, "#PPCR")
    # dual = plotly_dual_axis(quality_history, fig_ppcr_counts, title="Quality history", y1="F1-score", y2="PPCR Counts")
    # return dual
    return quality_history
