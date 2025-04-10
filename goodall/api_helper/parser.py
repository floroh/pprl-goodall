import pandas as pd
from pprl_data_owner_service_api_client import SerializableTable
from pprl_linkage_unit_service_api_client import BatchMatchProjectDto


def parse_serialized_table_to_dataframe(table: SerializableTable) -> pd.DataFrame:
    return parse_serialized_table_dict_to_dataframe(table.to_dict())


def parse_serialized_table_dict_to_dataframe(table: dict) -> pd.DataFrame:
    column_names = table["header"]
    df = pd.DataFrame(table["data"], columns=column_names)
    i = 0
    for column_type in table["types"]:
        if column_type == "DOUBLE":
            df[column_names[i]] = df[column_names[i]].astype(float)
        if column_type == "LONG":
            df[column_names[i]] = df[column_names[i]].astype(int)
        i += 1
    return df


def get_project_quality_results(project_json: BatchMatchProjectDto, report_name="Active") -> pd.DataFrame:
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
    except:
        return None


def remove_weighted_columns(df):
    weighted_cols = [col for col in df.columns if " (w)" in col]
    df = df.drop(columns=weighted_cols)
    return df
