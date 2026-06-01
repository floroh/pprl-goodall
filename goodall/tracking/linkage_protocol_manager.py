import json
import os
import shutil
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Any

import mlflow
from loguru import logger
from mlflow.data.code_dataset_source import CodeDatasetSource
from mlflow.data.meta_dataset import MetaDataset
from pprl_protocol_manager_service_api_client import MultiLayerProtocol, DatasetCsvDto, \
    DatasetDto, ProtocolAnalysisRequestDto

from goodall.api_helper import do_api, common_api, pm_api, lu_api
from goodall.api_helper.parser import get_project_quality_results, \
    parse_serialized_table_to_dataframe, \
    get_best_result_and_threshold_from_quality_overview
from goodall.api_helper.pm_api import create_protocol
from goodall.api_helper.pprl_clients import Service

from goodall.models.experiment_definitions import LinkageProtocolConfig, InputDatasets
from goodall.tracking.dataset_creation_manager import DatasetCreationManager, \
    ARTIFACT_PATH_DATASET, PARAM_DATASET_NAME, ARTIFACT_PATH_ANALYSIS
from goodall.tracking.mlflow_artifact_manager import MLflowArtifactManager

TAG_EXCLUDE_LOGGING = "exclude_tag_logging"

ARTIFACT_PATH_PROTOCOL_CONFIG = "protocol_config.json"  # Scheduled
ARTIFACT_PATH_PROTOCOL_CONFIG_FINAL = "protocol_config_final.json"  # After Execution
ARTIFACT_PATH_MULTI_LAYER_FOLDER = "multi_layer_protocols"
PARAM_DATASET_RUN_ID = "dataset_run_id"
PARAM_DATASET_ID = "dataset_id"
PARAM_PROTOCOL_FILE = "protocol_file"


