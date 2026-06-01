import ast
import csv
import json
import re
from pathlib import Path
from typing import List, Tuple, Any
import numpy as np
import pandas as pd
from loguru import logger
from pprl_data_owner_service_api_client import SerializableTable, Tag, ReportGroup, \
    RecordDto, AttributeDto, RecordIdDto
from pprl_linkage_unit_service_api_client import BatchMatchProjectDto
from pprl_protocol_manager_service_api_client import MultiLayerProtocol

from goodall.utils.constants import ATTRIBUTE_ORDER, ATTRIBUTE_SHORT, \
    ATTRIBUTE_REPLACEMENTS, ATTRIBUTES_FOR_DISPLAY


def parse_serialized_table_to_dataframe(table: SerializableTable) -> pd.DataFrame:
    return parse_serialized_table_dict_to_dataframe(table.to_dict())


def parse_serialized_table_dict_to_dataframe(table: dict) -> pd.DataFrame:
    column_names = table["header"]
    df = pd.DataFrame(table["data"], columns=column_names)
    i = 0
    for column_type in table["types"]:
        if column_type == "DOUBLE":
            df[column_names[i]] = (
                df[column_names[i]]
                .replace("", np.nan)
                .replace("...", np.nan)
                .astype(float)
            )
        if column_type == "LONG":
            df[column_names[i]] = (
                df[column_names[i]]
                .replace("", np.nan)
                .replace("...", np.nan)
                .astype(int)
            )
        i += 1
    return df


def parse_record_pair_df(df: pd.DataFrame):
    if not df.empty:
        if "properties" in df.columns:
            df["active"] = df["properties"].apply(
                lambda props: "active" in props
                if isinstance(props, list)
                else [props == "active"]
            )
        if "tags" in df.columns:
            df["probability"] = df["tags"].apply(
                lambda tags: get_tag_value(tags, "PROBABILITY", True)
            )
            df["type"] = df["tags"].apply(lambda tags: get_tag_value(tags, "type", False))
            df["gtLabel"] = df["tags"].apply(
                lambda tags: get_tag_value(tags, "Groundtruth-Label", False)
            )


def parse_tag_list_to_df(tags: list[Tag]) -> pd.DataFrame:
    """Convert a list of Tag objects into a pandas DataFrame."""
    COL_TAG_NUMERIC = "tagNumeric"
    cols = ["id0", "id1", "attribute", "tag", "tagString", COL_TAG_NUMERIC, "Type",
            "Origin"]
    data = {
        "id0": [t.id0 for t in tags],
        "id1": [t.id1 for t in tags],
        "attribute": [t.attribute for t in tags],
        "tag": [t.tag for t in tags],
        "tagString": [t.string_value for t in tags],
        COL_TAG_NUMERIC: [t.numeric_value for t in tags],
        "Type": [t.type for t in tags],
        "Origin": [t.origin for t in tags],
    }

    df = pd.DataFrame(data, columns=cols)
    # Coerce numeric column to float (NaN for missing or invalid)
    df[COL_TAG_NUMERIC] = pd.to_numeric(df[COL_TAG_NUMERIC], errors="coerce")
    return df


def get_tag_value(tags, tag_name: str, numeric: bool = False):
    if tags is not None:
        for tag in tags:
            if tag["tag"] == tag_name:
                if numeric:
                    return tag["numericValue"]
                else:
                    return tag["stringValue"]
    return None


def get_report_output(report_groups: dict[str, ReportGroup],
                      report_name: str,
                      report_group_name: str = "all") \
        -> None | Tuple[str, pd.DataFrame | None]:
    try:
        report = report_groups[report_group_name].reports[report_name]
        if report.type == "TABLE":
            return report.report, parse_serialized_table_to_dataframe(report.table)
        elif report.type == "TEXT":
            return report.report, None
    except:
        logger.warning(f"Failed to parse TAG_BASED_DATASET_ANALYSIS result for "
                       f"report {report_name} in group {report_group_name}.")
    return None


def get_project_quality_results(
        project_json: BatchMatchProjectDto, report_name="Active"
) -> pd.DataFrame:
    try:
        table = (
            project_json.phases.get("CLASSIFICATION")
            .report_groups.get("Linkage quality evaluation")
            .reports.get(report_name)
            .table
        )
        df = parse_serialized_table_to_dataframe(table)
        df = remove_weighted_columns(df)
        return df
    except Exception:
        return None


