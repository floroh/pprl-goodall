from typing import Any

import pandas as pd
from pandas import DataFrame
import plotly.express as px
import plotly.graph_objects as go

def grouped_figure(func, df: DataFrame, x_columns: list, y_col: str = None):
    rows = []
    for x_column in x_columns:
        for val in df[x_column].values:
            rows.append([val, x_column])
    grouped_df = pd.DataFrame(rows, columns=["x", "g"])
    return func(grouped_df, x="x", color="g")


def grouped_figure_x_y(func, df: DataFrame, x_col: str, y_columns: list):
    rows = []
    for y_column in y_columns:
        for index, row in df.iterrows():
            x_val = row[x_col]
            y_val = row[y_column]
            rows.append([x_val, y_val, y_column])
    grouped_df = pd.DataFrame(rows, columns=["x", "y", "g"])
    return func(grouped_df, x="x", y="y", color="g")

def get_box_plots(df: pd.DataFrame, x_col: Any, y_col: Any,
                  color_col: Any | None = None,
                  facet_col: Any | None = None,
                  color_discrete_sequence=None,
                  range_y: Any | None = None) -> go.Figure:
    fig = px.box(df, x=x_col, y=y_col, color=color_col, facet_col=facet_col,
                 color_discrete_sequence=color_discrete_sequence, range_y=range_y)
    return fig

def get_recall_precision_curve(df_thresholds: pd.DataFrame, color_col: str = "run_id"):
    fig = px.line(
        df_thresholds,
        x="recall",
        y="precision",
        color=color_col,
        symbol=color_col,
        markers=True,  # optional, show points
        hover_data=["threshold"]  # show threshold on hover
    )

    fig.update_layout(
        xaxis_title="Recall",
        yaxis_title="Precision",
        legend_title="Method",
        template="plotly_white"
    )
    return fig

def get_quality_metrics(df_thresholds: pd.DataFrame,
                        metrics: list[str] = ["recall", "precision", "F1-score"],
                        color_col: str = "run_id",
                        reference_thr_col: str | None = None,
                        range_x: list[float] = None,
                        range_y: list[float] = [-0.01, 1.03],
                        ):
    x_col = "threshold"
    if reference_thr_col:
        x_col = "threshold diff"
        df_thresholds[x_col] = df_thresholds["threshold"] - df_thresholds[reference_thr_col]
    df_thresholds = df_thresholds.sort_values(by=[color_col, x_col])
    # streamlit.dataframe(df_thresholds)
    fig = px.line(
        df_thresholds,
        x=x_col,
        y=metrics,
        color=color_col,
        symbol=color_col,
        range_x=range_x,
        range_y=range_y,
        markers=True,  # optional, show points
        hover_data=["threshold"]  # show threshold on hover
    )

    return fig