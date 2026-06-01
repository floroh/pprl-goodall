from typing import Tuple

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pandas import DataFrame

from goodall.plotting.plotly_helper import get_recall_precision_curve, \
    get_quality_metrics
from goodall.result_analysis.project_metrics import METRIC_BLOCKING_PAIR_COUNT, \
    METRIC_BLOCKING_BLOCK_COUNT
from goodall.ui.components.mlflow.mlflow import get_df_thresholds


class MlflowResultRenderer:
    def __init__(self, df_dataset_runs: pd.DataFrame | None = None):
        super().__init__()
        self.df_dataset_runs = df_dataset_runs

    def join_dataset_name_if_possible(self, df_children: pd.DataFrame) -> pd.DataFrame:
        if self.df_dataset_runs is not None:
            df_children = pd.merge(df_children, self.df_dataset_runs[
                ["dataset_run_id", "dataset_name"]],
                                   how="left",
                                   left_on="params.dataset_run_id",
                                   right_on="dataset_run_id")
        return df_children


def group_and_aggregate(
        df_children: pd.DataFrame,
        group_by_tags: list[str],
        *,
        metrics_prefix: str = "metrics",
        metrics_aggregations: str | list[str] = "mean",
        non_metrics_aggregations: dict[str, str | list[str]] | None = None,
        show_dataframe: bool = True,
) -> pd.DataFrame:
    """
    Group a DataFrame and aggregate metric and non-metric columns.

    Parameters
    ----------
    df_children : pd.DataFrame
        Input DataFrame to be grouped and aggregated.
    group_by_tags : Sequence[str]
        Column names to group by.
    metrics_prefix : str, optional
        Prefix used to identify metric columns, by default "metrics".
    metrics_aggregations : str or Sequence[str], optional
        Aggregation function(s) applied to all metric columns,
        by default "mean".
    non_metrics_aggregations : Mapping[str, str | Sequence[str]] | None, optional
        Explicit aggregations for non-metric columns
        (e.g., {"status": "count"}), by default {"status": "count"}.
    show_dataframe : bool, optional
        Whether to display the resulting DataFrame using Streamlit,
        by default True.

    Returns
    -------
    pd.DataFrame
        Aggregated DataFrame.
    """

    if non_metrics_aggregations is None:
        non_metrics_aggregations = {"status": "count"}

    metric_columns = [
        col for col in df_children.columns if col.startswith(metrics_prefix)
    ]

    # Identify metric columns dynamically
    metric_columns: list[str] = [
        col for col in df_children.columns if col.startswith(metrics_prefix)
    ]
    non_numeric_metrics = [
        col for col in metric_columns
        if not pd.api.types.is_numeric_dtype(df_children[col])
    ]
    if non_numeric_metrics:
        st.info(f"Excluding non-numeric metric columns: {non_numeric_metrics}")
        metric_columns = [col for col in metric_columns if
                          col not in non_numeric_metrics]
    # Build aggregation dictionary
    aggregation_functions: dict[str, str | list[str]] = {
        **non_metrics_aggregations,
        **{col: metrics_aggregations for col in metric_columns},
    }

    grouped = (
        df_children
        .groupby(by=list(group_by_tags), dropna=False)
        .agg(aggregation_functions)
        .reset_index()
    )

    if show_dataframe:
        st.dataframe(grouped)

    return grouped


def parse_metrics_wide_to_long(df_children: pd.DataFrame) -> pd.DataFrame:
    df_long = pd.wide_to_long(df_children, "metrics", i="run_id",
                              j="metric_name", sep=".", suffix=".*")
    df_long = df_long.reset_index()
    df_long.rename(columns={"metrics": "metric"}, inplace=True)
    return df_long


