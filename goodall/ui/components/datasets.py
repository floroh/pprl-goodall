import uuid
from pathlib import Path
from typing import Dict, Any, Tuple

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots
from pprl_data_owner_service_api_client import (
    AnalysisResultDto,
    DatasetManagementApi, DatasetDto,
)

import pprl_data_owner_service_api_client as do
import pprl_linkage_unit_service_api_client as lu
from goodall.api_helper import lu_api
from goodall.api_helper.common_api import get_records_as_dataframe, \
    get_dataset_analysis_result
from goodall.api_helper.lu_api import (
    run_linkage_result_analysis,
)
from goodall.ui.components.api.lu_api_streamlit import fetch_encoded_dataset_cached
from goodall.api_helper.parser import parse_serialized_table_to_dataframe, \
    process_dataset_dataframe, order_rows, get_sorted_attributes
from goodall.api_helper.pprl_clients import Service, get_client
from goodall.ui.components.dataset_tag_analyzer import DatasetTagAnalyzer
from goodall.ui.streamlit_utils import get_state_or_default, state_exists_and_equals, sts
from goodall.utils.constants import ATTRIBUTE_REPLACEMENTS, \
    DATASET_ORDER, ATTRIBUTES_FOR_DISPLAY, ATTRIBUTE_SHORT


@st.cache_data
def get_dataset_ids(service: Service) -> list[int]:
    if service == Service.Linkage_unit:
        controller = lu.DatasetManagementApi(get_client(service))
    else:
        controller = do.DatasetManagementApi(get_client(service))
    return controller.get_dataset_ids()

@st.cache_data
def get_dataset_dto(service: Service, dataset_id: int) -> DatasetDto:
    if service == Service.Linkage_unit:
        controller = lu.DatasetManagementApi(get_client(service))
    else:
        controller = do.DatasetManagementApi(get_client(service))
    return controller.get_dataset_description(dataset_id)


@st.cache_data
def get_dataset_analysis_result_cached(
        service: Service,
        dataset_id: int,
        analysis_type: str = "DATASET_DESCRIPTION",
        parameters: Dict[str, str] = None,
) -> AnalysisResultDto:
    return get_dataset_analysis_result(service=service, dataset_id=dataset_id,
                                       analysis_type=analysis_type,
                                       parameters=parameters)


@st.cache_data
def get_records_as_dataframe_cached(
    service: Service, dataset_id: int, limit: int = -1
) -> pd.DataFrame:
    return get_records_as_dataframe(service, dataset_id, limit)


def delete_dataset(service: Service, dataset_id: int):
    dataset_controller = DatasetManagementApi(get_client(service))
    dataset_controller.delete_dataset(dataset_id)


def get_dataset_privacy_analysis(
    project_id: str, report: str = "AttributePrivacy", ref_dataset_id: int = 0
) -> pd.DataFrame:
    origin_dataset_id = lu_api.get_project(project_id).dataset_id
    df = _get_dataset_privacy_analysis(origin_dataset_id, report)
    if not df.empty:
        if ref_dataset_id != 0:
            df = add_reference_results(df, report, ref_dataset_id)
            df = df[~df["attribute"].str.contains("_DEV", na=False)]
            df = df[~df["attribute"].str.contains("FRQ", na=False)]
    return df


def add_reference_results(
    df_privacy_result: pd.DataFrame,
    report: str = "AttributePrivacy",
    ref_dataset_id: int = 2112,
) -> pd.DataFrame:
    result = _get_dataset_privacy_analysis(ref_dataset_id, report)
    result["type"] = "ref"
    df_privacy_result["type"] = "origin"
    return pd.concat([df_privacy_result, result], ignore_index=True)


def _get_dataset_privacy_analysis(dataset_id: int, report: str):
    result = get_dataset_analysis_result_cached(
        Service.Linkage_unit,
        dataset_id,
        parameters={"runPerSource": "false", "refresh": "true"},
    )
    try:
        privacy_report = result.report_groups["all"].reports[report]
    except TypeError:
        return pd.DataFrame()
    privacy_result = parse_serialized_table_to_dataframe(privacy_report.table)
    privacy_result.loc[privacy_result["attribute"] == "PLZ", "attribute"] = "ZIP"
    privacy_result = order_rows(privacy_result)
    return privacy_result


def get_linkage_evaluation(project_id: str, plaintext_id: int) -> lu.AnalysisResultDto:
    plain_records = fetch_encoded_dataset_cached(plaintext_id)
    request = lu.AnalysisRequestDto.from_dict(
        {"projectId": project_id, "parameters": {"EXCLUDE_AVAILABILITY": "true"}}
    )
    return run_linkage_result_analysis(plain_records, request)


