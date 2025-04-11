import streamlit
from plotly.graph_objs import Figure
from pprl_linkage_unit_service_api_client import BatchMatchProjectDto

from goodall.api_helper.lu_api import (
    get_projects,
    get_project,
    get_record_pairs,
    delete_project,
    get_record_pairs_as_dataframe,
)
from goodall.api_helper.parser import parse_record_pair_df, get_project_quality_results
from goodall.ui.components.projects import (
    project_refresh,
    project_id_colored_button,
    project_selector,
    get_indexed_state_key,
    prepareProjectsForDisplay,
)
from goodall.result_analysis.pair_evaluation import *
from goodall.ui.streamlit_utils import del_state_if_exists, get_state_or_default
from goodall.utils import downsampling_if_possible
from goodall.ui.PPRL_Services_UI import *
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

referenceLineStyle = dict(color="Gray", width=2)
color_map_type_change = {"TT": "blue", "TF": "red", "FT": "green", "FF": "orange"}
color_map_match_grade_change = {"CC": "blue", "CN": "yellow", "NC": "orange", "NN": "blue"}

def prepare_for_merge(df: DataFrame):
    if df.empty:
        return df
    df["i0"] = df["id0"].apply(lambda id: id["source"] + "-" + id["local"])
    df["i1"] = df["id1"].apply(lambda id: id["source"] + "-" + id["local"])
    df["ID0"] = df[["i0", "i1"]].min(axis=1)
    df["ID1"] = df[["i0", "i1"]].max(axis=1)
    # df = df.loc[df['active'] == True]
    return df.drop(columns=["i0", "i1", "id0", "id1"])


def pos_neg_result(groupedStats: pd.DataFrame, type: str) -> float:
    resSize = groupedStats["size"]
    type_series = resSize.get(type)
    if type_series is None:
        print("No " + type)
        return 0
    pos = resSize.at[type].get("+")
    if pos is None:
        pos = 0
    neg = resSize.at[type].get("-")
    if neg is None:
        neg = 0
    diff = pos - neg
    # print('Diff for ' + type + ': ' + str(diff))
    st.write("Diff for " + type + ": " + str(diff))
    return diff


def count_type_changes(dfM: DataFrame):
    stats = compute_change_statistics(dfM)
    col1, col2, col3 = st.columns([1, 2, 2])
    with col1:
        st.dataframe(stats, hide_index=True)

    # labels = ['TP_x', 'FP_x', 'FN_x', 'TN_x', 'TP_y', 'FP_y', 'FN_y', 'TN_y']
    # source_indices = [labels.index(current_type + '_x') for current_type in stats['type_x']]
    # target_indices = [labels.index(current_type + '_y') for current_type in stats['type_y']]

    with col2:
        fig = plot_type_correspondences(stats)
        st.plotly_chart(fig)
    with col3:
        fig = plot_type_changes(stats)
        st.plotly_chart(fig)


def compute_change_statistics(df_in: pd.DataFrame, column: str = "type"):
    df = df_in.copy()
    change_column = f"{column}_change"
    df.insert(4, change_column, df[f"{column}_x"] + "->" + df[f"{column}_y"])
    grouped = df.groupby(by=[change_column, f"{column}_x", f"{column}_y"])
    stats = (
        grouped[change_column]
        .agg([np.size])
        .sort_values(by=[f"{column}_x", f"{column}_y"], ascending=False)
    )
    stats.reset_index(inplace=True)
    return stats


def plot_type_changes(stats):
    changeOnlyStats = stats[stats["type_x"] != stats["type_y"]]
    labels = ["TP_x", "FP_x", "FN_x", "TN_x", "TP_y", "FP_y", "FN_y", "TN_y"]
    source_indices = [
        labels.index(current_type + "_x")
        for current_type in changeOnlyStats["type_x"]
    ]
    target_indices = [
        labels.index(current_type + "_y")
        for current_type in changeOnlyStats["type_y"]
    ]
    link_colors = changeOnlyStats[["type_x", "type_y"]].apply(
        lambda x: color_map_type_change[x["type_x"][0] + x["type_y"][0]], axis=1
    )
    fig = go.Figure(
        data=[
            go.Sankey(
                node=dict(
                    pad=15,
                    thickness=20,
                    line=dict(color="black", width=0.5),
                    label=labels,
                    color="blue",
                ),
                link=dict(
                    source=source_indices,
                    # indices correspond to labels, eg A1, A2, A1, B1, ...
                    target=target_indices,
                    value=changeOnlyStats["size"],
                    color=link_colors,
                ),
            )
        ]
    )
    fig.update_layout(title_text="Type changes", font_size=20)
    return fig


