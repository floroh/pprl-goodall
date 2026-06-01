import pandas as pd
import pprl_linkage_unit_service_api_client as lu
from pprl_linkage_unit_service_api_client import RecordDto

import streamlit as st
from goodall.api_helper import do_api
from goodall.api_helper import lu_api


@st.cache_data
def fetch_encoded_dataset_cached(plaintext_id):
    return do_api.fetch_encoded_dataset(
        plaintext_id, "DBSLeipzig/Plain/Selective", "exampleProject"
    )


@st.cache_data
def get_records_by_unique_id(record_ids: list[str]) -> list[RecordDto]:
    return lu_api.dataset_controller.find_by_unique_ids(record_ids)


@st.cache_data
def get_record_pairs_cached(
    project_id: str, properties: list
) -> list[lu.RecordPairDto]:
    return lu_api.result_analysis_controller.get_pairs(
        lu.ResultRequest.from_dict(
            {"projectId": project_id, "pairProperties": properties}
        )
    )


@st.cache_data
def get_record_pairs_as_dataframe_cached(
    project_id: str, properties: list
) -> pd.DataFrame:
    return lu_api.get_as_dataframe(get_record_pairs_cached(project_id, properties))


def get_linkage_evaluation(project_id: str, plaintext_id: int) -> lu.AnalysisResultDto:
    plain_records = fetch_encoded_dataset_cached(plaintext_id)
    request = lu.AnalysisRequestDto.from_dict(
        {"projectId": project_id, "parameters": {"SIMULATE": "True"}}
    )
    return lu_api.run_linkage_result_analysis(plain_records, request)
