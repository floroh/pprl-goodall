import os
import tempfile
from loguru import logger
from dotenv import load_dotenv

from goodall.models.services import ServiceStatus

load_dotenv(override=False)
logger.debug("loading env")

import mlflow
import pandas as pd
from mlflow import MlflowClient, MlflowException
from mlflow.utils.mlflow_tags import MLFLOW_PARENT_RUN_ID
from goodall.tracking.linkage_protocol_manager import PARAM_DATASET_RUN_ID

COL_DATASET_RUN_ID = "params.%s" % PARAM_DATASET_RUN_ID
COL_PARENT_RUN_ID = "tags.%s" % MLFLOW_PARENT_RUN_ID


def check_mlflow_server_connection() -> ServiceStatus:
    required_env_variables = [
        "MLFLOW_TRACKING_URI",
        "MLFLOW_TRACKING_USERNAME",
        "MLFLOW_TRACKING_PASSWORD"
    ]
    missing_env = False
    is_healthy = False
    for required_env_variable in required_env_variables:
        if required_env_variable not in os.environ:
            logger.warning(f"{required_env_variable} is not set")
            missing_env = True
        else:
            env_value = os.getenv(required_env_variable)
            if "PASSWORD" in required_env_variable:
                env_value = "*" * len(env_value)
            logger.debug(f"{required_env_variable} is {env_value}")
    if missing_env:
        is_healthy = False
    else:
        try:
            mlflow.search_experiments()
            is_healthy = True
        except MlflowException as e:
            logger.exception(f"mlflow test failed with {e.message}")
            is_healthy = False
    return ServiceStatus(
        name="Mlflow server",
        healthy=is_healthy,
        endpoint=os.getenv("MLFLOW_TRACKING_URI", None)
    )

def check_mlflow_artifact_storage_connection():
    """
    Minimal connectivity check to MLflow tracking + artifact storage.
    Creates a temp run, uploads a file, downloads it, and deletes the run.
    Returns True if successful, False otherwise.
    """
    client = MlflowClient()

    try:
        # Start an ephemeral run
        with mlflow.start_run(run_name="mlflow_healthcheck") as run:
            run_id = run.info.run_id

            try:
                client.list_artifacts(run_id)
            except MlflowException:
                raise
            # Create tiny temp file
            with tempfile.TemporaryDirectory() as tmpdir:
                file_path = os.path.join(tmpdir, "ping.txt")
                with open(file_path, "w") as f:
                    f.write("mlflow-ping")

                # Upload to artifact store
                mlflow.log_artifact(file_path)

                # Try downloading back via API
                download_dir = os.path.join(tmpdir, "download")
                os.makedirs(download_dir, exist_ok=True)
                client.download_artifacts(run_id, "ping.txt", dst_path=download_dir)

                downloaded_path = os.path.join(download_dir, "ping.txt")
                with open(downloaded_path) as f:
                    data = f.read().strip()

                # Success only if round-trip content matches
                is_healthy = data == "mlflow-ping"
        client.delete_run(run_id)

    except Exception as e:
        logger.error(f"MLflow artifact test failed: {e}")
        is_healthy = False
    return ServiceStatus(
        name="Mlflow artifact connection",
        healthy=is_healthy,
        endpoint=os.getenv("MLFLOW_S3_ENDPOINT_URL", None)
    )

def clean_experiment_run_df(df_runs: pd.DataFrame,
                            drop_slurm_params_columns: bool = True,
                            drop_mlflow_source_columns: bool = True,
                            drop_mlflow_clutter: bool = True,
                            drop_empty_columns: bool = True,
                            drop_times: bool = True,
                            ) -> pd.DataFrame:
    if drop_slurm_params_columns:
        drop_columns = [col for col in df_runs.columns if
                        col.startswith('params.') and 'slurm' in col]
        df_runs = df_runs.drop(columns=drop_columns)
    if drop_mlflow_source_columns:
        drop_columns = [col for col in df_runs.columns if
                        col.startswith('tags.mlflow.source.')]
        df_runs = df_runs.drop(columns=drop_columns)
    if drop_mlflow_clutter:
        drop_columns = [col for col in df_runs.columns if
                        col == 'artifact_uri'
                        or col == 'tags.mlflow.runName'
                        or col == 'tags.mlflow.user'
                        # or
                        ]
        df_runs = df_runs.drop(columns=drop_columns)
    if drop_empty_columns:
        df_runs = df_runs.dropna(axis=1, how='all')
        # df_runs = df_runs.replace('', pd.NA).dropna(axis=1, how='all')
    if drop_times:
        drop_columns = [col for col in df_runs.columns if
                        col in ["start_time", "end_time"]]
        df_runs = df_runs.drop(columns=drop_columns)
    return df_runs

def add_dataset_run_id_to_children(df_runs: pd.DataFrame,
                                   split: bool = False,
                                   ) -> tuple[pd.DataFrame | None, pd.DataFrame | None]:

    df = df_runs.copy()

    has_parent_col = COL_PARENT_RUN_ID in df.columns
    has_dataset_col = COL_DATASET_RUN_ID in df.columns

    if not has_parent_col and not has_dataset_col:
        return None, None

    if has_parent_col:
        # Candidate parents = no parent but dataset_run_id exists
        parent_mask = df[COL_PARENT_RUN_ID].isna() & df[COL_DATASET_RUN_ID].notna()
        parent_runs = df[parent_mask].copy()

        # Child runs = all other rows
        child_runs = df[~parent_mask].copy()

        # Map parent run_id -> dataset_run_id
        parent_map = parent_runs.set_index("run_id")[COL_DATASET_RUN_ID].to_dict()

        # Only children that have a parent need dataset_run_id filled
        child_with_parent_mask = child_runs[COL_PARENT_RUN_ID].notna()

        # Fill dataset_run_id for children with a parent
        child_runs.loc[child_with_parent_mask, COL_DATASET_RUN_ID] = (
            child_runs.loc[child_with_parent_mask].apply(
                lambda row: parent_map.get(row[COL_PARENT_RUN_ID], row.get(COL_DATASET_RUN_ID)),
                axis=1
            )
        )

        # Determine which parent runs were actually used in mapping
        used_parents = set(child_runs.loc[child_with_parent_mask, COL_PARENT_RUN_ID].dropna().unique())
        unused_parents_mask = ~parent_runs["run_id"].isin(used_parents)
        # Move unused parents to child_runs
        if unused_parents_mask.any():
            child_runs = pd.concat([child_runs, parent_runs[unused_parents_mask]]).sort_index()
            parent_runs = parent_runs[~unused_parents_mask]

        if split:
            return parent_runs, child_runs
        else:
            return pd.concat([parent_runs, child_runs]).sort_index(), None

    # No parent column but dataset_run_id exists → all children
    if has_dataset_col:
        return None, df

    return None, None