def get_best_result_and_threshold_from_quality_overview(df: pd.DataFrame) -> Tuple[
    pd.DataFrame | None, float | None]:
    if df is not None:
        for i, desc in enumerate(df["Description"]):
            if isinstance(desc, str) and desc.startswith("Best"):
                match = re.search(r"\(([^)]+)\)", desc)
                if match:
                    try:
                        value = float(match.group(1))
                    except ValueError:
                        return None, None
                    df_row = df.drop(columns=["Description"]).iloc[[i]]
                    df_row = df_row.reset_index(drop=True)
                    return df_row, value
    return None, None


def remove_weighted_columns(df):
    weighted_cols = [col for col in df.columns if " (w)" in col]
    df = df.drop(columns=weighted_cols)
    return df


def process_dataset_dataframe(
        df: pd.DataFrame,
        clean_attribute_keys: bool = True,
        without_attribute_types: bool = True,
        order_attribute_columns: bool = True,
) -> pd.DataFrame:
    if clean_attribute_keys or without_attribute_types:
        df = clean_keys(df, clean_attribute_keys, without_attribute_types)
    if order_attribute_columns:
        df = order_columns(df)
    return df


def order_columns(
        df: pd.DataFrame, column_order: List[str] | None = None
) -> pd.DataFrame:
    if column_order is None:
        column_order = ATTRIBUTE_ORDER
    ordered_columns = [col for col in column_order if col in df.columns]
    remaining_columns = [col for col in df.columns if col not in ordered_columns]
    final_order = remaining_columns + ordered_columns
    return df[final_order]


def order_rows(
        df: pd.DataFrame,
        row_order: List[str] | None = None,
        attribute_column: str = "attribute",
) -> pd.DataFrame:
    if row_order is None:
        row_order = ATTRIBUTE_ORDER

    if attribute_column not in df.columns:
        raise ValueError(f"The DataFrame must have an '{attribute_column}' column.")

    valid_order = [attr for attr in row_order if attr in df[attribute_column].values]

    ordered_rows = df[df[attribute_column].isin(valid_order)]
    remaining_rows = df[~df[attribute_column].isin(valid_order)]

    ordered_rows = (
        ordered_rows.set_index(attribute_column).reindex(valid_order).reset_index()
    )
    final_df = pd.concat([ordered_rows, remaining_rows], ignore_index=True)
    return final_df


