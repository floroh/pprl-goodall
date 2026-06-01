import json
import tempfile
from collections import defaultdict
from typing import Any, Tuple
from loguru import logger
import mlflow
import pandas as pd
from mlflow.entities import Experiment, Run
import streamlit as st
from pandas import DataFrame
from pprl_data_owner_service_api_client import AnalysisResultDto
from pprl_linkage_unit_service_api_client import BatchMatchProjectDto
from pprl_protocol_manager_service_api_client import MultiLayerProtocol

from goodall.api_helper.parser import parse_serialized_table_to_dataframe
from goodall.plotting.plot_definitions import get_plot_definition_by_mode
from goodall.plotting.quality_history_plotter import DataToShow, QualityHistoryPlotter
from goodall.result_analysis.multi_layer_evaluation.helper import build_df_runs, \
    get_run_description, add_iteration
from goodall.tracking.dataset_creation_manager import ARTIFACT_PATH_DATASET_DESCRIPTION
from goodall.tracking.experiment_modifier import THRESHOLDS_JSON, \
    load_artifact_as_dataframe, TAG_DATASET_NAME
from goodall.tracking.linkage_protocol_manager import \
    ARTIFACT_PATH_PROTOCOL_CONFIG_FINAL, ARTIFACT_PATH_MULTI_LAYER_FOLDER, PARAM_PROTOCOL_FILE
from goodall.tracking.mlflow_utils import COL_DATASET_RUN_ID, COL_PARENT_RUN_ID
from goodall.utils.constants import DATASET_NAME_MAPPING

# Result analysis
COL_MLFLOW_RUN_ID = "mlflow_run_id"


@st.cache_data
def get_run_dataset_description(run_id: str) -> AnalysisResultDto:
    description = get_artifact_dict(run_id, ARTIFACT_PATH_DATASET_DESCRIPTION)
    return AnalysisResultDto.model_validate(description)


@st.cache_data
def get_artifact_dict(run_id: str, artefact_location: str):
    with tempfile.TemporaryDirectory() as tmpdir:
        local_artifact = mlflow.artifacts.download_artifacts(run_id=run_id,
                                                             artifact_path=artefact_location,
                                                             dst_path=tmpdir)
        with open(local_artifact) as local_artifact_fd:
            return json.load(local_artifact_fd)


@st.cache_data
def get_project_dto(run_id: str, layer_name: str) -> BatchMatchProjectDto:
    description = get_artifact_dict(run_id, f"layer.{layer_name}.project.json")
    return BatchMatchProjectDto.model_validate(description)


@st.cache_data
def get_protocol_dto(run_id: str,
                     protocol_file: str | None = None) -> MultiLayerProtocol:
    artifact_path = f"{ARTIFACT_PATH_MULTI_LAYER_FOLDER}/{protocol_file}" \
        if protocol_file else ARTIFACT_PATH_PROTOCOL_CONFIG_FINAL
    description = get_artifact_dict(run_id, artifact_path)
    return MultiLayerProtocol.model_validate(description)


def show_mlflow_config():
    st.text(f"Tracking URI: {mlflow.config.get_tracking_uri()}")


def filter_by_column(df: pd.DataFrame, filter_col: str,
                     defaults: dict[str, list[Any]]| None = None) -> pd.DataFrame:
    if defaults is None:
        defaults = {}
    if filter_col in df.columns:
        options = df[filter_col].unique().tolist()
        default = defaults.get(filter_col, options)
        selection = st.multiselect(f"Filter on column {filter_col}", options,
                                   default=default)
        return df[df[filter_col].isin(selection)]
    else:
        st.warning(f"Column {filter_col} is not in {df.columns}")
    return df

def select_experiments(default_selection: list[str] | None = None) -> list[Experiment]:
    all_experiments = mlflow.search_experiments()
    all_experiments.sort(key=lambda e: e.name)

    def format_experiment(e: Experiment):
        return f"{e.name} (id={e.experiment_id})"

    if default_selection:
        # all_experiments_names = [e.name for e in all_experiments]
        # default_selection = [sel for sel in default_selection if sel in all_experiments_names]
        default_selection = [e for e in all_experiments if e.name in default_selection]
    selection = st.multiselect("Select experiments", all_experiments,
                               default=default_selection,
                               format_func=format_experiment)
    return selection