def get_ppcr_privacy_analysis(
    project_id_ppcr: str, plaintext_dataset_id: int
) -> pd.DataFrame:
    evaluation_result = get_linkage_evaluation(project_id_ppcr, plaintext_dataset_id)
    # print(evaluation_result)
    try:
        kapr_report = evaluation_result.report_groups["Links"].reports[
            "Privacy Measure KAPR"
        ]
    except TypeError:
        return pd.DataFrame()
    kapr_result = parse_serialized_table_to_dataframe(kapr_report.table)
    return kapr_result


def render_data_owner_dataset_description(
    dataset_id, index: int = 0, analysis_type: str = "DATASET_DESCRIPTION"
):
    sel_show_records = st.checkbox("Show records", key=f"show_records{index}")
    if sel_show_records:
        sel_combine_sources = st.checkbox(
            "Combine sources", key=f"combine_sources{index}"
        )
        render_dataset_records(Service.Data_owner_1, dataset_id, separated_by_source=not sel_combine_sources)

    render_dataset_report = st.checkbox("Show analysis", key=f"show_dataset_analysis{index}")
    if render_dataset_report:
        render_dataset_analysis_report_for_id(dataset_id, analysis_type=analysis_type)


def render_dataset_records(
    service: Service, dataset_id: int, separated_by_source: bool = True
):
    df = get_records_as_dataframe_cached(
        service, dataset_id, get_state_or_default("record_limit", 20)
    )
    # -1)
    df.rename(columns=lambda col: col.replace("PLZ", "ZIP"), inplace=True)
    df.drop(columns="datasetId", inplace=True)
    df = process_dataset_dataframe(df)

    if separated_by_source:
        grouped = df.groupby("id.source")
        for group_name, group_data in grouped:
            with st.container(height=300):
                st.subheader(f"Records of source {group_name}")
                st.dataframe(group_data, hide_index=True)
    else:
        with st.container(height=600):
            st.dataframe(df, hide_index=True)


@st.cache_data
def get_tags(dataset_id: int) -> pd.DataFrame:
    return DatasetTagAnalyzer.get_df_tags(sts["selected_service"], dataset_id)

def render_dataset_analysis_report_for_id(
    dataset_id: int, analysis_type: str = "DATASET_DESCRIPTION"
):
    parameters = None
    if analysis_type == "TAG_BASED_DATASET_ANALYSIS":
        analyzer = DatasetTagAnalyzer(dataset_id, get_tags(dataset_id))
        analyzer.analyze()
    else:
        if state_exists_and_equals("include_additional_results", True):
            parameters = {"includeAdditionalResults": "true"}
        result = get_dataset_analysis_result_cached(
            sts["selected_service"], dataset_id, analysis_type=analysis_type,
            parameters=parameters
        )
        render_dataset_analysis_report(result)


def render_dataset_analysis_report(result: AnalysisResultDto, show_additional_results: bool = False):
    st.json(result.to_json(), expanded=False)
    for report_group in result.report_groups.values():
        if report_group.name == "all":
            is_expanded = True
        else:
            is_expanded = False
        with st.expander(report_group.name, expanded=is_expanded):
            for report in report_group.reports.values():
                if ">>>" in report.name and not show_additional_results:
                    continue
                st.caption(report.name)
                with st.container():
                    if report.type == "TEXT":
                        st.text(report.report)
                    elif report.type == "TABLE":
                        dfReport = parse_serialized_table_to_dataframe(report.table)
                        st.text(report.report)
                        if "WeightAnalyzer" in report.name:
                            st.write("Similarity distribution")
                            st.data_editor(dfReport)
                        else:
                            st.dataframe(dfReport)



def reorder_columns_by_dataset(
    df: pd.DataFrame,
    order_list: list[str],
    suffixes: list[str] = None
) -> pd.DataFrame:
    """
    Reorder DataFrame columns based on order_list and optional suffixes.
    Columns not in order_list are appended at the end.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame
    order_list : list of str
        List of dataset names (or column bases) in desired order
    suffixes : list of str, optional
        List of suffixes to append to dataset names, e.g., ['.v', '.f']

    Returns
    -------
    pd.DataFrame
        DataFrame with reordered columns
    """
    if suffixes is None:
        ordered_cols = [col for col in order_list if col in df.columns]
    else:
        ordered_cols = []
        for ds in order_list:
            for suf in suffixes:
                col_name = f"{ds}{suf}"
                if col_name in df.columns:
                    ordered_cols.append(col_name)
    remaining_cols = [col for col in df.columns if col not in ordered_cols]
    new_order = ordered_cols + remaining_cols
    return df[new_order]

