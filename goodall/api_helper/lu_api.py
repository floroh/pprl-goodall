import logging
from typing import List

import pandas as pd
import pprl_linkage_unit_service_api_client as do
import pprl_linkage_unit_service_api_client as lu
import streamlit as st
from pprl_linkage_unit_service_api_client import RecordDto

from goodall.api_helper import do_api
from goodall.api_helper.pprl_clients import Service, get_client
from goodall.utils import flatten_dict

client = get_client(Service.Linkage_unit)
dataset_controller = lu.DatasetManagementApi(client)
project_controller = lu.ProjectBasedBatchMatchingApi(client)
config_controller = lu.ConfigurationManagementApi(client)
result_analysis_controller = lu.LinkageResultAnalysisApi(client)
evaluation_controller = lu.LinkageResultEvaluationApi(client)
multi_layer_protocol_controller = lu.MultiLayerProtocolsApi(client)

logger = logging.getLogger(__name__)


def create_encoded_dataset(plaintext_dataset_id: int,
                           dataset_name: str = "") -> lu.DatasetDto:
    return dataset_controller.add_dataset_description(lu.DatasetDto.from_dict({
        "plaintextDatasetId": plaintext_dataset_id,
        "datasetName": dataset_name
    }))


def insert_encoded_data(dataset_id: int, records: list[lu.RecordDto]):
    logger.info("Deleting previous dataset")
    dataset_controller.delete_all(dataset_id)
    logger.info("Adding ground truth")
    add_ground_truth_from_global_ids(dataset_id, records)
    lu_records = []
    for record in records:
        record.dataset_id = dataset_id
        record.id.blocks = [record.id.var_global]
        record.id.var_global = None
        lu_records.append(lu.RecordDto.from_dict(record.to_dict()))
    logger.info("Inserting " + str(len(lu_records)) + " records")
    return dataset_controller.insert_batch(lu_records)


def add_ground_truth_from_global_ids(dataset_id: int, records: list[do.RecordDto]):
    record_ids = []
    for record in records:
        record_id = lu.RecordIdDto.model_validate(
            {
                "local": record.id.local,
                "source": record.id.source,
                "global": record.id.var_global,
            }
        )
        record_ids.append(record_id)
    evaluation_controller.add_ground_truth_from_global_ids(dataset_id, record_ids)


def get_linkage_evaluation(project_id: str, plaintext_id: int) -> lu.AnalysisResultDto:
    plain_records = fetch_cached_encoded_dataset(plaintext_id)
    request = lu.AnalysisRequestDto.from_dict(
        {"projectId": project_id, "parameters": {"SIMULATE": "True"}}
    )
    return run_linkage_result_analysis(plain_records, request)


def run_linkage_result_analysis(plain_records: List[RecordDto],
                                request: lu.AnalysisRequestDto):
    plain_records_as_dict = [plain_record.to_dict() for plain_record in plain_records]
    return result_analysis_controller.run_linkage_result_analysis(
        lu.MatchResultAnalysisRequestDto.from_dict(
            {
                "analysisRequest": request,
                "matchResult": lu.MatchResultDto.from_dict(
                    {"records": plain_records_as_dict}
                ),
            }
        )
    )


@st.cache_data
def fetch_cached_encoded_dataset(plaintext_id):
    return do_api.fetch_encoded_dataset(plaintext_id,
                                        "DBSLeipzig/Plain/Selective",
                                        "exampleProject"
                                        )


def get_projects() -> list[lu.BatchMatchProjectDto]:
    return project_controller.find_all()


def get_project(project_id: str) -> lu.BatchMatchProjectDto:
    try:
        return project_controller.get(project_id=project_id)
    except:
        return None


def get_record_pairs_as_dataframe(project_id: str, properties: list) -> pd.DataFrame:
    pairs = get_record_pairs(project_id, properties)
    pairs_as_dict = [pair.to_dict() for pair in pairs]
    return pd.DataFrame(pairs_as_dict)


@st.cache_data
def get_record_pairs(project_id: str, properties: list) -> list[lu.RecordPairDto]:
    return result_analysis_controller.get_pairs(
        lu.ResultRequest.from_dict(
            {"projectId": project_id, "pairProperties": properties})
    )


def update_record_pairs(record_pairs: list[lu.RecordPairDto]):
    multi_layer_protocol_controller.update_record_pairs(record_pairs)


# def
def transform_records_to_dataframe(records: list[RecordDto]) -> pd.DataFrame:
    dicts = [flatten_dict(record.to_dict()) for record in records]
    df = pd.DataFrame(dicts)
    return df


def get_records_as_dataframe(dataset_id: int, limit: int = -1) -> pd.DataFrame:
    return transform_records_to_dataframe(get_records(dataset_id, limit=limit))


def get_records(dataset_id: int, limit: int = -1) -> list[RecordDto]:
    logging.info(f"Getting records for dataset {dataset_id} with limit {limit}")
    if limit >= 0:
        return dataset_controller.get_all(id_dataset=dataset_id, limit=limit)
    return dataset_controller.get_all(id_dataset=dataset_id)


@st.cache_data
def get_records_by_unique_id(record_ids: list[str]) -> list[RecordDto]:
    return dataset_controller.find_by_unique_ids(record_ids)


def get_config(method: str) -> lu.MatchingDto:
    return config_controller.get_matching(
        matcher_id_dto=lu.MatcherIdDto.from_dict({"method": method})
    )


def update_config(config: lu.MatchingDto):
    config_controller.update1(config)


def get_classifier_description(method: str) -> str:
    return config_controller.get_classifier_description(
        matcher_id_dto=lu.MatcherIdDto.from_dict({"method": method})
    ).classifier_description


def delete_project(project_id: str, delete_parents: bool = False):
    project_controller.delete(project_id=project_id, delete_parents=delete_parents)
    # response = requests.delete(
    #     get_matcher_endpoint() + 'project/' + project_id + '?deleteParents=' + str(delete_parents))
    # return response