def select_datasets_from_experiments(experiment_names: list[str]) -> list[str]:
    runs = mlflow.search_runs(experiment_names=experiment_names,
                              output_format="list")
    parent_runs = [mlflow.get_parent_run(r.info.run_id) for r in runs]
    if len(parent_runs) != len(runs):
        st.warning("Not all runs have a parent run.")
        return []

    dataset_run_ids = []
    for idx, run in enumerate(runs):
        st.text(run)
        parent_run = parent_runs[idx]
        if parent_run:
            dataset_run_id = parent_run.data.params["dataset_run_id"]
            dataset_run_ids.append(dataset_run_id)
        else:
            st.warning(f"No parent run for {run.info.run_id}")
            dataset_run_ids.append(None)

    def format_experiment(e: Experiment):
        return f"{e.name} (id={e.experiment_id})"

    selection = st.multiselect("Select datasets", dataset_run_ids)
    return selection


@st.cache_data
def get_mlflow_run_cached(run_id: str | Any) -> Run:
    return mlflow.get_run(run_id)


@st.cache_data
def get_dataset_runs(
        df_runs: pd.DataFrame = None,
        dataset_run_ids: list[str] = None,
        include_dataset_names: bool = True,
        include_display_column: bool = False
) -> pd.DataFrame:
    """
    Returns a DataFrame with following columns:
    - 'run_id' always present
    - 'dataset_run_id' always present
    - 'dataset_name' optionally included if include_dataset_names=True
    - 'display_name' optionally included if include_display_column=True
    """
    if df_runs is None and dataset_run_ids is None:
        raise Exception("Either df_runs or run_ids must be given.")

    if not dataset_run_ids:
        dataset_run_ids = df_runs[COL_DATASET_RUN_ID].unique().tolist()
    dataset_run_ids.sort()
    if not include_dataset_names and not include_display_column:
        return pd.DataFrame({"run_id": df_runs["run_id"],
                             "dataset_run_id": dataset_run_ids})

    rows = []
    name_counts = defaultdict(int)
    for idx, dataset_run_id in enumerate(dataset_run_ids):
        run = get_mlflow_run_cached(dataset_run_id)
        run_id_series = df_runs.loc[
            df_runs[COL_DATASET_RUN_ID] == dataset_run_id, "run_id"]
        if run_id_series.empty:
            raise RuntimeError(f"No run_id found for dataset_run_id {dataset_run_id}")
        run_id = run_id_series.iloc[0]
        row = {
            "run_id": run_id,
            "dataset_run_id": dataset_run_id
        }
        dataset_name = get_dataset_short_name(run)
        if include_dataset_names:
            row["dataset_name"] = dataset_name
        if include_display_column:
            if dataset_name:
                name_counts[dataset_name] += 1
                suffix = f" ({name_counts[dataset_name]})" if name_counts[
                                                                  dataset_name] > 1 else ""
                display_name = f"{dataset_name}{suffix}"
            else:
                run_name = run.data.tags.get("mlflow.runName", dataset_run_id)
                display_name = f"{run_name}"

            row["display_name"] = display_name
        rows.append(row)

    return pd.DataFrame(rows)


def get_dataset_short_name(run: Run) -> str:
    dataset_name = run.data.params.get("dataset_name", None)
    dataset_name = dataset_name if dataset_name and dataset_name != "None" else None
    if not dataset_name:
        dataset_name = run.data.tags.get(TAG_DATASET_NAME, None)
        dataset_name = dataset_name if dataset_name and dataset_name != "None" else None
    if dataset_name:
        for subs, new_name in DATASET_NAME_MAPPING.items():
            if subs in dataset_name:
                size = run.data.metrics.get("size.total", None)
                if size:
                    size = f"{int(size / 1000)}"
                else:
                    size = "?"
                overlap = run.data.metrics.get("overlap-relative.A-B", None)
                if overlap == 0.1:
                    overlap = "S"
                elif overlap == 0.2:
                    overlap = "M"
                elif overlap == 0.3:
                    overlap = "L"
                elif overlap == 0.5:
                    overlap = "XL"
                else:
                    overlap = "?"
                dataset_name = f"{new_name}-{size}-{overlap}"
                break
    return dataset_name


