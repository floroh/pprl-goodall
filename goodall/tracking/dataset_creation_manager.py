import tempfile
import time
from pathlib import Path
from typing import Any

import mlflow
from loguru import logger
from pprl_data_owner_service_api_client import DatasetCorruptionRequestDto
from pprl_protocol_manager_service_api_client import DatasetCsvDto, DatasetGeneratorDto

from goodall.api_helper import do_api, common_api, pm_api
from goodall.api_helper.pprl_clients import Service

from goodall.models.experiment_definitions import DatasetCreationConfig, \
    DatasetCreationPipeline, DatasetCreationType
from goodall.result_analysis.dataset_analysis_result_parser import get_dataset_metrics
from goodall.tracking.mlflow_artifact_manager import MLflowArtifactManager

PARAM_DATASET_NAME = "dataset_name"

ARTIFACT_PATH_DATASET = "dataset"
ARTIFACT_PATH_ANALYSIS = "analysis"
ARTIFACT_PATH_DATASET_DESCRIPTION = f"{ARTIFACT_PATH_ANALYSIS}/dataset_description.json"


class DatasetCreationManager:

    def __init__(self):
        self.compression: str | None = "zip"

    def run(self, config: DatasetCreationConfig) -> list[str]:
        pipeline: DatasetCreationPipeline = config.config
        if not pipeline:
            raise RuntimeError("Pipeline definition is missing")
        run_ids = []
        dataset_ids = []
        with mlflow.start_run():
            logger.info("Starting run")

            start_time = time.perf_counter()
            dataset_id = None
            for idx, stage in enumerate(pipeline.stages):
                start_time_stage = time.perf_counter()
                match stage.type:
                    case DatasetCreationType.CsvImport:
                        if not isinstance(stage.config, DatasetCsvDto):
                            raise "Configuration failure due to type mismatch."
                        logger.info(f"Adding csv dataset {stage.config}")
                        dataset_id = pm_api.add_data_owner_dataset(stage.config)
                        mlflow.log_param("csvPath", stage.config.path)
                    case DatasetCreationType.Generation:
                        if not isinstance(stage.config, DatasetGeneratorDto):
                            raise "Configuration failure due to type mismatch."
                        logger.info(f"Generating dataset {stage.config}")
                        dataset_id = pm_api.do_preparation_controller.add_generated_dataset(
                            stage.config)
                    case DatasetCreationType.Corruption:
                        if not isinstance(stage.config, DatasetCorruptionRequestDto):
                            raise "Configuration failure due to type mismatch."
                        if dataset_id:
                            stage.config.input_dataset_id = dataset_id
                        logger.info(f"Corrupting dataset {stage.config}")
                        config_creator = stage.config.config_creator
                        if config_creator:
                            config_creator.reference_dataset_id = dataset_id \
                                if dataset_id else stage.config.input_dataset_id
                            generation_config = do_api.corrupter_controller.get_dataset_generation_config(
                                config_creator)
                            mlflow.log_dict(generation_config.to_dict(),
                                            "corruption_config.json")
                        dataset_id = do_api.corrupter_controller.corrupt_dataset(
                            stage.config)
                    case DatasetCreationType.Selection:
                        if not isinstance(stage.config, DatasetGeneratorDto):
                            raise "Configuration failure due to type mismatch."
                        dataset_id = pm_api.do_preparation_controller.add_generated_dataset(
                            stage.config)
                mlflow.log_param(f"datasetId.{idx}", dataset_id)
                mlflow.log_metric(f"runtime.{idx}",
                                  time.perf_counter() - start_time_stage)
                dataset_ids.append(dataset_id)
            mlflow.log_metric("runtime", time.perf_counter() - start_time)
            mlflow.log_dict(config.model_dump(), "dataset_creation_config.json")
            artifact_manager = MLflowArtifactManager(compression_enabled=False)
            self.log_dataset_to_active_run(artifact_manager, dataset_id, config.tags)
            run_ids.append(mlflow.active_run().info.run_id)
        if pipeline.clean_up_datasets:
            for dataset_id in dataset_ids:
                do_api.dataset_controller.delete_dataset(dataset_id)
        return run_ids

    @staticmethod
    def log_dataset_to_active_run(artifact_manager: MLflowArtifactManager,
                                  dataset_id: int, tags: dict[str, Any] | None = None,
                                  ):
        dataset_dto = common_api.get_dataset(Service.Data_owner_1, dataset_id)
        mlflow.log_param(PARAM_DATASET_NAME, dataset_dto.dataset_name)

        logger.info("Fetching dataset analysis result")
        dataset_analysis = common_api.get_dataset_analysis_result(
            Service.Data_owner_1, dataset_id, parameters={"includeAdditionalResults": "true"})
        mlflow.log_dict(dataset_analysis.model_dump(),
                        ARTIFACT_PATH_DATASET_DESCRIPTION)

        logger.info("Parsing dataset metrics")
        metrics = get_dataset_metrics(dataset_analysis)
        logger.info("Logging dataset metrics")
        mlflow.log_metrics(metrics)

        logger.info("Logging file artifacts")
        with tempfile.TemporaryDirectory(prefix="datacreation_") as tmpdir:
            tmp_path = Path(tmpdir)

            logger.info("Getting record dataframe")
            df_records = common_api.get_records_as_dataframe(Service.Data_owner_1,
                                                             dataset_id)
            dataset_path = tmp_path / Path(ARTIFACT_PATH_DATASET)
            logger.info("Logging record csv dataset")
            common_api.write_dataset(df_records, dataset_path)
            artifact_manager.log_artifacts(str(dataset_path), ARTIFACT_PATH_DATASET,
                                           compress=True)

            logger.info("Getting tag dataframe")
            df_tags = common_api.get_tags_as_dataframe(Service.Data_owner_1,
                                                       dataset_id)
            tag_file_path = tmp_path / Path("tags.csv")
            logger.info("Logging tag csv")
            df_tags.to_csv(tag_file_path, index=False, encoding="utf-8")
            artifact_manager.log_artifact(str(tag_file_path), ARTIFACT_PATH_ANALYSIS,
                                          compress=True)

        tags_to_log = {"creation.status": "logged"}
        if tags:
            tags_to_log.update(tags)
        mlflow.set_tags(tags_to_log)