def plot_attribute_availability(normalized: dict[str, pd.DataFrame]):
    for key, df in normalized.items():
        df["attribute"] = df["attribute"].replace(ATTRIBUTE_REPLACEMENTS)
    all_attrs_raw = sorted({a for df in normalized.values() for a in df["attribute"].tolist()})
    all_attrs = get_sorted_attributes(all_attrs_raw)

    # build pivot tables
    missing_pct = pd.DataFrame(index=all_attrs)
    breakdown = {}  # per dataset DataFrame indexed by attribute with columns valid,invalid,empty,missing
    for name, df in normalized.items():
        df2 = df.set_index("attribute").reindex(all_attrs).fillna(0.0)
        missing_pct[name] = df2["missing"] + df2["empty"]
        breakdown[name] = df2[["valid", "invalid", "empty", "missing"]]
    # Sidebar controls
    with st.sidebar:
        st.header("Display options")
        # choose attributes to show
        default_attrs = all_attrs[:50]  # default: first 50
        chosen_attrs = st.multiselect("Attributes to show (empty = all)", all_attrs,
                                      default=default_attrs)
        if not chosen_attrs:
            chosen_attrs = all_attrs
        order_by = st.selectbox("Order features by", ("attribute", "missing_mean_desc"),
                                index=0)
        if order_by == "missing_mean_desc":
            order = missing_pct.loc[chosen_attrs].mean(axis=1).sort_values(
                ascending=False).index.tolist()
        else:
            order = chosen_attrs

        heatmap_height = st.slider("Heatmap height (px)", min_value=300, max_value=1600,
                                   value=600, step=50)
        show_stacked = st.checkbox("Show stacked breakdown bars per feature",
                                   value=True)
    # ---- Heatmap: feature x dataset (% missing) ----
    hm_df = missing_pct.loc[order]
    hm_df = reorder_columns_by_dataset(hm_df, DATASET_ORDER)
    if st.checkbox("Show dataframe"):
        st.dataframe(hm_df)
    fig_hm = px.imshow(
        hm_df.values,
        x=hm_df.columns.tolist(),
        y=hm_df.index.tolist(),
        labels={"x": "Dataset", "y": "Attribute", "color": "% missing"},
        color_continuous_scale="Blues",
        aspect="auto",
        text_auto=True
    )
    fig_hm.update_layout(height=heatmap_height, margin=dict(l=220, r=20, t=40, b=40))
    st.subheader("Feature × Dataset: % Missing (heatmap)")
    st.plotly_chart(fig_hm, use_container_width=True)

    # ---- Optional: stacked bar per feature showing valid/invalid/empty/missing for each dataset ----
    if show_stacked:
        st.subheader(
            "Per-feature stacked breakdown (valid / invalid / empty / missing)")
        # Build long dataframe for plotly: columns = attribute, dataset, category, pct
        long_parts = []
        for name, df in breakdown.items():
            df2 = df.reset_index().rename(columns={"index": "attribute"})
            df2["dataset"] = name
            long = df2.melt(id_vars=["attribute", "dataset"],
                            value_vars=["valid", "invalid", "empty", "missing"],
                            var_name="category", value_name="pct")
            long_parts.append(long)
        long_df = pd.concat(long_parts, ignore_index=True)
        long_df = long_df[long_df["attribute"].isin(order)]

        # Plot grouped by dataset, facet by dataset to compare per dataset per feature (too crowded otherwise).
        # Use facet_col = dataset for horizontal layout
        fig_bar = px.bar(
            long_df,
            x="pct",
            y="attribute",
            color="category",
            orientation="h",
            facet_col="dataset",
            category_orders={"attribute": order},
            height=min(1000, 40 * len(order) + 200),
            labels={"pct": "Percent", "attribute": "Attribute"}
        )
        fig_bar.update_layout(barmode="stack", margin=dict(l=220, r=20, t=40, b=40))
        # reduce facet spacing
        fig_bar.update_xaxes(
            matches=None)  # allow different x scales per dataset if you prefer
        st.plotly_chart(fig_bar, use_container_width=True)