def select_datasets(
        df_runs: pd.DataFrame,
        show_dataset_names: None | bool = True) -> tuple[list[str], pd.DataFrame]:
    if show_dataset_names is None:
        show_dataset_names = st.sidebar.toggle("Show dataset names if available", True)
    df_dataset_runs = get_dataset_runs(
        df_runs,
        include_dataset_names=show_dataset_names,
        include_display_column=show_dataset_names
    )
    if show_dataset_names:
        include_ger = st.toggle("Include GER", True)
        include_bw = st.toggle("Include BW", True)
        include_us_corr = st.toggle("Include NCVR with corruption", True)
        include_us_subgroups = st.toggle("Include NCVR subgroups", True)
        include_dataset_sizes = st.multiselect("Include dataset sizes", ["All", "2", "20", "100", "200"], default=["All"], accept_new_options=True)
        include_overlaps = st.multiselect("Include dataset overlaps", ["All", "S", "M", "L"], default=["All"], accept_new_options=True)

        if not include_bw:
            df_dataset_runs = df_dataset_runs[~df_dataset_runs["display_name"].str.startswith("BW")]
        if not include_ger:
            df_dataset_runs = df_dataset_runs[
                ~df_dataset_runs["display_name"].str.startswith("GER")]
        if not include_us_corr:
            df_dataset_runs = df_dataset_runs[
                ~df_dataset_runs["display_name"].str.startswith(("NC-T-", "NC-D-", "NC-F-"))
            ]
        if not include_us_subgroups:
            df_dataset_runs = df_dataset_runs[
                ~df_dataset_runs["display_name"].str.startswith("NC-") | \
                df_dataset_runs["display_name"].str.startswith(
                    ("NC-T-", "NC-D-", "NC-F-"))
            ]
        if include_dataset_sizes:
            if "All" not in include_dataset_sizes or len(include_dataset_sizes) > 1:
                include_dataset_sizes = [s for s in include_dataset_sizes if s != "All"]
                sizes_regex = "|".join([f"-{s}-" for s in include_dataset_sizes])
                st.info(sizes_regex)
                df_dataset_runs = df_dataset_runs[
                    df_dataset_runs["display_name"].str.contains(sizes_regex, regex=True)]

        if include_overlaps:
            if "All" in include_overlaps and len(include_overlaps) == 1:
                pass
            else:
                if "All" in include_overlaps:
                    include_overlaps = [s for s in include_overlaps if s != "All"]
                overlap_regex = "|".join([f"-{s}" for s in include_overlaps])
                st.info(overlap_regex)
                df_dataset_runs = df_dataset_runs[
                    df_dataset_runs["display_name"].str.contains(overlap_regex, regex=True)]

        df_dataset_runs.sort_values(by="display_name", inplace=True)
        options = [
            f"{row['display_name']} [{row['dataset_run_id']}]" for _, row in
            df_dataset_runs.iterrows()
        ]
        selection_display = st.multiselect("Select datasets", options)
        selection = [s.split('[')[-1][:-1] for s in selection_display]  # extract run_id
    else:
        selection = st.multiselect("Select datasets", df_dataset_runs)
    if not selection:
        selection = df_dataset_runs["dataset_run_id"].tolist()
    return selection, df_dataset_runs


def select_runs_list(runs: list[Run] | None = None,
                     experiment_names: list[str] | None = None,
                     ) -> list[Run]:
    if not runs:
        runs = mlflow.search_runs(experiment_names=experiment_names,
                                  output_format="list")

    def format_run(r: Run):
        return f"{r.info.run_name} {r.info.run_id} {r.info.start_time}"

    selection = st.multiselect("Select run", runs, format_func=format_run)
    if st.toggle("Select all runs"):
        return runs
    return selection


