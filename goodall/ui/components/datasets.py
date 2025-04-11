import logging
from typing import Dict, List

import pandas as pd
import streamlit as st
from pprl_data_owner_service_api_client import AnalysisResultDto, DatasetAnalysisApi, \
    AnalysisRequestDto, DatasetManagementApi

import pprl_data_owner_service_api_client as do
import pprl_linkage_unit_service_api_client as lu
from goodall.api_helper import do_api
from goodall.api_helper import lu_api
from goodall.api_helper.lu_api import fetch_cached_encoded_dataset, \
    run_linkage_result_analysis
from goodall.api_helper.parser import parse_serialized_table_to_dataframe
from goodall.api_helper.pprl_clients import Service, get_client
from goodall.ui.PPRL_Services_UI import ATTRIBUTE_ORDER
from goodall.ui.streamlit_utils import get_state_or_default
from goodall.utils import flatten_dict

logger = logging.getLogger(__name__)


@st.cache_data
def get_dataset_ids(service: Service) -> list[int]:
    if service == Service.Linkage_unit:
        controller = lu.DatasetManagementApi(get_client(service))
    else:
        controller = do.DatasetManagementApi(get_client(service))
    return controller.get_dataset_ids()


@st.cache_data
def get_dataset_analysis_result(service: Service, dataset_id: int,
                                analysis_type: str = "DATASET_DESCRIPTION",
                                parameters: Dict[str, str] = None) -> AnalysisResultDto:
    analysis_controller = DatasetAnalysisApi(get_client(service))
    return analysis_controller.run_analysis(
        analysis_request_dto=AnalysisRequestDto.from_dict(
            ({"datasetId": dataset_id, "type": analysis_type,
              "parameters": parameters})
        )
    )

@st.cache_data
def get_records_as_dataframe(service: Service, dataset_id: int,
                             limit: int = -1) -> pd.DataFrame:
    dataset_controller = DatasetManagementApi(get_client(service))
    logging.info(f"Getting records for dataset {dataset_id} with limit {limit}")
    if limit >= 0:
        records = dataset_controller.get_all(id_dataset=dataset_id, limit=limit)
    else:
        records = dataset_controller.get_all(id_dataset=dataset_id)
    dicts = [flatten_dict(record.to_dict()) for record in records]
    df = pd.DataFrame(dicts)
    return df


def process_dataset_dataframe(df: pd.DataFrame,
                              clean_attribute_keys: bool = True,
                              without_attribute_types: bool = True,
                              order_attribute_columns: bool = True) -> pd.DataFrame:
    if clean_attribute_keys or without_attribute_types:
        df = clean_keys(df, clean_attribute_keys, without_attribute_types)
    if order_attribute_columns:
        df = order_columns(df)
    return df


def order_columns(df: pd.DataFrame,
                            column_order: List[str]|None = None) -> pd.DataFrame:
    if column_order is None:
        column_order = ATTRIBUTE_ORDER
    ordered_columns = [col for col in column_order if col in df.columns]
    remaining_columns = [col for col in df.columns if col not in ordered_columns]
    final_order = remaining_columns + ordered_columns
    return df[final_order]


def order_rows(df: pd.DataFrame,
               row_order: List[str] | None = None,
               attribute_column: str ="attribute") -> pd.DataFrame:
    if row_order is None:
        row_order = ATTRIBUTE_ORDER

    if attribute_column not in df.columns:
        raise ValueError(f"The DataFrame must have an '{attribute_column}' column.")

    valid_order = [attr for attr in row_order if attr in df[attribute_column].values]

    ordered_rows = df[df[attribute_column].isin(valid_order)]
    remaining_rows = df[~df[attribute_column].isin(valid_order)]

    ordered_rows = ordered_rows.set_index(attribute_column).reindex(valid_order).reset_index()
    final_df = pd.concat([ordered_rows, remaining_rows], ignore_index=True)
    return final_df