def plot_attribute_statistics(normalized: dict[str, pd.DataFrame]):
    """
    summaries: dict[name -> per-attribute summary DF]
      Each DF should have attribute,count,median,mean,min,max,sd (case-insensitive).
    Produces:
      - heatmaps (mean/median/sd) feature x dataset
      - horizontal "boxplot-like" figure per dataset showing min→max, median, mean±sd
    """
    # union attributes

    for key, df in normalized.items():
        df["attribute"] = df["attribute"].replace(ATTRIBUTE_REPLACEMENTS)
    all_attrs_raw = sorted({a for df in normalized.values() for a in df["attribute"].tolist()})
    all_attrs = get_sorted_attributes(all_attrs_raw)

    # build dataframes keyed by attribute
    possible_metrics = ["mean", "median", "sd", "count", "min", "max"]
    available_metrics_set = set()
    for df in normalized.values():
        lower_cols = {c.lower(): c for c in df.columns}
        for metric in possible_metrics:
            if metric.lower() in lower_cols:
                available_metrics_set.add(metric)
    metrics = [m for m in possible_metrics if m in available_metrics_set]
    metric_pivots = {m: pd.DataFrame(index=all_attrs) for m in metrics}

    for name, df in normalized.items():
        df2 = df.set_index("attribute").reindex(all_attrs)
        for m in metrics:
            metric_pivots[m][name] = df2[m]

    # STREAMLIT UI controls
    with st.sidebar:
        st.header("Display options")
        default_attrs = all_attrs[:30]
        chosen_attrs = st.multiselect("Attributes to show (empty = all)", all_attrs, default=default_attrs)
        if not chosen_attrs:
            chosen_attrs = all_attrs

        # choose which metric heatmap to show
        heat_metric = st.selectbox("Heatmap metric", options=["mean", "median", "sd"], index=0)
        # controls for boxplot-like
        if len(normalized) > 1:
            max_datasets = st.slider("Max datasets to show in boxplot-like view", min_value=1, max_value=len(normalized), value=min(4, len(normalized)))
        else:
            max_datasets = len(normalized)
        chosen_datasets = st.multiselect("Datasets to include in boxplot-like view (order matters)", list(normalized.keys()), default=list(normalized.keys())[:max_datasets])
        if not chosen_datasets:
            chosen_datasets = list(normalized.keys())[:max_datasets]

        order_by = st.selectbox("Order attributes by", ("attribute", f"{heat_metric}_desc"))
        if order_by == f"{heat_metric}_desc":
            # sort by mean/median/sd across datasets (descending)
            order = metric_pivots[heat_metric].loc[chosen_attrs].mean(axis=1).sort_values(ascending=False).index.tolist()
        else:
            order = [a for a in all_attrs if a in chosen_attrs]

        heatmap_height = st.slider("Heatmap height (px)", 300, 1400, 700, step=50)
        show_boxlike = st.checkbox("Show boxplot-like comparisons", value=True)
        annotate_values = st.checkbox("Annotate heatmap values", value=False)

    # --- Heatmap for selected metric ---
    hm_df = metric_pivots[heat_metric].loc[order]
    hm_df = reorder_columns_by_dataset(hm_df, DATASET_ORDER)

    if st.checkbox("Show dataframe"):
        st.dataframe(hm_df)
    # If metric is sd, it can be large scale; no normalization by default.
    title = f"Feature × Dataset: {heat_metric}"
    fig_hm = px.imshow(
        hm_df.values,
        x=hm_df.columns.tolist(),
        y=hm_df.index.tolist(),
        labels={"x": "Dataset", "y": "Attribute", "color": heat_metric},
        aspect="auto",
        color_continuous_scale="Viridis",
        text_auto=annotate_values
    )
    fig_hm.update_layout(height=heatmap_height, margin=dict(l=240, r=20, t=40, b=40))
    st.subheader(title)
    st.plotly_chart(fig_hm, use_container_width=True)

    st.subheader("Summary table (selected attributes)")
    hm_df = reorder_columns_by_dataset(hm_df, DATASET_ORDER)
    st.dataframe(hm_df.style.format({c: "{:.3f}" for c in hm_df.columns}))

    # --- Boxplot-like visuals built from aggregated stats ---
    if show_boxlike:
        st.subheader("Boxplot-like comparison (min → max, median, mean ± sd)")
        # For readability, only include chosen_datasets and chosen attributes
        attrs = order  # already filtered and ordered
        datasets = chosen_datasets

        # Build a single figure where y axis is attribute and traces per dataset are grouped vertically.
        # We'll offset dataset positions slightly so multiple datasets per attribute are visible.
        # y_base_index for attribute i is i; dataset offsets applied around it.
        y_positions = {attr: i for i, attr in enumerate(attrs)}
        n_dsets = len(datasets)
        # small offset scale
        offset_scale = 0.18  # how far apart dataset bars are within an attribute row
        offsets = np.linspace(-offset_scale * n_dsets / 2, offset_scale * n_dsets / 2, n_dsets)

        fig = go.Figure()
        for j, ds in enumerate(datasets):
            mins = metric_pivots["min"][ds].reindex(attrs)
            maxs = metric_pivots["max"][ds].reindex(attrs)
            meds = metric_pivots["median"][ds].reindex(attrs)
            means = metric_pivots["mean"][ds].reindex(attrs)
            sds = metric_pivots["sd"][ds].reindex(attrs)

            # bar from min to max: use go.Bar with base=min and length=max-min
            # but bar wants positive length; if max<min (bad data) guard
            span = (maxs - mins).fillna(0)
            # y positions
            ys = [y_positions[a] + offsets[j] for a in attrs]

            # horizontal bars: use go.Bar with orientation='h'
            fig.add_trace(go.Bar(
                x=span.values,
                y=ys,
                base=mins.values,
                orientation='h',
                width=0.25,
                marker=dict(opacity=0.4),
                name=f"{ds} range",
                hovertemplate=(
                    "dataset=%s<br>attr=%s<br>min=%g<br>max=%g<br>median=%g<br>mean=%g<br>sd=%g"
                )
            ))

            # median markers
            fig.add_trace(go.Scatter(
                x=meds.values,
                y=ys,
                mode='markers',
                marker_symbol='diamond',
                marker_size=10,
                name=f"{ds} median",
                showlegend=(j == 0),
            ))
            # mean markers with horizontal error bars = sd
            fig.add_trace(go.Scatter(
                x=means.values,
                y=ys,
                mode='markers',
                marker_symbol='circle-open',
                marker_size=9,
                error_x=dict(type='data', array=sds.fillna(0).values, visible=True),
                name=f"{ds} mean±sd",
                showlegend=(j == 0),
            ))

        # format y axis to show attribute labels at integer positions (use middle offset)
        y_tickvals = list(range(len(attrs)))
        y_ticktext = attrs
        fig.update_yaxes(tickmode="array", tickvals=y_tickvals, ticktext=y_ticktext, autorange='reversed')

        fig.update_layout(
            height= max(400, 40 * len(attrs)),
            margin=dict(l=300, r=20, t=40, b=40),
            yaxis_title="Attribute",
            xaxis_title="Value (units as in summaries)",
            legend_title="Legend",
        )
        st.plotly_chart(fig, use_container_width=True)



