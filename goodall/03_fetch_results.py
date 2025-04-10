import argparse
import os

import numpy as np
import pandas as pd

from goodall.api_helper import lu_api, pm_api
from goodall.api_helper.parser import (
    parse_serialized_table_to_dataframe,
)
from goodall.api_helper.pprl_clients import Service
from goodall.multi_layer_evaluation.helper import get_run_description, \
    add_iteration, get_dataset_analysis_result, plot_quality_comparison

import plotly.io as pio

pio.templates.default = "plotly"
plaintext_dataset_id_names = {2030: "E1S", 2032: "E1M", 2034: "E1L", 2040: "E2S", 2042: "E2M"}

def get_run_results(dfRuns: pd.DataFrame, project_type: str):
    df_run_results = None
    for index, row in dfRuns.iterrows():
        try:
            # if index > 1:
            #     continue
            if index % 10 == 0:
                print("Processing project " + str(index) + ", " + row[project_type])
            description = get_run_description(row)
            project = lu_api.get_project(row[project_type])
            reports = (
                project.phases["CLASSIFICATION"]
                .report_groups["Linkage quality evaluation"]
                .reports
            )
            df_run_result = None
            for report in reports.values():
                if report.name == "Improved links history":
                    df_run_result = parse_serialized_table_to_dataframe(report.table)
                    df_run_result["type"] = description
                    # df_run_result = add_imbalance_info(df_run_result)
                    # print(df_report)

            df_run_result["project"] = row[project_type]
            df_run_result = add_iteration(df_run_result)
            df_run_results = pd.concat([df_run_results, df_run_result])
        except:
            print("Error processing project " + str(index) + ", " + row[project_type])

    print(df_run_results)
    return df_run_results

def get_abf_privacy_analysis(project_id_abf: str) -> pd.DataFrame:
    dataset_id_abf = lu_api.get_project(project_id_abf).dataset_id
    result = get_dataset_analysis_result(Service.Linkage_unit, dataset_id_abf)
    privacy_report = result.report_groups["all"].reports["AttributePrivacy"]
    privacy_result = parse_serialized_table_to_dataframe(privacy_report.table)
    privacy_result["abfProject"] = project_id_abf
    privacy_result["abfDatasetId"] = dataset_id_abf
    return privacy_result

def get_ppcr_privacy_analysis(project_id_ppcr: str, plaintext_dataset_id: str) -> pd.DataFrame:
    evaluation_result = lu_api.get_linkage_evaluation(
        project_id_ppcr, plaintext_dataset_id
    )
    # print(evaluation_result)
    kapr_report = evaluation_result.report_groups["Links"].reports[
        "Privacy Measure KAPR"
    ]
    kapr_result = parse_serialized_table_to_dataframe(kapr_report.table)
    kapr_result["ppcrProject"] = project_id_ppcr
    print(kapr_result)
    return kapr_result


def get_privacy_analysis(dfRuns: pd.DataFrame) -> pd.DataFrame:
    abf_results = None
    ppcr_results = None
    for index, row in dfRuns.iterrows():
        if not (row["rbfDatasetId"] == 2232 or row["rbfDatasetId"] == 2242):  # E1M or E2M
            continue
        if row["ppcrErr"] != 0.2:
            continue
        if row["ppcrBudget"] != 200:
            continue
        print(
            "Getting privacy results for "
            + str(index)
            + ": "
            + get_run_description(row)
        )
        plaintext_dataset_id = lu_api.get_project(row["rbfProject"]).dataset_id
        if plaintext_dataset_id - 2000 > 300:
            plaintext_dataset_id = plaintext_dataset_id - 300
        elif plaintext_dataset_id - 2000 > 200:
            plaintext_dataset_id = plaintext_dataset_id - 200
        project_id_ppcr = row["ppcrProject"]
        project_id_abf = row["abfProject"]

        ppcr_result = get_ppcr_privacy_analysis(project_id_ppcr, plaintext_dataset_id)
        ppcr_results = pd.concat([ppcr_results, ppcr_result])

        abf_result = get_abf_privacy_analysis(project_id_abf)
        abf_results = pd.concat([abf_results, abf_result])
    return abf_results, ppcr_results


def fetch_run_results(dfRuns: pd.DataFrame, project_type: str, output_directory: str):
    print("Getting results for " + project_type)
    df_run_results = get_run_results(dfRuns, project_type)
    df_run_results["project_type"] = project_type

    return df_run_results

def process_baseline_protocol_log(file_path: str) -> pd.DataFrame:
    columns = [
        "abfProject", "plaintextDatasetId", "abfDatasetId"
    ]
    df_runs = pd.read_csv(file_path)

    rows = []
    for index, row in df_runs.iterrows():
        protocol_id = row["protocolId"]
        protocol = pm_api.get_protocol(protocol_id)
        new_row = {
            "abfProject": protocol.layers[0].project_id,
            "plaintextDatasetId": protocol.plaintext_dataset_id,
            "abfDatasetId": protocol.initial_dataset_id,
        }
        rows.append(new_row)
    df = pd.DataFrame(rows, columns=columns)
    return df

