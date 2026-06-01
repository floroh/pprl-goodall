import os
from typing import Any

import mlflow
import pandas as pd
from dotenv import load_dotenv
from loguru import logger
from mlflow import MlflowClient
from mlflow.entities import Run
from mlflow.utils.mlflow_tags import MLFLOW_PARENT_RUN_ID
from pprl_data_owner_service_api_client import AnalysisResultDto
from pprl_linkage_unit_service_api_client import BatchMatchProjectDto
from pprl_protocol_manager_service_api_client import MultiLayerProtocol

from goodall.api_helper.parser import build_weight_string_and_attribute_set, \
    get_attributes_in_encoding, get_weights_from_protocol_step_properties
from goodall.result_analysis.dataset_analysis_result_parser import get_analysis_report
from goodall.result_analysis.project_metrics import ProjectMetricsAnalyzer, \
    get_differing_metrics
from goodall.tracking.dataset_creation_manager import PARAM_DATASET_NAME, \
    ARTIFACT_PATH_ANALYSIS
from goodall.tracking.linkage_protocol_manager import \
    ARTIFACT_PATH_PROTOCOL_CONFIG_FINAL, PARAM_PROTOCOL_FILE
from goodall.tracking.mlflow_artifact_manager import MLflowArtifactManager
from goodall.tracking.mlflow_utils import PARAM_DATASET_RUN_ID

THRESHOLDS_JSON = "thresholds.json"

TAG_LINKAGE_METHOD = "linkage.method"
TAG_LINKAGE_METHOD_BLOCKING = "linkage.method.blocking"
TAG_LINKAGE_METHOD_ENCODING = "linkage.method.encoding"
TAG_LINKAGE_WEIGHT_METHOD = "linkage.weight.method"
TAG_LINKAGE_WEIGHT_VALUES = "linkage.weight.values"
TAG_LINKAGE_ATTRIBUTE_SET = "linkage.attributes"
TAG_DATASET_RUN_ID = "dataset.run_id"
TAG_DATASET_NAME = "dataset.name"