class LinkageProtocolManager:

    @staticmethod
    def _schedule_one(dataset_run_id: str, config: LinkageProtocolConfig):
        """Schedule a single dataset run and return run_id (or raise)."""
        logger.info(f"Scheduling dataset_run_id {dataset_run_id}")
        with mlflow.start_run():
            mlflow.log_param(PARAM_DATASET_RUN_ID, dataset_run_id)
            if not config.input.import_plain_datasets_from_mlflow:
                dataset_run = mlflow.get_run(dataset_run_id)
                i = 0
                while (v := dataset_run.data.params.get(f"datasetId.{i}")) is not None:
                    last_stage_dataset_id = v
                    i += 1
                mlflow.log_param(PARAM_DATASET_ID, last_stage_dataset_id)
            mlflow.log_dict(config.model_dump(), ARTIFACT_PATH_PROTOCOL_CONFIG)
            mlflow.log_dict(
                config.config.model_dump(),
                str(Path(ARTIFACT_PATH_MULTI_LAYER_FOLDER, "0.json"))
            )
            if config.tags:
                mlflow.set_tags(config.tags)
            if config.logging_config:
                if config.logging_config.exclude_tags:
                    mlflow.log_param(TAG_EXCLUDE_LOGGING, True)
            _set_linkage_status("scheduled")
            run_id = mlflow.active_run().info.run_id
            mlflow.end_run(status="SCHEDULED")
            return run_id

    def schedule(self, config: LinkageProtocolConfig) -> list[str]:
        protocol: MultiLayerProtocol = config.config
        if not protocol:
            raise RuntimeError("Pipeline definition is missing")
        _preparing_dataset_run_ids(config.input)

        run_ids = []
        max_workers = getattr(config, "max_workers", None) or min(32, (
                os.cpu_count() or 4) * 2)
        logger.debug(f"Using {max_workers} workers for scheduling the runs for "
                     f"{len(config.input.run_ids)} datasets.")
        with ThreadPoolExecutor(max_workers=max_workers) as exe:
            futures = {
                exe.submit(self._schedule_one, dataset_run_id, config): dataset_run_id
                for dataset_run_id in config.input.run_ids}
            for fut in as_completed(futures):
                ds_id = futures[fut]
                try:
                    run_id = fut.result()
                    run_ids.append(run_id)
                    logger.info(f"Scheduled run for dataset {ds_id} -> run_id={run_id}")
                except Exception as e:
                    logger.exception(f"Failed to schedule dataset {ds_id}: {e}")

        return run_ids

    def execute(self, run_ids: list[str]) -> list[str]:
        finished_run_ids = []
        artifact_manager = MLflowArtifactManager()
        for idx, run_id in enumerate(run_ids, start=1):
            run_exit_status = "FINISHED"
            with mlflow.start_run(run_id=run_id):
                logger.info(f"Executing scheduled run {run_id} ({idx}/{len(run_ids)})")
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                self.log_slurm_params(f"{timestamp}.")
                active_run = mlflow.active_run()
                exp_id = active_run.info.experiment_id
                mlflow.set_experiment(experiment_id=exp_id)
                dataset_run_id = active_run.data.params.get(PARAM_DATASET_RUN_ID)
                tmp_base_dir_host = os.getenv("MLFLOW_EXPERIMENT_TMP_DIR")
                with tempfile.TemporaryDirectory(prefix="protocol_",
                                                 dir=tmp_base_dir_host) as tmpdir:
                    tmp_path = Path(tmpdir)
                    try:
                        # Add plaintext dataset if needed
                        plaintext_dataset_id = active_run.data.params.get(PARAM_DATASET_ID)
                        if plaintext_dataset_id:
                            plaintext_dataset_id = int(plaintext_dataset_id)
                            logger.info(
                                f"Using plaintext dataset {plaintext_dataset_id} which"
                                f" is expected to be present in the data owner services"
                            )
                        else:
                            logger.info("Adding plaintext dataset to data owner.")
                            artifact_manager.download_artifact(run_id=dataset_run_id,
                                                               artifact_path=ARTIFACT_PATH_DATASET,
                                                               dst_path=tmpdir)
                            dataset_run = mlflow.get_run(dataset_run_id)
                            dataset_name = dataset_run.data.params[PARAM_DATASET_NAME]
                            dataset_path = tmp_path / Path(ARTIFACT_PATH_DATASET)
                            if tmp_base_dir_host is not None:
                                tmp_base_dir_container = os.getenv(
                                    "PPRL_SERVICES_PROTOCOL_MANAGER_TMP_DIR")
                                if tmp_base_dir_container is not None:
                                    logger.info(
                                        f"Mapping dataset_path from host to container: {tmp_base_dir_host} -> {tmp_base_dir_container}")
                                    dataset_path = Path(
                                        tmp_base_dir_container) / tmp_path.relative_to(
                                        Path(tmp_base_dir_host).absolute()) / Path(
                                        ARTIFACT_PATH_DATASET)
                            start_time = time.perf_counter()

                            plaintext_dataset_id = pm_api.do_preparation_controller.insert_from_csv(
                                DatasetCsvDto(
                                    path=str(dataset_path),
                                    datasetDto=DatasetDto(datasetName=dataset_name)
                                ))
                            mlflow.log_metric("runtime.datasetimport",
                                              time.perf_counter() - start_time)

                        # TODO Add encoding/matching configs to services

                        # Add protocol to protocol manager service
                        protocol_dir = tmp_path / Path("protocols")
                        artifact_manager.download_artifact(run_id=run_id,
                                                           artifact_path=ARTIFACT_PATH_MULTI_LAYER_FOLDER,
                                                           dst_path=str(protocol_dir))
                        for protocol_file in os.listdir(protocol_dir):
                            with mlflow.start_run(experiment_id=exp_id,
                                                  parent_run_id=run_id, nested=True):
                                exclude_tag_logging = active_run.data.params.get(
                                    "exclude_tag_logging", False)
                                logger.info("Starting protocol execution.")
                                protocol_run_exit_status = self.execute_protocol_run(
                                    artifact_manager,
                                    dataset_run_id,
                                    plaintext_dataset_id,
                                    protocol_dir,
                                    protocol_file,
                                    exclude_tag_logging=exclude_tag_logging)
                                if protocol_run_exit_status != "FINISHED":
                                    raise Exception("Child protocol failed.")
                        _set_linkage_status("finished")
                    except Exception as e:
                        logger.error(f"Failed: {e}")
                        import traceback
                        tb_str = traceback.format_exc()
                        mlflow.log_text(tb_str, "exception_traceback.txt")
                        mlflow.log_metric("runtime",
                                          time.perf_counter() - start_time)
                        run_exit_status = "FAILED"
                    finally:
                        logger.info("Logging logfiles")
                        self.log_mongo_logfile(artifact_manager,
                                               log_dir_postfix=f".{timestamp}")
                        self.log_protocol_logfiles(artifact_manager,
                                                   log_dir_postfix=f".{timestamp}")
                        self.log_slurm_logfiles(artifact_manager,
                                                log_dir_postfix=f".{timestamp}")
                        mlflow.end_run(run_exit_status)
                finished_run_ids.append(active_run.info.run_id)
        return finished_run_ids

    def execute_protocol_run(self, artifact_manager: MLflowArtifactManager,
                             dataset_run_id: Any | None, plaintext_dataset_id: int,
                             protocol_dir: Path, protocol_file: str,
                             exclude_tag_logging: bool = False) -> str:
        mlflow.log_param(PARAM_PROTOCOL_FILE, protocol_file)
        run_exit_status = "FINISHED"
        self.log_slurm_params()
        start_time = time.perf_counter()
        try:
            with open(protocol_dir / Path(protocol_file), "r") as file:
                payload = file.read()
                protocol = MultiLayerProtocol.model_validate_json(
                    payload)
            protocol.plaintext_dataset_id = plaintext_dataset_id
            protocol.initial_dataset_id = None
            source = CodeDatasetSource(
                tags={"run_id": dataset_run_id})
            meta_dataset = MetaDataset(source=source,
                                       name=f"run_id:{dataset_run_id}")
            mlflow.log_input(meta_dataset, "dataset")

            logger.info(f"Creating protocol from {protocol_file}")

            protocol = create_protocol(protocol)

            # Execute protocol
            logger.info(f"Running protocol {protocol.protocol_id}")
            protocol = pm_api.run_protocol_no_stop(protocol.protocol_id)

            mlflow.log_metric("runtime",
                              time.perf_counter() - start_time)
            # Logging results
            self.log_protocol_result(protocol, artifact_manager,
                                     exclude_tag_logging=exclude_tag_logging)
            _set_linkage_status("finished")
        except Exception as e:
            logger.error(f"Failed: {e}")
            import traceback
            tb_str = traceback.format_exc()
            mlflow.log_text(tb_str, "exception_traceback.txt")
            mlflow.log_metric("runtime",
                              time.perf_counter() - start_time)
            _set_linkage_status("failed")
            run_exit_status = "FAILED"
        finally:
            # mlflow.set_tags(mlflow.get_parent_run(mlflow.active_run().info.run_id).data.tags)
            logger.info("Logging runtime and logfiles")
            self.log_protocol_logfiles(artifact_manager)
            self.log_slurm_logfiles(artifact_manager)
            mlflow.end_run(run_exit_status)
        return run_exit_status

    @staticmethod
    def log_slurm_params(prefix: str = ""):
        if os.getenv("SLURM_JOB_ID", None):
            mlflow.log_param(f"{prefix}slurm_job_id", os.getenv("SLURM_JOB_ID"))
        if os.getenv("SLURM_HOSTNAME", None):
            mlflow.log_param(f"{prefix}slurm_hostname", os.getenv("SLURM_HOSTNAME"))

    @staticmethod
    def log_protocol_result(protocol: MultiLayerProtocol,
                            artifact_manager: MLflowArtifactManager,
                            exclude_tag_logging: bool = False):
        mlflow.log_dict(protocol.model_dump(), ARTIFACT_PATH_PROTOCOL_CONFIG_FINAL)
        upper_project_id = protocol.layers[0].project_id
        upper_project = lu_api.get_project(upper_project_id)
        df_quality_active = get_project_quality_results(upper_project)
        metrics = {
            "recall": df_quality_active.loc[0, "recall"],
            "precision": df_quality_active.loc[0, "precision"],
            "f1-score": df_quality_active.loc[0, "F1-score"]
        }
        df_quality_overview = get_project_quality_results(upper_project,
                                                          report_name="Overview")
        df_best, thr = get_best_result_and_threshold_from_quality_overview(
            df_quality_overview)
        if df_best is not None:
            metrics['bestthr'] = thr
            metrics['recall.bestthr'] = df_best.loc[0, "recall"]
            metrics['precision.bestthr'] = df_best.loc[0, "precision"]
            metrics['f1-score.bestthr'] = df_best.loc[0, "F1-score"]
        mlflow.log_metrics(metrics)

        with tempfile.TemporaryDirectory(prefix="protocol_result_") as tmpdir:
            tmp_path = Path(tmpdir)

            for layer in protocol.layers:
                logger.info(f"Logging artifacts of layer {layer.name}")
                project = lu_api.get_project(layer.project_id)
                mlflow.log_dict(
                    project.model_dump(), f"layer.{layer.name}.project.json"
                )
                # Log encoding config
                logger.debug(f"Logging encoding config of layer {layer.name}")
                e_config = do_api.get_config(layer.encoding_method)
                mlflow.log_dict(e_config.model_dump(),
                                f"layer.{layer.name}.encoding.json")
                encoding_config = json.loads(e_config.config)
                mlflow.log_dict(encoding_config,
                                f"layer.{layer.name}.encoding.config.json")

                # Log matching config
                logger.debug(f"Logging matching config of layer {layer.name}")
                m_config = lu_api.get_config(project.method)
                mlflow.log_dict(m_config.model_dump(),
                                f"layer.{layer.name}.matching.json")
                matching_config = json.loads(m_config.config)
                mlflow.log_dict(matching_config,
                                f"layer.{layer.name}.matching.config.json")
                classifier_description = lu_api.get_classifier_description(
                    project.method)
                mlflow.log_text(classifier_description,
                                f"layer.{layer.name}.classifier.txt")

                # Log encoded dataset description
                logger.info("Logging dataset analysis result")
                dataset_analysis = common_api.get_dataset_analysis_result(
                    Service.Linkage_unit, project.dataset_id,
                    parameters={"includeAdditionalResults": "true"})
                mlflow.log_dict(dataset_analysis.model_dump(),
                                f"{ARTIFACT_PATH_ANALYSIS}"
                                f"/layer.{layer.name}.dataset_description.json")

                # Log pairs
                logger.debug(f"Logging pairs of layer {layer.name}")
                df_pairs = lu_api.get_record_pairs_as_dataframe(
                    layer.project_id, ["ALL"]
                )
                logger.debug(f"Got {df_pairs.size} pairs.")
                pairs_file_path = tmp_path / Path(f"layer.{layer.name}.pairs.csv")
                logger.info("Logging pairs csv")
                df_pairs.to_csv(pairs_file_path, index=False, encoding="utf-8")
                artifact_manager.log_artifact(str(pairs_file_path), "", compress=True)

            # Log combined tags from the protocol
            if exclude_tag_logging:
                logger.info("Skip logging protocol tags, due to experiment flag/tag.")
            else:
                logger.info("Fetching protocol tags")
                table = pm_api.protocol_analyzer_controller.get_tags_from_protocol_as_table(
                    ProtocolAnalysisRequestDto(protocolId=protocol.protocol_id,
                                               parameters={
                                                   "skipDataOwnerTags": "true"}))
                df_tags = parse_serialized_table_to_dataframe(table)
                tag_file_path = tmp_path / Path("tags.csv")
                logger.info("Logging tag csv")
                df_tags.to_csv(tag_file_path, index=False, encoding="utf-8")
                artifact_manager.log_artifact(str(tag_file_path),
                                              ARTIFACT_PATH_ANALYSIS,
                                              compress=True)

    @staticmethod
    def log_mongo_logfile(artifact_manager: MLflowArtifactManager,
                          log_dir_postfix: str = ""):
        if os.getenv("PPRL_MONGODB_LOCATION", None):
            mongodb_location = Path(os.getenv("PPRL_MONGODB_LOCATION"))
            mongodb_log_path = mongodb_location / Path("mongodb.log")
            if mongodb_log_path.exists():
                artifact_manager.log_artifact(
                    mongodb_log_path, artifact_path=f"logs{log_dir_postfix}",
                    compress=False
                )
            else:
                logger.warning(f"No MongoDB Log file found at {mongodb_log_path}")

    @staticmethod
    def log_protocol_logfiles(artifact_manager: MLflowArtifactManager,
                              log_dir_postfix: str = ""):
        if os.getenv("PPRL_LOGS_DIR", None):
            logs_path = Path(os.getenv("PPRL_LOGS_DIR"))
            logger.debug(f"Logging log file artifacts from {logs_path}")
            artifact_manager.log_artifacts(logs_path,
                                           f"logs{log_dir_postfix}", compress=False)

    @staticmethod
    def log_slurm_logfiles(artifact_manager: MLflowArtifactManager,
                           log_dir_postfix: str = ""):
        if os.getenv("SLURM_WORKDIR", None):
            slurm_workdir_path = Path(os.getenv("SLURM_WORKDIR"))
            logger.debug(f"Logging log file artifacts from {slurm_workdir_path}")
            slurm_logs = list(slurm_workdir_path.glob("slurm-*"))
            if not slurm_logs:
                logger.debug("No slurm-* log files found to log as artifacts.")
            else:
                for log_file in slurm_logs:
                    # Rename .out → .out.txt temporarily before logging
                    if log_file.suffix == ".out":
                        renamed_file = Path(
                            tempfile.gettempdir()) / f"{log_file.name}.txt"
                        shutil.copy2(log_file, renamed_file)
                        logger.debug(
                            f"Renamed {log_file.name} → {renamed_file.name} for upload")
                        log_file = renamed_file
                    artifact_manager.log_artifact(
                        log_file, artifact_path=f"logs{log_dir_postfix}",
                        compress=False
                    )


def _preparing_dataset_run_ids(config: InputDatasets):
    if config.dataset_ids:
        # Add datasets from data owner service to mlflow
        dataset_run_ids = []
        artifact_manager = MLflowArtifactManager(compression_enabled=False)
        for dataset_id in config.dataset_ids:
            with mlflow.start_run():
                dataset_run_ids.append(
                    DatasetCreationManager.log_dataset_to_active_run(
                        artifact_manager,
                        dataset_id)
                )
        config.run_ids = dataset_run_ids
    elif config.mlflow_filter_string is not None:
        runs = mlflow.search_runs(
            experiment_names=config.mlflow_search_experiments,
            filter_string=config.mlflow_filter_string,
            output_format="list")
        config.run_ids = [run.info.run_id for run in runs]


def _set_linkage_status(status: str, protocol_id: str | None = None):
    key = "linkage.status" if not protocol_id else f"linkage.{protocol_id}.status"
    mlflow.set_tag(key, status)
