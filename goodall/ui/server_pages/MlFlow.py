import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from goodall.tracking.mlflow_utils import add_dataset_run_id_to_children, \
    clean_experiment_run_df, COL_DATASET_RUN_ID
from goodall.ui.components.mlflow.mlflow import select_experiments, \
    select_runs, filter_by_column, select_datasets, render_mlflow_mlal
from goodall.ui.components.mlflow.mlflow_blocking_renderer import MlflowBlockingRenderer
from goodall.ui.components.mlflow.mlflow_dataset_renderer import MlflowDatasetRenderer
from goodall.ui.components.mlflow.mlflow_weight_renderer import MlflowWeightRenderer

load_dotenv(override=False)
selected_experiments = select_experiments()
if not selected_experiments:
    st.stop()
experiment_names = [e.name for e in selected_experiments]
selected_runs, _ = select_runs(experiment_names=experiment_names,
                               output_format="pandas")
if selected_runs is None or len(selected_runs) == 0:
    st.info("No runs selected")
    st.stop()

dataset_experiments = [exp for exp in selected_experiments if "datasets" in exp.name]
if len(dataset_experiments) > 0:
    selected_runs = filter_by_column(selected_runs, "metrics.size.total")
    selected_runs = filter_by_column(selected_runs, "metrics.overlap-relative.A-B")
    exclude_seed_efgh = st.toggle("Exclude seed efgh", True)
    exclude_seed_123 = st.toggle("Exclude seed 123", False)
    exclude_seed_456 = st.toggle("Exclude seed 456", True)
    only_min1E = st.toggle("Include only min1E", True)
    take_first_if_multiple_identical_names = st.toggle("Ensure dataset name is unique by keeping only the first", True)
    if exclude_seed_efgh:
        mask_keep = ~(
                selected_runs["params.dataset_name"].str.contains("seedefgh", na=False) |
                selected_runs["params.dataset_name"].str.contains("seed=efgh", na=False)
        )
        selected_runs = selected_runs[mask_keep]

    if exclude_seed_123:
        mask_keep = ~(
                selected_runs["params.dataset_name"].str.contains("seed123", na=False) |
                selected_runs["params.dataset_name"].str.contains("seed=123", na=False)
        )
        selected_runs = selected_runs[mask_keep]
    if exclude_seed_456:
        mask_keep = ~(
                selected_runs["params.dataset_name"].str.contains("seed456", na=False) |
                selected_runs["params.dataset_name"].str.contains("seed=456", na=False)
        )
        selected_runs = selected_runs[mask_keep]

    if only_min1E:
        mask_keep = (
                ~selected_runs["params.dataset_name"].str.contains("DatasetCsv", na=False) |
                selected_runs["params.dataset_name"].str.contains("min1E", na=False)
        )
        selected_runs = selected_runs[mask_keep]
    if take_first_if_multiple_identical_names:
        selected_runs = selected_runs.drop_duplicates(
            subset="params.dataset_name", keep="first"
        )

selected_runs = clean_experiment_run_df(selected_runs)
st.dataframe(selected_runs)
run_ids = selected_runs["run_id"].tolist()

default_mode = None
for selected_experiment in experiment_names:
    st.text(f"Experiment {selected_experiment}")
    if "dataset" in selected_experiment:
        default_mode = "Dataset"
        break
    if "blocking" in selected_experiment:
        default_mode = "Blocking"
        break
    if "test-linkage" in selected_experiment:
        default_mode = "Weight"
        break
sel_mode = st.segmented_control(
    "Mode",
    ["Dataset", "MLAL", "Weight", "Blocking"],
    default=default_mode
)
if not sel_mode:
    st.stop()

if sel_mode != "Dataset":
    _, df_children = add_dataset_run_id_to_children(selected_runs, split=True)
    df_children: pd.DataFrame = df_children
    only_finished_runs = st.sidebar.toggle("Include only finished runs", True)
    if only_finished_runs:
        df_children = df_children[df_children['status'] == "FINISHED"]
    st.info(f"{len(df_children)} remaining runs.")
    # df_children = clean_experiment_run_df(df_children)
    st.dataframe(df_children)
    dataset_run_ids, df_dataset_runs = select_datasets(df_children,
                                                       show_dataset_names=True)
    # st.subheader("Dataset runs")
    # st.dataframe(df_dataset_runs)
    # st.json(dataset_run_ids)
    if dataset_run_ids:
        df_children = df_children[df_children[COL_DATASET_RUN_ID].isin(dataset_run_ids)]
        st.info(f"{len(df_children)} remaining runs after dataset filtering.")
    st.dataframe(df_children)
    # st.subheader("Limit runs number")
    # run_limit = st.sidebar.slider("Limit runs", 1, len(df_children), 10)
    if len(df_children) > 1:
        run_limit = st.sidebar.slider("Limit runs", 1, len(df_children), len(df_children))
        df_children = df_children.head(run_limit)

    if sel_mode == "MLAL":
        render_mlflow_mlal(df_children, df_dataset_runs)
    elif sel_mode == "Weight":
        renderer = MlflowWeightRenderer(df_dataset_runs)
        renderer.render(df_children)
    elif sel_mode == "Blocking":
        renderer = MlflowBlockingRenderer(df_dataset_runs)
        renderer.render(df_children)

elif sel_mode == "Dataset":
    renderer = MlflowDatasetRenderer()
    renderer.render(selected_runs, run_ids)