def get_possible_and_default_metrics(possible_metrics: list[str],
                                     disabled_metrics: list[str] | None,
                                     disabled_metrics_search: list[str] | None) -> list[
    str]:
    if disabled_metrics_search:
        if not disabled_metrics:
            disabled_metrics = []
        found_matches = set()
        for metric_search_item in disabled_metrics_search:
            metric_matches = [m for m in possible_metrics if
                              metric_search_item in m]
            found_matches.update(metric_matches)
        disabled_metrics.extend(sorted(found_matches))
    if not disabled_metrics:
        disabled_metrics = ["runtime", "f1-score", "recall", "precision",
                            "AUC.noYaxisPt", METRIC_BLOCKING_PAIR_COUNT,
                            METRIC_BLOCKING_BLOCK_COUNT]
    default_metrics = [m for m in possible_metrics if m not in disabled_metrics]
    return default_metrics


def show_metric_correlation(df_wide: pd.DataFrame,
                            selected_metrics: list[str],
                            prefix: str = "metrics."):
    """
    Plot scatter plots of selected metrics vs a chosen reference metric.
    - df_wide: wide-format DataFrame where each metric column is named like f"{prefix}{metric_name}"
    - selected_metrics: iterable of plain metric names (no prefix)
    - prefix: column name prefix for metric columns, default "metrics."
    """
    selected_metrics = list(selected_metrics)  # ensure indexable/list

    if not selected_metrics:
        st.info("No metrics provided in selected_metrics.")
        return

    # Build mapping from plain name -> prefixed column name
    metric_to_col = {m: f"{prefix}{m}" for m in selected_metrics}

    # Determine which of the prefixed columns actually exist in the dataframe
    available = {m: col for m, col in metric_to_col.items() if
                 col in df_wide.columns}
    missing = [m for m in selected_metrics if
               metric_to_col[m] not in df_wide.columns]
    if missing:
        st.warning(
            f"The following selected metrics are not present and will be ignored: {missing}")

    if not available:
        st.error("None of the selected metrics are present in the dataframe.")
        return

    # Select reference metric (show plain names in the selectbox)
    options = [None] + list(available.keys())
    reference_metric = st.selectbox("Show metric correlation with this reference",
                                    options)

    if not reference_metric:
        return

    # If user picked a metric that somehow became unavailable, check again
    if reference_metric not in available:
        st.error(f"Reference metric '{reference_metric}' is not available.")
        return

    ref_col = available[reference_metric]

    # Build y metrics: exclude the reference and only keep available ones
    y_metrics_plain = [m for m in available.keys() if m != reference_metric]
    if not y_metrics_plain:
        st.info("No other selected metrics to compare to the reference.")
        return

    y_cols = [available[m] for m in y_metrics_plain]
    required_cols = [ref_col] + y_cols

    # Drop rows with NA in any required column
    df_filtered = df_wide[required_cols].dropna(how="any")
    if df_filtered.empty:
        st.warning(
            "No rows remain after dropping missing values for the selected/reference metrics.")
        return

    # Build plot: one trace per metric (plain name shown), include Pearson r in trace name
    fig = go.Figure()
    for m_plain, col in zip(y_metrics_plain, y_cols):
        try:
            r = df_filtered[ref_col].corr(df_filtered[col])
            r_str = f" (r={r:.2f})" if pd.notna(r) else ""
        except Exception:
            r_str = ""
        fig.add_trace(
            go.Scatter(
                x=df_filtered[ref_col],
                y=df_filtered[col],
                mode="markers",
                name=f"{m_plain}{r_str}",
                marker=dict(symbol="circle")
            )
        )

    fig.update_layout(
        title=f"Metrics vs {reference_metric}",
        xaxis_title=reference_metric,
        yaxis_title="Metric value",
        legend_title="Metric",
        template="plotly_white"
    )
    st.plotly_chart(fig)