class ExperimentModifierManager:
    def __init__(self, run_ids: list[str]):
        self.run_ids = run_ids
        load_dotenv()
        tracking_uri = os.getenv("MLFLOW_TRACKING_URI")
        mlflow.set_tracking_uri(uri=tracking_uri)
        logger.info(f"Using mlflow tracking uri: {tracking_uri}")
        self.artifact_manager = MLflowArtifactManager()
        self.client = MlflowClient()

    def update(self):
        for idx, run_id in enumerate(self.run_ids, start=1):
            logger.info(f"\n\nUpdating run_id {run_id} ({idx}/{len(self.run_ids)})")
            run = mlflow.get_run(run_id)
            protocol = get_protocol(run)
            if not protocol:
                logger.info(f"Skipping run {run} (not a finished linkage protocol run)")
                continue
            self.add_dataset_info(run)
            self.add_linkage_method(run, protocol)
            self.add_blocking_method(run, protocol)
            self.add_encoding_method(run, protocol)
            self.add_weight_method(run, protocol)
            self.add_attribute_weights_and_schema(run, protocol)
            self.add_metrics(run, protocol)

    def add_linkage_method(self, run: Run,
                           protocol: MultiLayerProtocol | None) -> str:
        if not protocol:
            protocol = get_protocol(run)
            if not protocol:
                return
        new_value = None
        if len(protocol.layers) == 1:
            if protocol.layers[0].name == "ABF":
                if "DBSLeipzig/Plain" in protocol.layers[0].encoding_method:
                    new_value = "PT"
                else:
                    new_value = "ABF"
            if protocol.layers[0].name == "RBF":
                new_value = "RBF"
        else:
            new_value = "ML:"
            for layer in protocol.layers:
                if new_value != "ML:":
                    new_value += "-"
                new_value += layer.name
        self._set_tag_on_change(run, TAG_LINKAGE_METHOD, new_value)
        return new_value

    def add_encoding_method(self, run: Run, protocol: MultiLayerProtocol | None):
        if not protocol:
            protocol = get_protocol(run)
            if not protocol:
                return
        new_value = None
        linkage_method = run.data.tags.get(TAG_LINKAGE_METHOD)
        if not linkage_method:
            linkage_method = self.add_linkage_method(run, protocol)
        if "ML:" not in linkage_method:
            layer = protocol.layers[0]
            encoding_method = layer.encoding_method
            if "name-exchange" in encoding_method:
                new_value = "name-exchange-group"
            elif linkage_method == "RBF":
                new_value = "attribute-salting"
            if "xor" in encoding_method:
                new_value = f"{new_value}:xor"
        self._set_tag_on_change(run, TAG_LINKAGE_METHOD_ENCODING, new_value)

    def add_blocking_method(self, run: Run, protocol: MultiLayerProtocol | None):
        if not protocol:
            protocol = get_protocol(run)
            if not protocol:
                return
        new_value = None
        layer = protocol.layers[0]
        # Use name of matcher to avoid fetching matcher config artifact
        matcher_method = layer.matcher_method
        if "/PGTB/" in matcher_method:
            new_value = "Plain+GT"
        elif "/PB/" in matcher_method:
            new_value = "Plain"
        elif "/LSH/" in matcher_method:
            new_value = "HLSH"
        elif "/LSHL/" in matcher_method:
            new_value = "HLSHL"
        elif "/LSHXL/" in matcher_method:
            new_value = "HLSHXL"
        elif "/LSHXLGT/" in matcher_method:
            new_value = "HLSHXL+GT"
        self._set_tag_on_change(run, TAG_LINKAGE_METHOD_BLOCKING, new_value)

    def add_weight_method(self, run: Run, protocol: MultiLayerProtocol | None):
        if not protocol:
            protocol = get_protocol(run)
            if not protocol:
                return
        new_value = None
        linkage_method = run.data.tags.get(TAG_LINKAGE_METHOD)
        if not linkage_method:
            linkage_method = self.add_linkage_method(run, protocol)
        if linkage_method == "RBF":
            rbf_layer = protocol.layers[0]
            encoding_method = rbf_layer.encoding_method
            def get_weight_string(protocol: MultiLayerProtocol) -> str:
                if rbf_layer.attribute_weight_method:
                    # rbf_encoding = load_artifact_dict(run,
                    #                                    "layer.RBF.encoding.config.json")
                    steps = protocol.step_history
                    for step in steps:
                        if step.type == "PREPARE_CONFIGS":
                            weight_origin: str = step.properties.get("weight-origin",
                                                                     "")
                            if weight_origin == "layer-config":
                                return "RBF:Static-W:layer-config"
                            elif "auto:" in weight_origin:
                                return (f"RBF:Auto-W:"
                                             f"{weight_origin.replace('auto: ', '')}")
                else:
                    return "RBF:Static-k"

            new_value = get_weight_string(protocol)
            # if "static-k" in encoding_method:
            #     new_value = get_weight_string(protocol)
            # if "static-w" in encoding_method:
            #     new_value = "RBF:Static-w"
            if "freq" in encoding_method:
                new_value = get_weight_string(protocol) + ":freq"
            if (rbf_layer.attribute_weight_method is not None
                    and "sourceSpecific" in rbf_layer.attribute_weight_method):
                new_value = new_value + ":src"
        elif linkage_method == "ABF" or linkage_method == "PT":
            layer = protocol.layers[0]
            if layer.attribute_weight_method:
                # matching = load_artifact_dict(run,
                #                                   f"layer.{linkage_method}.matching.config.json")
                steps = protocol.step_history
                for step in steps:
                    if step.type == "PREPARE_MATCHER_CONFIGS":
                        weight_origin: str = step.properties.get("weight-origin", "")
                        if weight_origin == "layer-config":
                            new_value = f"{linkage_method}:Static-W:layer-config"
                        elif "auto:" in weight_origin:
                            new_value = (f"{linkage_method}:Auto-W:"
                                         f"{weight_origin.replace('auto: ', '')}")
            else:
                new_value = f"{linkage_method}:Static-k"
        self._set_tag_on_change(run, TAG_LINKAGE_WEIGHT_METHOD, new_value)

    def add_attribute_weights_and_schema(self, run: Run, protocol: MultiLayerProtocol):
        new_weight_value = None
        new_attribute_set_value = None
        linkage_method = run.data.tags.get(TAG_LINKAGE_METHOD)
        if not linkage_method:
            linkage_method = self.add_linkage_method(run, protocol)
        if linkage_method == "RBF":
            rbf_layer = protocol.layers[0]
            if rbf_layer.attribute_weight_method:
                if rbf_layer.initial_attribute_weights:
                    new_weight_value, new_attribute_set_value = build_weight_string_and_attribute_set(
                        rbf_layer.initial_attribute_weights)
                else:
                    rbf_encoding = load_artifact_dict(run,
                                                      "layer.RBF.encoding.config.json")
                    try:
                        attributes = get_attributes_in_encoding(rbf_encoding)
                        weight_dict = get_weights_from_protocol_step_properties(protocol)
                        weight_dict = {k: v for k, v in weight_dict.items() if
                                   [k for attr in attributes if attr in k]}
                        new_weight_value, new_attribute_set_value = build_weight_string_and_attribute_set(
                            weight_dict)
                    except Exception:
                        logger.error(f"Failed to parse weights from {rbf_encoding}")
            else:
                rbf_encoding = load_artifact_dict(run,
                                                  "layer.RBF.encoding.config.json")
                attributes = get_attributes_in_encoding(rbf_encoding)
                weight_dict = {a: 1.0 for a in attributes}
                _, new_attribute_set_value = build_weight_string_and_attribute_set(
                    weight_dict)
        elif linkage_method == "ABF" or linkage_method == "PT":
            layer = protocol.layers[0]
            if layer.attribute_weight_method:
                if "Weighted" in layer.matcher_method:
                    matching = load_artifact_dict(run,
                                                  "layer.ABF.matching.config.json")
                    try:
                        weight_dict = matching["linker"]["recordSimilarityCalculator"][
                            "similarityAggregator"]["weights"]
                        new_weight_value, new_attribute_set_value = build_weight_string_and_attribute_set(
                            weight_dict)
                    except Exception:
                        logger.error(f"Failed to parse weights from {matching}")
        self._set_tag_on_change(run, TAG_LINKAGE_WEIGHT_VALUES, new_weight_value)
        self._set_tag_on_change(run, TAG_LINKAGE_ATTRIBUTE_SET, new_attribute_set_value)

    def add_dataset_info(self, run: Run):
        old_dataset_run_id = run.data.tags.get(TAG_DATASET_RUN_ID)
        new_dataset_run_id = None
        new_dataset_name = None
        parent_run_id = run.data.tags.get(MLFLOW_PARENT_RUN_ID)
        if parent_run_id:
            parent_run = mlflow.get_run(parent_run_id)
            new_dataset_run_id = parent_run.data.params.get(PARAM_DATASET_RUN_ID)
            if new_dataset_run_id:
                dataset_run = mlflow.get_run(new_dataset_run_id)
                new_dataset_name = dataset_run.data.params.get(PARAM_DATASET_NAME)
        self._set_tag_on_change(run, TAG_DATASET_RUN_ID, new_dataset_run_id)
        self._set_tag_on_change(run, TAG_DATASET_NAME, new_dataset_name)

    def _set_tag_on_change(self, run: Run, key: str, new_value: str | None):
        old_value = run.data.tags.get(key)
        if old_value != new_value:
            logger.info(
                f"Run {run.info.run_id}: Set tag {key}={new_value}")
            self.client.set_tag(run.info.run_id, key, new_value)
            run.data.tags[key] = new_value

    def add_metrics(self, run: Run, protocol: MultiLayerProtocol):
        run_id = run.info.run_id
        linkage_method = run.data.tags.get(TAG_LINKAGE_METHOD)
        if not linkage_method:
            linkage_method = self.add_linkage_method(run, protocol)

        if linkage_method == "RBF" or linkage_method == "ABF" or linkage_method == "PT":
            layer_name = "RBF" if linkage_method == "RBF" else "ABF"
            project_json = load_artifact_dict(run,
                                              f"layer.{layer_name}.project.json")
            project = BatchMatchProjectDto.model_validate(project_json)
            try:
                lu_logfile = load_artifact_text(run, "logs/lu.log")
            except:
                logger.warning("No lu.log found. Some metrics may not be extracted.")
                lu_logfile = None
            analyzer = ProjectMetricsAnalyzer(project=project, lu_logfile=lu_logfile)
            dataset_sizes = self.get_dataset_sizes_if_needed(run)
            metrics = analyzer.get_metrics_from_reports(dataset_sizes)
            matching_files = mlflow.artifacts.list_artifacts(run_id=run_id)
            if THRESHOLDS_JSON not in [file_info.path for file_info in matching_files]:
                mlflow.log_table(analyzer.get_df_thresholds(), THRESHOLDS_JSON, run_id)

            # Get encoded dataset metrics
            if linkage_method == "RBF":
                metrics.update(self.get_encoded_dataset_metrics(run, linkage_method))

            # Compare selected metrics with the ones already in mflow
            # check_metrics_identity(metrics, run.data.metrics)

            # Get metric updates
            metric_updates = get_differing_metrics(metrics, run.data.metrics)
            if metric_updates:
                logger.info(f"Metric updates: {metric_updates}")
            # self.client.log_batch(run_id=run_id, metrics=metric_updates)
            mlflow.log_metrics(run_id=run_id, metrics=metric_updates)

    def get_encoded_dataset_metrics(self, run: Run, linkage_method: str) -> dict[str, float]:
        dataset_description_json = load_artifact_dict(run,
                                                      f"{ARTIFACT_PATH_ANALYSIS}/"
                                                      f"/layer.{linkage_method}.dataset_description.json")
        dataset_description = AnalysisResultDto.model_validate(dataset_description_json)
        _, df_attribute_length = get_analysis_report(dataset_description,
                                                     "AttributeLength")
        df_attribute_length: pd.DataFrame
        df_attribute_length_rbf = df_attribute_length[
            df_attribute_length["attribute"] == "RBF"]
        if not df_attribute_length_rbf.empty:
            first_row = df_attribute_length_rbf.iloc[0]
            mean_rbf_fillrate = first_row["mean"] / 1024
            median_rbf_fillrate = first_row["median"] / 1024
            return {
                "dataset.rbf.fillrate.mean": float(mean_rbf_fillrate),
                "dataset.rbf.fillrate.median": float(median_rbf_fillrate),
            }
        return {}

    def get_dataset_sizes_if_needed(self, run: Run) -> Any:
        dataset_sizes = None
        # if not METRIC_BLOCKING_RR in run.data.metrics:
        dataset_run_id = run.data.tags.get(TAG_DATASET_RUN_ID, None)
        if not dataset_run_id:
            parent_run = mlflow.get_parent_run(run.info.run_id)
            dataset_run_id = parent_run.data.params.get(PARAM_DATASET_RUN_ID, None)
        if dataset_run_id:
            dataset_run = mlflow.get_run(dataset_run_id)
            dataset_sizes = [v for k, v in dataset_run.data.metrics.items()
                             if k.startswith("size.") and k != "size.total"]
        return dataset_sizes