def select_runs(
        runs: list[Run] | None = None,
        experiment_names: list[str] | None = None,
        output_format: str = "list",  # "list" or "pandas"
) -> Tuple[list[Run] | pd.DataFrame, list[str]]:
    # Fetch runs if not provided
    if runs is None:
        runs = mlflow.search_runs(experiment_names=experiment_names,
                                  output_format=output_format)

    def format_run_obj(r: Run) -> str:
        return f"{r.info.run_name} ({r.info.run_id[:6]}) {r.info.start_time}"

    if isinstance(runs, pd.DataFrame):
        return render_dataset_run_selection(runs)
    else:
        select_all_runs = st.toggle("Select all runs", value=True)
        selection = st.multiselect("Select run", runs, format_func=format_run_obj, disabled=select_all_runs)
        run_list = runs if select_all_runs else selection
        return run_list, [r.info.run_id for r in run_list]


def render_dataset_run_selection(runs: pd.DataFrame) -> tuple[pd.DataFrame, list[Any]]:
    id_to_row = {}
    name_counts = defaultdict(int)
    options = []

    for _, row in runs.iterrows():
        dataset_name = row.get('params.dataset_name')
        if dataset_name and dataset_name != "None":
            name_counts[dataset_name] += 1
            suffix = f" ({name_counts[dataset_name]})" if name_counts[
                                                              dataset_name] > 1 else ""
            display_name = f"{dataset_name}{suffix}"
        else:
            run_name = row.get('tags.mlflow.runName') or str(row.name)
            display_name = f"{run_name}"
        run_id = row['run_id']
        display_name_with_id = f"{display_name} [{run_id}]"
        options.append(display_name_with_id)
        id_to_row[run_id] = row

    select_all_runs = st.toggle("Select all runs", value=True)
    selection_display = st.multiselect("Select run", options, disabled=select_all_runs)

    # Determine selected rows
    if select_all_runs:
        return runs, runs['run_id'].tolist()
    else:
        selected_ids = [s.split('[')[-1][:-1] for s in
                        selection_display]  # extract run_id
        selected_rows = [id_to_row[rid] for rid in selected_ids if rid in id_to_row]
        selected_df = pd.DataFrame(
            [row.to_dict() for row in selected_rows]).reset_index(drop=True)
    if selection_display:
        return selected_df, selected_df['run_id'].tolist()
    else:
        return selected_df, []


def build_run_results_per_iteration(df_runs: pd.DataFrame,
                                    layer_name: str = "RBF") -> pd.DataFrame:
    df_run_results = None
    for index, row in df_runs.iterrows():
        try:
            # if index > 1:
            #     continue
            if index % 10 == 0:
                logger.info(
                    f"Processing project {index + 1}/{len(df_runs)}, {row[layer_name]}")
            description = get_run_description(row)
            project = get_project_dto(row[COL_MLFLOW_RUN_ID], layer_name)
            # logger.info(project)
            reports = (
                project.phases["CLASSIFICATION"]
                .report_groups["Linkage quality evaluation"]
                .reports
            )
            df_run_result = None
            for report in reports.values():
                if report.name == "Improved links history":
                    df_run_result = parse_serialized_table_to_dataframe(
                        report.table)
                    df_run_result["type"] = description
                    # df_run_result = add_imbalance_info(df_run_result)
                    # print(df_report)

            df_run_result["project"] = row[layer_name]
            df_run_result = add_iteration(df_run_result)
            df_run_results = pd.concat([df_run_results, df_run_result])
        except Exception as e:
            logger.error(
                "Error processing project " + str(index) + ", " + row[layer_name])
            logger.exception(e)
    logger.info("Finished fetching results per iteration.")
    df_run_results["layer_name"] = layer_name
    return df_run_results