def clean_keys(
        df: pd.DataFrame,
        clean_attribute_keys: bool = True,
        without_attribute_types: bool = True,
) -> pd.DataFrame:
    """
    Cleans the keys (column names) of a DataFrame based on specified rules.

    Args:
        df (pd.DataFrame): The input DataFrame to clean.
        clean_attribute_keys (bool): If True, remove leading "attributes."
                                     from column names.
        without_attribute_types (bool): If True, drop columns ending with ".type" and
                                        remove ".value" suffix from column names
                                        starting with "attributes.".

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


def build_weight_string_and_attribute_set(weight_dict,
                                          digits: int = 2,
                                          exclude_attributes_with_weight_zero: bool = True):
    """
    weight_dict: dict like {"FIRSTNAME": 10.45, "MIDDLENAME": 3.2, ...}
    digits: number of decimal digits to format weights (default = 2)

    Returns:
        weight_string, attribute_set
    """

    parts_weight = []
    parts_attr = []

    # Normalize weight_dict keys with replacements
    normalized_weights = {}
    for key, value in weight_dict.items():
        normalized_key = ATTRIBUTE_REPLACEMENTS.get(key, key)
        normalized_weights[normalized_key] = value

    for attr in ATTRIBUTE_ORDER:
        if attr not in normalized_weights:
            continue  # omit missing attributes

        value = round(normalized_weights[attr], digits)
        if exclude_attributes_with_weight_zero:
            if value == 0:
                continue  # Omit 0-weight attributes

        # Build weight part
        value_str = f"{value:.{digits}f}"

        # Build attribute short form
        short = ATTRIBUTE_SHORT.get(attr)
        if short:
            parts_attr.append(short)
            parts_weight.append(f"{short}={value_str}")
        else:
            parts_attr.append(attr)

            parts_weight.append(f"{attr}={value_str}")

    weight_string = "|".join(parts_weight)
    attribute_set = "-".join(parts_attr)

    return weight_string, attribute_set


def get_weights_from_protocol_step_properties(protocol: MultiLayerProtocol) -> dict[str, float]:
    weights = {}
    for step in protocol.step_history:
        if step.type == "PREPARE_CONFIGS":
            for property_key in step.properties:
                if property_key.startswith("weight.") and "IGNORE" not in property_key:
                    weight = step.properties.get(property_key)
                    property_key = property_key.replace("weight.", "")
                    # if source specific weights: use t
                    if "." in property_key:
                        parts = property_key.split(".")
                        property_key = f"{parts[1]}.{parts[0]}"
                    attribute_name = ATTRIBUTE_REPLACEMENTS.get(property_key,
                                                                property_key)
                    weights[attribute_name] = float(weight)
            break
    return weights


def get_attributes_in_encoding(encoding: dict) -> list[str]:
    if encoding['@class'] == '.SourceSpecificEncoder':
        for source, encoder in encoding['encoders'].items():
            encoder_groups = encoder["encoderGroups"]
            break
    else:
        encoder_groups = encoding["encoderGroups"]
    # RBF encoding
    rbf_groups = [eg for eg in encoder_groups if eg.get("id", "") == "RBF"]
    if rbf_groups:
        encoders: dict[str, Any] = rbf_groups[0]["attributeEncoders"]
        attributes = encoders.keys()
        return get_sorted_attributes(list(attributes))
    raise NotImplementedError("Unsupported encoding.")


def get_sorted_attributes(attributes: list[str],
                          only_for_display: bool = False) -> list[str]:

    """
    Normalize attribute names using ATTRIBUTE_REPLACEMENTS and
    return a list sorted as follows:

    1) Attributes in ATTRIBUTE_ORDER, in that exact order.
    2) All unknown attributes, sorted alphabetically at the end.
    """

    # Normalize names first
    normalized = [ATTRIBUTE_REPLACEMENTS.get(a, a) for a in attributes]

    if only_for_display:
        normalized = [attr for attr in normalized if attr in ATTRIBUTES_FOR_DISPLAY]

    # Known attributes (preserve ATTRIBUTE_ORDER)
    ordered = []
    for attr in ATTRIBUTE_ORDER:
        if attr in normalized:
            ordered.append(attr)

    # Unknown attributes → alphabetical at the end
    known_set = set(ATTRIBUTE_ORDER)
    unknown = sorted(a for a in normalized if a not in known_set)

    return ordered + unknown

def get_attributes_for_display(attributes: list[str]) -> list[str]:
    attributes = [attr for attr in attributes if attr in ATTRIBUTES_FOR_DISPLAY]
    return get_sorted_attributes(attributes)


def load_dataset(dataset_folder: str | Path) -> list[RecordDto]:
    dataset_folder = Path(dataset_folder)
    csv_path = dataset_folder / "records.csv"
    schema_path = dataset_folder / "schema.json"

    # --- Load schema ---
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    columns = [col["name"] for col in schema["columns"]]

    # --- Read CSV and parse dynamically ---
    records: List[RecordDto] = []

    with open(csv_path, newline="", encoding=schema.get("charset", "utf-8")) as f:
        reader = csv.reader(f)

        if schema.get("header", False):
            next(reader)  # skip header if present

        for row in reader:
            row_data = dict(zip(columns, row))

            record_id_fields = {}
            attributes: dict[str, AttributeDto] = {}

            for col_name, value in row_data.items():
                if col_name == "IGNORE":
                    continue  # skip ignored columns

                if col_name.startswith("id."):
                    key = col_name.split(".", 1)[1]
                    if key == "global":
                        record_id_fields["global"] = value
                    elif key == "blocks":
                        blocks_list = parse_string_list(value)
                        if blocks_list:
                            record_id_fields["blocks"] = blocks_list
                    else:
                        record_id_fields[key] = value
                else:
                    attributes[col_name] = AttributeDto(type="STRING", value=value)
            record = RecordDto(
                id=RecordIdDto(**record_id_fields) if record_id_fields else None,
                attributes=attributes if attributes else None
            )
            records.append(record)
    return records


def parse_string_list(value: str) -> List[str]:
    """
    Safely parse a string representation of a list of strings.
    Returns an empty list if parsing fails or the format is invalid.
    """
    if not value or not isinstance(value, str):
        return []

    try:
        parsed = ast.literal_eval(value)
    except (ValueError, SyntaxError):
        return []

    # Ensure it's a list of strings
    if isinstance(parsed, list) and all(isinstance(x, str) for x in parsed):
        return parsed

    return []