def show_lq_plots(df_combined: pd.DataFrame, color_col: str):
    show_lq_for_each_dataset = st.toggle(
        "Show results for each dataset separately", True)
    show_metrics_vs_threshold = st.toggle("Show metrics vs threshold")
    align_plots_by_optimal_thr = None
    if show_metrics_vs_threshold:
        lq_metrics = ["F1-score", "recall", "precision"]
        selected_metrics = st.multiselect("Choose metrics", lq_metrics,
                                          default=lq_metrics)
        align_plots_by_optimal_thr = st.toggle(
            "Align x-axis based on optimal thr")

    reference_thr_col = "metrics.bestthr" if align_plots_by_optimal_thr else None
    if show_lq_for_each_dataset:
        expand_all = st.toggle("Expand all")
        for ds_name, df_ds in df_combined.groupby("tags.dataset.name"):
            with st.expander(f"Dataset: {ds_name}", expanded=expand_all):
                st.plotly_chart(
                    get_recall_precision_curve(df_ds, color_col))
                if show_metrics_vs_threshold:
                    for selected_metric in selected_metrics:
                        st.plotly_chart(get_quality_metrics(df_ds,
                                                            metrics=selected_metric,
                                                            color_col=color_col,
                                                            reference_thr_col=reference_thr_col))
    else:
        st.plotly_chart(
            get_recall_precision_curve(df_combined, color_col))
        if show_metrics_vs_threshold:
            for selected_metric in selected_metrics:
                st.plotly_chart(get_quality_metrics(df_combined,
                                                    metrics=selected_metric,
                                                    color_col=color_col,
                                                    reference_thr_col=reference_thr_col))


def show_r_p_curve(df_children: pd.DataFrame, grouping_col: str):
    show_r_p_curve = st.toggle("Show Recall-Precision curve")
    if show_r_p_curve:
        run_ids = df_children["run_id"].unique().tolist()
        df_thresholds = get_df_thresholds(run_ids)
        df_thresholds_indexed = df_thresholds.set_index("run_id")
        df_children_indexed = df_children.set_index("run_id")
        df_combined = df_children_indexed.join(df_thresholds_indexed,
                                               on="run_id",
                                               how="inner")
        df_combined = df_combined.sort_values(by=[grouping_col, "recall"],
                                              ascending=[True, True])

        if st.toggle("Show result table for all thresholds"):
            st.dataframe(df_combined)
        show_lq_plots(df_combined, grouping_col)


def filter_by_selected_metrics(df_long: pd.DataFrame, group_by_tags: list[str],
                               disabled_metrics: list[str] | None = None,
                               disabled_metrics_search: list[str] | None = None) -> \
Tuple[
    pd.DataFrame, list[str]]:
    possible_metrics: list[str] = df_long["metric_name"].unique().tolist()
    possible_metrics = sorted(possible_metrics)
    default_metrics = get_possible_and_default_metrics(possible_metrics,
                                                       disabled_metrics,
                                                       disabled_metrics_search)
    selected_metrics = st.multiselect("Choose metrics", possible_metrics,
                                      default=default_metrics)
    df_long = df_long[df_long["metric_name"].isin(selected_metrics)]
    df_long = sort_by_metric_and_group_tags(df_long, group_by_tags)
    return df_long, selected_metrics

def sort_by_metric_and_group_tags(df_long: DataFrame, group_by_tags: list[str]) -> DataFrame:
    sort_columns = ["metric_name"]
    sort_columns.extend(group_by_tags)
    df_long = df_long.sort_values(by=sort_columns)
    return df_long


def get_combined_group(row: dict, group_by_tags: list[str]) -> str:
    parts = [str(row.get(tag)) for tag in group_by_tags if row.get(tag) is not None]
    return ", ".join(parts)

def add_combined_group_column(df_children: pd.DataFrame, group_by_tags: list[str],
                              col_name_combined="group",
                              col_name_no_dataset="group-no-ds"):
    df_children[col_name_combined] = df_children.apply(
        lambda row: get_combined_group(row, group_by_tags),
        axis=1)
    group_by_tags_no_ds = [g for g in group_by_tags if g != "dataset_name"]
    df_children[col_name_no_dataset] = df_children.apply(
        lambda row: get_combined_group(row, group_by_tags_no_ds),
        axis=1)