def fetch_baseline_results(project_table_path: str, output_directory: str):
    dfRuns = pd.read_csv(project_table_path)
    df_run_results = None
    df_abf_results = None
    for index, row in dfRuns.iterrows():
        try:
            project = lu_api.get_project(row["abfProject"])
            reports = (
                project.phases["CLASSIFICATION"]
                .report_groups["Linkage quality evaluation"]
                .reports
            )
            df_run_result = None
            for report in reports.values():
                if report.name == "Improved links history":
                    df_run_result = parse_serialized_table_to_dataframe(report.table)
            df_run_result["plaintextDatasetId"] = row["plaintextDatasetId"]
            df_run_result["abfDatasetId"] = row["abfDatasetId"]
            df_run_results = pd.concat([df_run_results, df_run_result])

            if row["plaintextDatasetId"] == 2032:  # E1M
                df_abf_result = get_abf_privacy_analysis(row["abfProject"])
                df_abf_result["plaintextDatasetId"] = row["plaintextDatasetId"]
                df_abf_result.drop(columns=["Shannon-Entropy", "Norm-Shannon-Entropy", "abfProject"], inplace=True)
                df_abf_results = pd.concat([df_abf_results, df_abf_result])
        except:
            print("Error processing project " + str(index))
    df_run_results.to_csv(os.path.join(output_directory, "results.csv"), index=False)
    df_abf_results.to_csv(os.path.join(output_directory, "privacy_results_abf.csv"))

    print("ABF Baselines quality results:")
    df_run_results = df_run_results[df_run_results["#Improved"] == -1]
    df_run_results.replace({"plaintextDatasetId": plaintext_dataset_id_names},
                  inplace=True)
    print(df_run_results[["F1-score", "plaintextDatasetId"]])
    print("Privacy measures for ABF in Table 4:")
    df_abf_results.replace({"plaintextDatasetId": plaintext_dataset_id_names}, inplace=True)
    print(df_abf_results)
    return df_run_results

def process_protocol_log(file_path: str) -> pd.DataFrame:
    columns = [
        "rbfProject", "abfProject", "ppcrProject",
        "plaintextDatasetId", "rbfDatasetId",
        "rbfInitThreshold", "ppcrErr", "ppcrBudget", "repetition"
    ]
    df_runs = pd.read_csv(file_path)

    rows = []
    for index, row in df_runs.iterrows():
        protocol_id = row["protocolId"]
        protocol = pm_api.get_protocol(protocol_id)
        error_rate = protocol.layers[2].error_rate
        error_rate = 0.0 if error_rate is None or np.isnan(error_rate) else error_rate
        new_row = {
            "rbfProject": protocol.layers[0].project_id,
            "abfProject": protocol.layers[1].project_id,
            "ppcrProject": protocol.layers[2].project_id,
            "plaintextDatasetId": protocol.plaintext_dataset_id,
            "rbfDatasetId": protocol.initial_dataset_id,
            "rbfInitThreshold": protocol.layers[0].initial_threshold,
            "ppcrErr": error_rate,
            "ppcrBudget": protocol.layers[2].budget,
            "repetition": row["repetition"],
        }
        rows.append(new_row)
    df = pd.DataFrame(rows, columns=columns)
    return df

def fetch_results(project_table_path: str, output_directory: str):
    dfRuns = pd.read_csv(project_table_path)
    dfTotalRunResults = fetch_run_results(dfRuns, "rbfProject", output_directory)
    dfTotalRunResults.to_csv(os.path.join(output_directory, "results_per_iteration.csv"), index=False)
    print(dfTotalRunResults)

    df_privacy_abf, df_privacy_ppcr = get_privacy_analysis(dfRuns)
    if df_privacy_abf is not None:
        df_privacy_abf.to_csv(os.path.join(output_directory, "privacy_results_abf.csv"))
    if df_privacy_ppcr is not None:
        df_privacy_ppcr.to_csv(os.path.join(output_directory, "privacy_results_ppcr.csv"))

    print("Done!")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("experiment_set", help="Set of experiments for a paper figure (fig3, fig4_left, fig4_right, fig5)")  # Add arguments here
    args = parser.parse_args()
    experiment_set = args.experiment_set
    output_directory = os.path.join("results", experiment_set)
    if not os.path.exists(output_directory):
        raise RuntimeError("Result directory " + output_directory + " does not exist")

    # Parse protocols and get the relevant parameters and project IDs of the layers
    file_path = os.path.join(output_directory, 'protocol_log.csv')
    if experiment_set == "baselines":
        df_projects = process_baseline_protocol_log(file_path)
    else:
        df_projects = process_protocol_log(file_path)
    project_table_path = os.path.join(output_directory, 'projectTable.csv')
    df_projects.to_csv(project_table_path, index=False)

    if experiment_set == "baselines":
        fetch_baseline_results(project_table_path, output_directory)
    else:
        # Fetch quality development history and privacy analysis results from projects
        fetch_results(project_table_path, output_directory)

if __name__ == '__main__':
    main()