def get_protocol(run: Run) -> MultiLayerProtocol | None:
    if not is_finished_linkage_protocol_run(run):
        logger.info(f"Run {run.info.run_id} is not a finished linkage protocol run")
        return None
    protocol_dict = load_artifact_dict(run, ARTIFACT_PATH_PROTOCOL_CONFIG_FINAL)
    return MultiLayerProtocol.model_validate(protocol_dict)


def load_artifact_dict(run: Run, artifact_path: str) -> dict:
    artifact_uri = run.info.artifact_uri
    protocol_dict = mlflow.artifacts.load_dict(artifact_uri + "/" + artifact_path)
    return protocol_dict

def load_artifact_text(run: Run, artifact_path: str) -> str:
    artifact_uri = run.info.artifact_uri
    protocol_dict = mlflow.artifacts.load_text(artifact_uri + "/" + artifact_path)
    return protocol_dict

def load_artifact_as_dataframe(run: Run, artifact_path: str) -> pd.DataFrame:
    artifact_uri = run.info.artifact_uri
    dataframe_dict = mlflow.artifacts.load_dict(artifact_uri + "/" + artifact_path)
    return pd.DataFrame(data=dataframe_dict["data"], columns=dataframe_dict["columns"])


def is_finished_linkage_protocol_run(run: Run):
    return is_finished_run(run) and is_linkage_protocol_run(run)


def is_linkage_protocol_run(run: Run):
    return PARAM_PROTOCOL_FILE in run.data.params


def is_finished_run(run: Run):
    return (run.info.status == "FINISHED"
            and run.data.tags.get("linkage.status", "") == "finished")