# Numeric mapping for similarity codes
CODE_TO_NUM = {
    '==': 4,    # equal
    'SS': 3,    # very similar
    'ss': 2,    # somewhat similar
    'DD': 1,    # dissimilar
    '?.': 0.5,  # one missing
    '??': 0     # both missing
}

COLORSCALE = [
    [0.0, 'black'],       # 0 -> ??
    [0.125, 'grey'],      # 0.5 -> ?.
    # [0.25, 'red'],        # 1 -> DD
    # [0.25, '#7A1F1F'],        # 1 -> DD
    [0.25, '#8B0000'],        # 1 -> DD
    [0.5, 'yellow'],      # 2 -> ss
    [0.75, 'lightgreen'], # 3 -> SS
    [1.0, 'green']        # 4 -> ==
]
# COLORSCALE = [
#     [0.0, 'black'],       # 0 -> ??
#     [0.125, 'grey'],      # 0.5 -> ?.
#     [0.25, '#EF553B'],        # 1 -> DD
#     [0.5, '#B6E880'],      # 2 -> ss
#     [0.75, '#00CC96'], # 3 -> SS
#     [1.0, '#2CA02C']        # 4 -> ==
# ]

ALL_CODES = list(CODE_TO_NUM.values())
ALL_CODE_LABELS = ['??', '?.', 'DD', 'ss', 'SS', '==']  # optional hover labels

def parse_schema_strings(df: pd.DataFrame) -> list[Any]:
    parsed_schemas = []
    for schema_str in df['Schema']:
        row_dict = parse_schema_string(schema_str)
        parsed_schemas.append(row_dict)
    return parsed_schemas

def parse_schema_string(schema_str) -> dict[str, str]:
    row_dict = {}
    parts = schema_str.split('_')
    for part in parts:
        if ':' in part:
            attr, code = part.split(':', 1)
            if attr == "PLZ":
                attr = "ZIP"
            if attr.lower() == "gender":
                attr = "SEX"
            row_dict[attr] = code
    return row_dict


def replace_schema_strings(df: pd.DataFrame,
                           parsed_schemas: list[dict[str, str]] | None = None,
                           attributes_to_keep: list[str] = ATTRIBUTES_FOR_DISPLAY):
    if not parsed_schemas:
        parsed_schemas = parse_schema_strings(df)
    new_schema_str_list = []
    for parsed_schema in parsed_schemas:
        new_schema_str = ""
        for attr_name in attributes_to_keep:
            if attr_name in parsed_schema:
                new_schema_str += f"_{attr_name}:{parsed_schema[attr_name]}"
        new_schema_str_list.append(new_schema_str)
    df['Schema'] = new_schema_str_list

def merge_stats_for_schema_strings(df: pd.DataFrame):
    df_grouped = df.groupby('Schema').agg({
        'absFrequency': 'sum',
        'relFrequency': 'sum'
    }).reset_index()
    df_grouped = df_grouped.sort_values(by='absFrequency', ascending=False)
    return df_grouped