def plot_type_correspondences(stats) -> Figure:
    labels = ["Match", "Non-Match", "Match", "Non-Match"]
    source_indices = [
        labels[:2].index(("Match" if current_type in ["TP", "FP"] else "Non-Match")) for current_type in stats["type_x"]
    ]
    target_indices = [
        labels[2:].index(("Match" if current_type in ["TP", "FP"] else "Non-Match")) + 2
        for current_type in stats["type_y"]
    ]
    link_colors = stats[["type_x", "type_y"]].apply(
        lambda x: color_map_type_change[x["type_x"][0] + x["type_y"][0]], axis=1
    )
    fig = go.Figure(
        data=[
            go.Sankey(
                node=dict(
                    thickness=20,
                    line=dict(color="black", width=0.5),
                    label=labels,
                    color="black",
                    pad=15,  # Padding between nodes
                ),
                link=dict(
                    source=source_indices,
                    target=target_indices,
                    line=dict(color="black", width=0.5),
                    value=stats["size"],
                    color=link_colors,
                ),
                textfont={'color': 'white'},
            )
        ]
    )

    fig.update_layout(title_text="Prediction changes", font_size=15)
    return fig

def plot_match_grade_correspondences(stats) -> Figure:
    labels_for_indexing = ["CERTAIN_MATCH", "NON_MATCH", "CERTAIN_MATCH", "NON_MATCH"]
    labels = ["Match", "Non-Match", "Match", "Non-Match"]
    left_column = "matchGrade_x"
    right_column = "matchGrade_y"
    source_indices = [
        labels_for_indexing[:2].index(current_type) for current_type in stats[left_column]
    ]
    target_indices = [
        labels_for_indexing[2:].index(current_type) + 2 for current_type in stats[right_column]
    ]
    link_colors = stats[[left_column, right_column]].apply(
        lambda x: color_map_match_grade_change[x[left_column][0] + x[right_column][0]], axis=1
    )
    fig = go.Figure(
        data=[
            go.Sankey(
                node=dict(
                    thickness=20,
                    line=dict(color="black", width=0.5),
                    label=labels,
                    color="black",
                ),
                link=dict(
                    source=source_indices,
                    # indices correspond to labels, eg A1, A2, A1, B1, ...
                    target=target_indices,
                    line=dict(color="black", width=0.5),
                    value=stats["size"],
                    color=link_colors,
                ),
                textfont={'color': 'white'},
            )
        ]
    )
    fig.update_layout(title_text="Prediction changes", font_size=20)
    return fig


def analyse_changes_by_type(dfM: DataFrame, numeric_column: str):
    col_x = numeric_column + "_x"
    col_y = numeric_column + "_y"
    col_shift_binary = numeric_column + "_shift_binary"
    col_diff = numeric_column + "_diff"
    conditions = [
        dfM[col_x] < dfM[col_y],
        dfM[col_x] == dfM[col_y],
        dfM[col_x] > dfM[col_y],
    ]
    dfM.insert(4, col_shift_binary, np.select(conditions, ["+", "=", "-"]))
    grouped = dfM.groupby(by=["type", col_shift_binary])
    # statsAll = grouped.agg([np.size, np.mean, np.min, np.max, np.std])
    stats = grouped[col_diff].agg([np.size, np.mean, np.min, np.max, np.std])
    st.dataframe(stats)
    pos_neg_result(stats, "TP")
    pos_neg_result(stats, "FP")
    pos_neg_result(stats, "FPd")
    pos_neg_result(stats, "FPs")
    pos_neg_result(stats, "FN")
    pos_neg_result(stats, "TN")


@st.cache_data
def get_merged_record_pair_df(
    prj_id_0, prj_id_1, left_properties=None, right_properties=None
) -> DataFrame:
    if right_properties is None:
        right_properties = []
    if left_properties is None:
        left_properties = []
    with st.spinner("Fetching record pairs..."):
        df_record_pairs = get_record_pairs_as_dataframe(prj_id_0, left_properties)
    with st.spinner("Fetching record pairs 2..."):
        df_record_pairs2 = get_record_pairs_as_dataframe(prj_id_1, right_properties)
    parse_record_pair_df(df_record_pairs)
    parse_record_pair_df(df_record_pairs2)
    return merge_record_pair_df(df_record_pairs, df_record_pairs2)


def merge_record_pair_df(df: DataFrame, df2: DataFrame) -> DataFrame:
    df = prepare_for_merge(df)
    df2 = prepare_for_merge(df2)
    if df.empty:
        return df
    if df2.empty:
        return df2
    dfM = pd.merge(df, df2, how="inner", on=["ID0", "ID1"])
    dfM["type"] = dfM["type_" + get_state_or_default("reference_side", "x")]
    dfM.insert(3, "similarity_diff", dfM["similarity_y"] - dfM["similarity_x"])
    dfM.insert(7, "probability_diff", dfM["probability_y"] - dfM["probability_x"])
    return dfM