def clean_keys(df: pd.DataFrame,
               clean_attribute_keys: bool = True,
               without_attribute_types: bool = True) -> pd.DataFrame:
    """
    Cleans the keys (column names) of a DataFrame based on specified rules.

    Args:
        df (pd.DataFrame): The input DataFrame to clean.
        clean_attribute_keys (bool): If True, remove leading "attributes." from column names.
        without_attribute_types (bool): If True, drop columns ending with ".type" and
                                        remove ".value" suffix from column names starting with "attributes.".

    Returns:
        pd.DataFrame: A new DataFrame with cleaned keys.
    """
    cleaned_columns = {}

    for col in df.columns:
        original_col = col

        # Handle "attributes." prefix
        if clean_attribute_keys and col.startswith("attributes."):
            col = col[len("attributes."):]

        # Handle ".type" suffix
        if without_attribute_types and col.endswith(".type"):
            continue

        # Handle ".value" suffix
        if without_attribute_types and col.endswith(".value"):
            col = col[: -len(".value")]

        cleaned_columns[original_col] = col

    # Apply the cleaned column names and return the updated DataFrame
    df = df.rename(columns=cleaned_columns)

    # Drop columns that were removed due to ".type"
    if without_attribute_types:
        df = df[[col for col in cleaned_columns.values()]]

    return df


def get_dataset_privacy_analysis(project_id: str,
                                 report: str = "AttributePrivacy",
                                 ref_dataset_id: int = 0) -> pd.DataFrame:
    origin_dataset_id = lu_api.get_project(project_id).dataset_id
    df = _get_dataset_privacy_analysis(origin_dataset_id, report)
    if not df.empty:
        if ref_dataset_id != 0:
            df = add_reference_results(df, report, ref_dataset_id)
            df = df[~df["attribute"].str.contains("_DEV", na=False)]
            df = df[~df["attribute"].str.contains("FRQ", na=False)]
    return df


def add_reference_results(df_privacy_result: pd.DataFrame,
                          report: str = "AttributePrivacy",
                          ref_dataset_id: int = 2112) -> pd.DataFrame:
    result = _get_dataset_privacy_analysis(ref_dataset_id, report)
    result["type"] = "ref"
    df_privacy_result["type"] = "origin"
    return pd.concat([df_privacy_result, result], ignore_index=True)


def _get_dataset_privacy_analysis(dataset_id: int, report: str):
    result = get_dataset_analysis_result(Service.Linkage_unit, dataset_id,
                                         parameters={"runPerSource": "false",
                                          "refresh": "true"})
    try:
        privacy_report = result.report_groups["all"].reports[report]
    except TypeError:
        return pd.DataFrame()
    privacy_result = parse_serialized_table_to_dataframe(privacy_report.table)
    privacy_result.loc[privacy_result['attribute'] == 'PLZ', 'attribute'] = 'ZIP'
    privacy_result = order_rows(privacy_result)
    return privacy_result

def get_linkage_evaluation(project_id: str, plaintext_id: int) -> lu.AnalysisResultDto:
    plain_records = fetch_cached_encoded_dataset(plaintext_id)
    request = lu.AnalysisRequestDto.from_dict(
        {"projectId": project_id,
         "parameters": {"EXCLUDE_AVAILABILITY": "true"}}
    )
    return run_linkage_result_analysis(plain_records, request)


def get_ppcr_privacy_analysis(project_id_ppcr: str,
                              plaintext_dataset_id: int) -> pd.DataFrame:
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


def render_data_owner_dataset_description(dataset_id, index: int = 0,
                                          analysis_type: str = "DATASET_DESCRIPTION"):
    sel_show_records = st.checkbox("Show records", key=f"show_records{index}")
    if sel_show_records:
        sel_combine_sources = st.checkbox("Combine sources", key=f"combine_sources{index}")
        render_dataset_records(Service.Data_owner_1, dataset_id, ~sel_combine_sources)
    render_dataset_analysis_report(dataset_id, analysis_type=analysis_type)


def render_dataset_records(service: Service, dataset_id: int, separated_by_source: bool = True):
    df = get_records_as_dataframe(service, dataset_id,
                                  get_state_or_default("record_limit", 20))
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


def render_dataset_analysis_report(dataset_id: int,
                                   analysis_type: str = "DATASET_DESCRIPTION"):
    result = get_dataset_analysis_result(
        st.session_state["selected_service"], dataset_id, analysis_type=analysis_type
    )
    st.json(result.to_json(), expanded=False)
    for report_group in result.report_groups.values():
        if report_group.name == "all":
            is_expanded = True
        else:
            is_expanded = False
        with st.expander(report_group.name, expanded=is_expanded):
            for report in report_group.reports.values():
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
                            st.dataframe(dfReport, use_container_width=True)