def parse_and_map(df: pd.DataFrame, report_name: str = None, limit: int = 10)\
        -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Parse schema strings into numeric DataFrame for heatmap plotting."""

    df.rename(columns=lambda col: col.replace("SCHEMA", "Schema"), inplace=True)
    replace_schema_strings(df, attributes_to_keep=ATTRIBUTES_FOR_DISPLAY)
    df = merge_stats_for_schema_strings(df)
    if limit > 0:
        df = df.head(limit)
    parsed_schemas = parse_schema_strings(df)
    schema_cols = pd.DataFrame(parsed_schemas)
    ordered_columns = [attr for attr in ATTRIBUTES_FOR_DISPLAY if attr in schema_cols.columns]
    schema_cols = schema_cols.reindex(columns=ordered_columns)

    num_data = schema_cols.map(lambda cell: CODE_TO_NUM.get(cell, 0) if isinstance(cell, str) else 0)

    if report_name:
        num_data.columns = [f"{report_name} | {col}" for col in num_data.columns]

    return num_data, df


def add_vertical_legend_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add a blank separator column and a single-column vertical legend on the right.
    The legend has one row per code; other rows are empty.
    """
    n_rows = df.shape[0]
    n_codes = len(ALL_CODES)

    # Create blank separator column
    blank_col = pd.DataFrame([[None]]*n_rows, columns=["sep_legend"], index=df.index)
    df_with_sep = pd.concat([df, blank_col], axis=1)

    # Create legend column: fill first n_codes rows, rest are NaN
    legend_col_values = ALL_CODES + [None]*(n_rows - n_codes)
    legend_col = pd.DataFrame({"Legend": legend_col_values}, index=df.index)

    df_final = pd.concat([df_with_sep, legend_col], axis=1)
    return df_final

def generate_y_labels(df_length: int) -> list[str]:
    """Generate y-axis labels for actual data rows."""
    return [f"top {i+1}" for i in range(df_length)]

def add_rel_frequency_column(df_numeric: pd.DataFrame, df_original: pd.DataFrame) -> pd.DataFrame:
    """
    Add a column with rounded relFrequency values to the right of the numeric schema matrix.
    """
    rel_freq = df_original['relFrequency'].round(1)
    rel_freq_col = pd.DataFrame({'relFrequency': rel_freq}, index=df_numeric.index)
    return pd.concat([df_numeric, rel_freq_col], axis=1)


