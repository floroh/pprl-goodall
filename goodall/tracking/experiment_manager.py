import json
import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger

import mlflow

from goodall.api_helper.service_status import get_service_health_checks
from goodall.models.experiment_definitions import ExperimentDefinition, \
    MlFlowRunSelection
from goodall.models.services import ServiceStatus
from goodall.modifier.dataset_creation_modifier import DatasetCreationModifier
from goodall.modifier.linkage_protocol_modifier import LinkageProtocolModifier
from goodall.tracking.dataset_creation_manager import DatasetCreationManager
from goodall.tracking.experiment_modifier import ExperimentModifierManager
from goodall.tracking.linkage_protocol_manager import LinkageProtocolManager

MLFLOW_FILTER_STRING_SCHEDULED = 'tags.`linkage.status` = "scheduled"'


class Experimentmanager:
    def __init__(self, config_base_path: Path):
        self.config_base_path = config_base_path
        self.experiments: list[ExperimentDefinition] = []
        load_dotenv()
        tracking_uri = os.getenv("MLFLOW_TRACKING_URI")
        mlflow.set_tracking_uri(uri=tracking_uri)
        logger.info(f"Using mlflow tracking uri: {tracking_uri}")

    def status(self) -> list[ServiceStatus]:
        results = get_service_health_checks(check_mlflow=True)
        for service in results:
            status_str = "healthy" if service.healthy else "failed"
            if service.healthy:
                logger.info(f"{service.name} ({service.endpoint}): {status_str}")
            else:
                logger.error(f"{service}: {status_str}")
        return results

    def prepare(self, path: Path):
        config_path = self.config_base_path / path
        with open(config_path, "r") as file:
            parsed_list = json.loads(file.read())
            exp_definitions = [
                ExperimentDefinition.model_validate_json(json.dumps(obj))
                for obj in parsed_list
            ]
            for exp_definition in exp_definitions:
                if exp_definition.add_timestamp:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    exp_definition.name = f"{exp_definition.name}_{timestamp}"
                if exp_definition.dataset_creation_config:
                    creation_pipelines = DatasetCreationModifier(
                        config_path.parent).create_configs(
                        exp_definition.dataset_creation_config)
                    for creation_pipeline in creation_pipelines:
                        new_exp_definition = ExperimentDefinition.model_validate_json(
                            exp_definition.model_dump_json())
                        new_exp_definition.dataset_creation_config.config = creation_pipeline
                        self.experiments.append(new_exp_definition)
                if exp_definition.protocol_config:
                    protocols = LinkageProtocolModifier(
                        config_path.parent).create_configs(
                        exp_definition.protocol_config
                    )
                    for protocol in protocols:
                        new_exp_definition = ExperimentDefinition.model_validate_json(
                            exp_definition.model_dump_json())
                        new_exp_definition.protocol_config.config = protocol
                        self.experiments.append(new_exp_definition)

    def run(self):
        manager = DatasetCreationManager()
        for idx, experiment in enumerate(self.experiments):
            logger.info(
                f"Running experiment ({idx + 1}/{len(self.experiments)}): {experiment}")
            mlflow.set_experiment(experiment.name)
            if experiment.dataset_creation_config:
                manager.run(experiment.dataset_creation_config)
            if experiment.protocol_config:
                raise NotImplementedError("Protocol experiments must be scheduled.")

    def schedule(self):
        manager = LinkageProtocolManager()
        for idx, experiment in enumerate(self.experiments):
            logger.info(
                f"Scheduling experiment ({idx + 1}/{len(self.experiments)}): {experiment}")
            mlflow.set_experiment(experiment.name)
            if experiment.dataset_creation_config:
                raise NotImplementedError(
                    "Dataset creation must be executed with run().")
            if experiment.protocol_config:
                manager.schedule(experiment.protocol_config)

    def search(self,
               selection: MlFlowRunSelection,
               log_details: bool = True) -> list[str]:
        if selection.run_ids:
            return selection.run_ids

        if not selection.filter_string:
            selection.filter_string = MLFLOW_FILTER_STRING_SCHEDULED
        logger.info(f"Searching runs with filter_string: {selection.filter_string}")
        if selection.search_experiments:
            runs = mlflow.search_runs(experiment_names=selection.search_experiments,
                                      filter_string=selection.filter_string,
                                      output_format="list")
        else:
            runs = mlflow.search_runs(search_all_experiments=True,
                                      filter_string=selection.filter_string,
                                      output_format="list")
        runs.sort(key=lambda run: run.info.start_time)
        run_ids = [run.info.run_id for run in runs]
        logger.info(f"Found {len(run_ids)} run ids: {run_ids}")
        if log_details:
            for run in runs:
                logger.info(
                    f"{run.info.run_id}: "
                    f"exp_id={run.info.experiment_id}, "
                    f"dataset_run_id={run.data.params.get('dataset_run_id')}")
        return run_ids

    def execute(self, selection: MlFlowRunSelection):
        logger.info("Executing scheduled runs")
        manager = LinkageProtocolManager()
        run_ids = self.search(selection)
        manager.execute(run_ids)

    def update(self, run_ids: list[str]):
        manager = ExperimentModifierManager(run_ids)
        manager.update()
