import csv
import json
import os
import re
from pathlib import Path

import pandas as pd
from pprl_data_owner_service_api_client import DatasetManagementApi, DatasetAnalysisApi, \
    AnalysisResultDto, AnalysisRequestDto, DatasetDto
from loguru import logger

from goodall.api_helper.parser import process_dataset_dataframe, parse_tag_list_to_df
from goodall.api_helper.pprl_clients import get_client, Service
from goodall.result_analysis.dataset_analysis_result_parser import get_analysis_report
from goodall.utils.utils import flatten_dict


def get_dataset(service: Service, dataset_id: int) -> DatasetDto:
    dataset_controller = DatasetManagementApi(get_client(service))
    return dataset_controller.get_dataset_description(dataset_id)

def get_records_as_dataframe(
        service: Service, dataset_id: int, limit: int = -1
) -> pd.DataFrame:
    dataset_controller = DatasetManagementApi(get_client(service))
    logger.debug(f"Getting records for dataset {dataset_id} with limit {limit}")
    if limit >= 0:
        records = dataset_controller.get_all(dataset_id=dataset_id, limit=limit)
    else:
        records = dataset_controller.get_all(dataset_id=dataset_id)
    dicts = [flatten_dict(record.to_dict()) for record in records]
    df = pd.DataFrame(dicts)
    return df


def get_tags_as_dataframe(service: Service, dataset_id: int) -> pd.DataFrame:
    df_tags_analysis = get_tags_as_dataframe_from_analysis(service, dataset_id)
    logger.info(f"Got {len(df_tags_analysis)} tags from analysis.")
    return df_tags_analysis

def get_tags_as_dataframe_from_database(service: Service, dataset_id: int) -> pd.DataFrame:
    dataset_controller = DatasetAnalysisApi(get_client(service))
    tags = dataset_controller.get_tags(dataset_id)
    return parse_tag_list_to_df(tags)

def get_tags_as_dataframe_from_analysis(service: Service, dataset_id: int) -> pd.DataFrame:
    dataset_controller = DatasetAnalysisApi(get_client(service))
    analysis_result = dataset_controller.run_analysis(AnalysisRequestDto(
        datasetId=dataset_id,
        type="TAG_BASED_DATASET_ANALYSIS",
    ))
    _, df_tags = get_analysis_report(analysis_result, "Tags", "all")
    return df_tags


def get_dataset_analysis_result(
        service: Service,
        dataset_id: int,
        analysis_type: str = "DATASET_DESCRIPTION",
        parameters: dict[str, str] = None,
) -> AnalysisResultDto:
    analysis_controller = DatasetAnalysisApi(get_client(service))
    return analysis_controller.run_analysis(
        analysis_request_dto=AnalysisRequestDto.from_dict(
            ({"datasetId": dataset_id, "type": analysis_type, "parameters": parameters})
        )
    )


def write_dataset(df_records: pd.DataFrame, output_dir: Path,
                  skip_columns: list[str] | None = None):
    """
    Write cleaned dataset CSV and a schema.json to output_dir.

    - df_records: original DataFrame (contains columns like attributes.<NAME>.type and attributes.<NAME>.value)
    - output_dir: Path to directory where data.csv and schema.json will be written

    Produces:
    - data.csv  (no header, UTF-8, RFC4180-compatible quoting)
    - schema.json (structure as requested; columns listed in CSV order; attribute columns include "type" if not STRING)
    """
    if skip_columns is None:
        skip_columns = ["id.unique", "datasetId"]
    output_dir = Path(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    df_records = df_records.drop(
        columns=[col for col in skip_columns if col in df_records.columns],
        errors="ignore")

    # Extract attribute types from original dataframe BEFORE cleaning/dropping .type columns
    # We look for columns of the form: attributes.<NAME>.type
    attr_type_map: dict[str, str] = {}
    type_col_regex = re.compile(r"^attributes\.(?P<attr>.+)\.type$")

    for col in df_records.columns:
        m = type_col_regex.match(col)
        if not m:
            continue
        attr_name = m.group("attr")  # e.g., FIRSTNAME or CITY
        # find first non-null type value in this column if any; fall back to "STRING"
        raw_vals = df_records[col].dropna().unique()
        type_val = None
        if raw_vals.size > 0:
            # choose first unique - but if multiple appear we keep the first (you can refine this)
            type_val = str(raw_vals[0]).strip()
        if not type_val or type_val == "":
            type_val = "STRING"
        # After cleaning keys, the attribute column will become attr_name (clean_keys removes attributes. and .value)
        attr_type_map[attr_name] = type_val

    df_clean = process_dataset_dataframe(df_records.copy(), clean_attribute_keys=True,
                                         without_attribute_types=True,
                                         order_attribute_columns=True)

    csv_path = output_dir / "records.csv"
    df_clean.to_csv(
        csv_path,
        index=False,
        header=False,
        encoding="utf-8",
        quoting=csv.QUOTE_MINIMAL,
        lineterminator="\n",
    )

    schema = {
        "header": False,
        "charset": "UTF-8",
        "format": "RFC4180",
        "columns": []
    }

    for col in df_clean.columns:
        entry = {"name": col}
        if col in attr_type_map:
            attr_type = attr_type_map[col]
            if attr_type and attr_type.upper() != "STRING":
                entry["type"] = attr_type
        schema["columns"].append(entry)

    schema_path = output_dir / "schema.json"
    with schema_path.open("w", encoding="utf-8") as fh:
        json.dump(schema, fh, ensure_ascii=False, indent=2)

    return {"csv": str(csv_path), "schema": str(schema_path)}