def generate_frequency_table(df_reports: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Generate a wide table of relFrequency and absFrequency for all topN rows of each report.

    Returns a dataframe with multi-level columns: (report_name, frequency_type)
    """
    freq_tables = []

    for report_name, df in df_reports.items():
        df = df.head(10)
        freq_df = df[['relFrequency', 'absFrequency']].round(
            3)  # round relFrequency to 1 decimal
        # rename columns with report name
        freq_df.columns = pd.MultiIndex.from_product([[report_name], freq_df.columns])
        freq_df.reset_index(drop=True, inplace=True)
        freq_tables.append(freq_df)

    # Combine horizontally
    combined_freq_df = pd.concat(freq_tables, axis=1)
    combined_freq_df.index = [f"top {i + 1}" for i in range(combined_freq_df.shape[0])]
    return combined_freq_df



def plot_pairwise_schema(df: pd.DataFrame):
    """Plot a single schema dataframe with vertical legend column on the right."""
    num_data, df = parse_and_map(df)
    num_data_full = add_vertical_legend_column(num_data)
    y_labels = generate_y_labels(len(df))

    fig = px.imshow(
        num_data_full,
        labels=dict(x="Attribute", y="Schema Rank", color="Similarity"),
        x=num_data_full.columns,
        y=y_labels,
        color_continuous_scale=COLORSCALE,
        aspect="auto",
        height=max(600, 30*len(df))
    )

    fig.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig, key=str(uuid.uuid4()))

def plot_pairwise_schemas(df_reports: dict[str, pd.DataFrame]):
    """Plot multiple schema dataframes horizontally with vertical legend column."""
    horizontal_blocks = []
    for i, (report_name, df) in enumerate(df_reports.items()):
        num_data, df = parse_and_map(df, report_name)
        df_reports[report_name] = df
        horizontal_blocks.append(num_data)

        # Add blank column between reports
        if i < len(df_reports) - 1:
            sep_col = pd.DataFrame(
                [[None]] * num_data.shape[0],
                columns=[f"sep_{i}"],
                index=num_data.index
            )
            horizontal_blocks.append(sep_col)
    combined_df = pd.concat(horizontal_blocks, axis=1)
    if st.button("Save reports dataframe"):
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"df_diff_pattern_{timestamp}.csv"
        combined_df.to_csv(filename)
        st.success(f"Saved to {filename}")
    # combined_df_full = add_vertical_legend_column(combined_df)
    combined_df_full = combined_df
    combined_length = len(combined_df_full)
    y_labels = generate_y_labels(combined_length)
    st.dataframe(combined_df_full)
    x_labels = combined_df_full.columns
    # x_labels = ["" if col.startswith("sep_") else col for col in x_labels]
    fig = px.imshow(
        combined_df_full,
        labels=dict(x="Attribute (Report)", y="Schema Rank", color="Similarity"),
        x=x_labels,
        y=y_labels,
        color_continuous_scale=COLORSCALE,
        aspect="auto",
        height=max(600, 30*combined_length),
        # showlegend=False
    )

    fig.update_layout(
        coloraxis_showscale=False,
    )
    st.plotly_chart(fig, key=str(uuid.uuid4()))

    freq_table = generate_frequency_table(df_reports)
    st.dataframe(freq_table)  # show in Streamlit

def save_dataset_data_csv(dataset_data: dict[str, tuple[pd.DataFrame, pd.DataFrame]], folder: str):
    folder_path = Path(folder)
    folder_path.mkdir(parents=True, exist_ok=True)

    for report_name, (num_data, mapped_df) in dataset_data.items():
        num_data_file = folder_path / f"{report_name}_num_data.csv"
        mapped_df_file = folder_path / f"{report_name}_mapped_df.csv"

        num_data.to_csv(num_data_file, index=False)
        mapped_df.to_csv(mapped_df_file, index=False)

def load_dataset_data_csv(folder: str) -> dict[str, tuple[pd.DataFrame, pd.DataFrame]]:
    folder_path = Path(folder)
    dataset_data = {}

    # Find all *_num_data.csv files
    for num_data_file in folder_path.glob("*_num_data.csv"):
        report_name = num_data_file.stem.replace("_num_data", "")
        mapped_df_file = folder_path / f"{report_name}_mapped_df.csv"

        num_data = pd.read_csv(num_data_file)
        mapped_df = pd.read_csv(mapped_df_file)

        dataset_data[report_name] = (num_data, mapped_df)

    return dataset_data

def plot_pairwise_schemas_subplots(df_reports: dict[str, pd.DataFrame]):
    dataset_data: dict[str, tuple[pd.DataFrame, pd.DataFrame]] = {}

    # Parse + normalize input
    for report_name, df in df_reports.items():
        num_data, mapped_df = parse_and_map(df)
        dataset_data[report_name] = (num_data, mapped_df)
        # st.dataframe(mapped_df)

    if st.sidebar.toggle("Sort known datasets", value=True):
        ordered_datasets = [name for name in DATASET_ORDER if name in dataset_data]
        dataset_data = {name: dataset_data[name] for name in ordered_datasets}

    if st.button("Save reports dataframes"):
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        folder_name = f"diff_pattern_{timestamp}"
        save_dataset_data_csv(dataset_data, folder_name)
        st.success(f"Saved to {folder_name}")

    fig = make_subplots(
        rows=1,
        cols=len(dataset_data),
        shared_yaxes=True,
        subplot_titles=list(dataset_data.keys()),
        horizontal_spacing=0.02,
    )

    max_length = 0

    for col_idx, (dataset_name, (num_data_df, mapped_df)) in enumerate(
            dataset_data.items(), start=1):
        max_length = max(max_length, len(num_data_df))

        # Extract attribute short names from columns
        x_labels = [ATTRIBUTE_SHORT.get(col.split(" | ")[-1], col) for col in
                    num_data_df.columns]

        y_labels = generate_y_labels(len(num_data_df))

        fig.add_trace(
            go.Heatmap(
                z=num_data_df.values,
                x=x_labels,
                y=y_labels,
                coloraxis="coloraxis",
            ),
            row=1,
            col=col_idx,
        )

    fig.update_layout(
        coloraxis=dict(
            colorscale=COLORSCALE,
            colorbar_title="Similarity",
        ),
        height=max(600, 30 * max_length),
        margin=dict(t=80),
    )

    fig.update_xaxes(
        tickangle=0,
        tickfont=dict(size=14),
    )
    fig.update_yaxes(
    #     title_text="Schema Rank",
        autorange="reversed",
    )
    st.plotly_chart(fig)

    st.warning("Frequency tables may not match the heatmap as the entries are not merged on selected attribute sets.")
    freq_table = generate_frequency_table(df_reports)
    st.dataframe(freq_table)  # show in Streamlit


def plot_attribute_frequency_distributions(df_sub_reports: pd.DataFrame, x_lim: int = 100) -> dict[str, go.Figure]:
    df_sub_reports = df_sub_reports[df_sub_reports["group"] == "A"]
    attribute_names = df_sub_reports["attribute_name"].unique().tolist()
    attribute_names = get_sorted_attributes(attribute_names)
    figs = {}
    for attr_name in attribute_names:
        df_attr = df_sub_reports[df_sub_reports["attribute_name"] == attr_name]
        df_attr.reset_index(drop=True, inplace=True)
        df_attr["n"] = df_attr.groupby("dataset_name").cumcount()

        df_attr["dataset_name"] = pd.Categorical(
            df_attr["dataset_name"],
            categories=DATASET_ORDER,
            ordered=True
        )

        # Sort by dataset_name (categorical) and then by n
        df_attr = df_attr.sort_values(["dataset_name", "n"]).reset_index(drop=True)

        # fig = px.bar(df_attr, x="n", y="relFrequency", color="dataset_name",
        #              barmode="group")
        # fig = px.line(df_attr, x="n", y="relFrequency", color="dataset_name", log_x=True)
        my_symbols = ["circle", "square", "diamond", "cross", "x", "triangle-up",
                      "triangle-down", "star", "bowtie"]
        fig = px.line(df_attr, x="n", y="relFrequency", color="dataset_name", symbol="dataset_name", range_x=[0, x_lim],
                      color_discrete_sequence=px.colors.qualitative.Plotly,
                      symbol_sequence=my_symbols)
        figs[attr_name] = fig
    return figs


def get_attribute_most_frequent_values_tables(df_sub_reports: pd.DataFrame,
                                              top_n_values: int = 10,
                                              show_percent_values: bool = False,
                                              digits: int = 3,
                                              separate_columns_for_value_and_frequency: bool = True
                                              ) -> dict[str, pd.DataFrame]:
    df_sub_reports = df_sub_reports[df_sub_reports["group"] == "A"]
    # st.dataframe(df_sub_reports)

    include_frequencies = st.sidebar.toggle("Include attribute frequencies", True)
    dfs = {}

    attribute_names = df_sub_reports["attribute_name"].unique().tolist()
    attribute_names = get_sorted_attributes(attribute_names)
    for attr_name in attribute_names:
        df_attr = df_sub_reports[df_sub_reports["attribute_name"] == attr_name]
        df_mfv = pd.DataFrame(
            index=range(top_n_values))  # fixed integer index 0..9
        for dataset_id, df_ds in df_attr.groupby("dataset_name"):
            # Attribute values (pad with NaN if fewer than TOP_N)
            df_ds = df_ds.head(top_n_values).copy()
            attr_vals = df_ds["attribute"].values
            attr_vals_padded = np.pad(attr_vals, (0, top_n_values - len(attr_vals)),
                                      constant_values=np.nan)
            if include_frequencies:
                if show_percent_values:
                    df_ds["relFrequency"] = df_ds["relFrequency"] * 100
                df_ds["relFrequency"] = df_ds["relFrequency"].round(digits)
                freq_vals = df_ds["relFrequency"].values
                freq_vals_padded = np.pad(freq_vals, (0, top_n_values - len(freq_vals)),
                                          constant_values=np.nan)
                if separate_columns_for_value_and_frequency:
                    df_mfv[f"{dataset_id}.v"] = attr_vals_padded
                    df_mfv[f"{dataset_id}.f"] = freq_vals_padded
                else:
                    combined_values = [
                        f"{val} ({freq})" if pd.notna(val) and pd.notna(freq) else ""
                        for val, freq in zip(attr_vals_padded, freq_vals_padded)
                    ]
                    df_mfv[f"{dataset_id}"] = combined_values
            else:
                df_mfv[f"{dataset_id}"] = attr_vals_padded
        df_mfv.dropna(how="all", inplace=True)
        if separate_columns_for_value_and_frequency:
            df_mfv = reorder_columns_by_dataset(df_mfv, DATASET_ORDER, [".v", ".f"])
        else:
            df_mfv = reorder_columns_by_dataset(df_mfv, DATASET_ORDER)

        df_mfv.insert(loc=0,
                  column='n',
                  value=df_mfv.index + 1)

        dfs[attr_name] = df_mfv
        # st.text(f"Attribute: {attr_name}")
        # st.dataframe(df_mfv)
    return dfs

def plot_violin(df: pd.DataFrame, metric_column: str):
    group_names = df["group"].unique().tolist()
    if len(group_names) == 2:
        st.text("Show violin plot for each source")
        fig = go.Figure()
        sides = ["negative", "positive"]
        colors = ["blue", "orange"]
        for group_idx, group_name in enumerate(group_names):
            fig.add_trace(go.Violin(x=df['attribute_name'][df['group'] == group_name],
                                    y=df[metric_column][df['group'] == group_name],
                                    legendgroup=group_name, scalegroup=group_name, name=group_name,
                                    scalemode="count",
                                    side=sides[group_idx],
                                    line_color=colors[group_idx])
                      )
        fig.update_traces(meanline_visible=True)
        fig.update_layout(violingap=0, violinmode='overlay')
        st.plotly_chart(fig)
    else:
        st.text("Show violin plot for all records")