def render_mlflow_mlal(df_children: pd.DataFrame, df_dataset_runs: pd.DataFrame):
    protocols = []
    raw_protocols = []
    pt_dataset_id_mapping = {}
    progress_bar = st.progress(0)
    status_text = st.empty()
    total = len(df_children)
    for i, (_, row) in enumerate(df_children.iterrows(), start=1):
        progress_bar.progress(i / total)
        status_text.text(f"Processing {i}/{total} ({(i / total) * 100:.1f}%)")
        protocol_file = row[f"params.{PARAM_PROTOCOL_FILE}"]
        protocol_file = str(protocol_file) if pd.notna(protocol_file) else None
        parent_run_id = str(row[COL_PARENT_RUN_ID]) if pd.notna(
            row[COL_PARENT_RUN_ID]) else None
        raw_protocols.append(
            get_protocol_dto(parent_run_id, protocol_file=protocol_file))

        run_id = str(row["run_id"]) if pd.notna(row["run_id"]) else None
        protocol = get_protocol_dto(run_id)
        dataset_run_id = str(row[COL_DATASET_RUN_ID]) if pd.notna(
            row[COL_DATASET_RUN_ID]) else None
        dataset_run_id_series = df_dataset_runs.loc[
            df_dataset_runs["dataset_run_id"] == dataset_run_id, "dataset_run_id"]
        if not dataset_run_id_series.empty:
            dataset_name = f"ds={dataset_run_id_series.iloc[0]}"
            pt_dataset_id_mapping[protocol.plaintext_dataset_id] = dataset_name
        protocols.append(protocol)
    df_runs = build_df_runs(protocols, raw_protocols,
                            plaintext_dataset_id_mapping=pt_dataset_id_mapping)
    df_runs[COL_MLFLOW_RUN_ID] = df_children["run_id"].tolist()
    st.dataframe(df_runs)

    categories = ["ppcrErr", "ppcrBudget", "repetition", "plaintextDatasetId"]
    st.header("Dataset Summary & Filters")
    metric_cols = st.columns(len(categories))
    for i, col in enumerate(categories):
        with metric_cols[i]:
            counts = df_runs[col].value_counts().sort_index()
            logger.info(counts)
            n_unique = len(counts)
            val_metrics_cols = st.columns(
                min(n_unique + 1, 5))  # show up to 5 metrics side by side
            val_metrics_cols[0].metric(label=f"Distinct: {col}", value=n_unique)
            for j, (val, count) in enumerate(counts.items(), start=1):
                # if j >= len(val_metrics_cols):
                #     break
                val_metrics_cols[j % len(val_metrics_cols)].metric(label=str(val),
                                                                   value=count)
            # for ival, col_val in enumerate(val_metrics_cols):
            #     val_metrics_cols[ival + 1].metric(label=str(unique_vals[ival]),
            #                                       value=counts.iloc(ival))

    filter_cols = st.columns(len(categories))
    filters = {}
    for i, col in enumerate(categories):
        options = sorted(df_runs[col].unique().tolist())
        selected = filter_cols[i].multiselect(f"Select {col}", options, default=options)
        filters[col] = selected

    filtered_df = df_runs.copy()
    for col, selected in filters.items():
        filtered_df = filtered_df[filtered_df[col].isin(selected)]
    st.dataframe(filtered_df)
    continue_with_plotting = st.toggle("Continue with plotting")
    if continue_with_plotting:
        df_result_history = build_run_results_per_iteration(filtered_df, "RBF")
        st.dataframe(df_result_history)

        plot_mode = st.pills("Plot mode",
                             options=[DataToShow.BUDGET_THRESHOLD,
                                      DataToShow.BUDGET_DATASET,
                                      DataToShow.ERROR, DataToShow.BUDGET,
                                      DataToShow.THRESHOLD],
                             format_func=lambda x: x.name)
        plotter = QualityHistoryPlotter(get_plot_definition_by_mode(plot_mode))
        fig = plotter.create_figure(df_result_history, filtered_df)
        st.plotly_chart(fig)



@st.cache_data
def get_df_thresholds_single_run(run_id: str) -> DataFrame:
    logger.info(f"Fetching threshold dataframe for run_id={run_id}")
    run = mlflow.get_run(run_id)
    df_threshold = load_artifact_as_dataframe(run, THRESHOLDS_JSON)
    df_threshold["run_id"] = run_id
    return df_threshold

@st.cache_data
def get_df_thresholds(run_ids: list[str]) -> pd.DataFrame:
    df_thresholds = None
    for run_id in run_ids:
        df_threshold = get_df_thresholds_single_run(run_id)
        if df_thresholds is None:
            df_thresholds = df_threshold
        else:
            df_thresholds = pd.concat([df_thresholds, df_threshold])
    return df_thresholds