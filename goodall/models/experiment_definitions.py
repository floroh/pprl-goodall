from enum import StrEnum
from pathlib import Path
from typing import Any

from pprl_data_owner_service_api_client import DatasetCorruptionRequestDto
from pprl_protocol_manager_service_api_client import DatasetGeneratorDto, DatasetCsvDto, \
    MultiLayerProtocol
from pydantic import BaseModel, model_validator


# General config
class ConfigVariation(BaseModel):
    type: str
    description: str | None = None
    replacements: list
    as_range: bool = False

class InputDatasets(BaseModel):
    dataset_ids: list[int] | None = None
    mlflow_search_experiments: list[str] = ["datasets"]
    mlflow_filter_string: str | None = None
    run_ids: list[str] | None = None
    import_plain_datasets_from_mlflow: bool = True

    @model_validator(mode="after")
    def _require_any_source(self):
        if ((not self.dataset_ids) and (self.mlflow_filter_string is None) and (
        not self.run_ids)):
            raise ValueError(
                "`dataset_ids`, `mlflow_filter_string` or `run_ids` must be provided.")
        return self


# Dataset Creation
class DatasetCreationType(StrEnum):
    CsvImport = "csvImport"
    Generation = "generation"
    Corruption = "corruption"
    Selection = "selection"


class DatasetCreationStage(BaseModel):
    type: DatasetCreationType
    config: DatasetCsvDto | DatasetGeneratorDto | DatasetCorruptionRequestDto | None = None
    config_path: str | Path | None = None
    config_path_is_relative: bool = True
    input_dataset_id: int | None = None
    output_dataset_id: int | None = None

    @model_validator(mode="after")
    def _require_config_or_config_path(self):
        if (self.config is None) and (self.config_path is None):
            raise ValueError("Either `config` or `config_path` must be provided.")
        return self


class DatasetCreationPipeline(BaseModel):
    input: InputDatasets | None = None
    stages: list[DatasetCreationStage]
    clean_up_datasets: bool = False


class DatasetCreationConfig(BaseModel):
    config: DatasetCreationPipeline | None = None
    config_path: str | Path | None = None
    tags: dict[str, Any] | None = None
    variations: list[ConfigVariation] | None = []

    @model_validator(mode="after")
    def _require_config_or_config_path(self):
        if (self.config is None) and (self.config_path is None):
            raise ValueError("Either `config` or `config_path` must be provided.")
        return self


# Linkage
class LinkageLogging(BaseModel):
    exclude_tags: bool = True

class LinkageProtocolConfig(BaseModel):
    input: InputDatasets
    config: MultiLayerProtocol | None = None
    config_path: str | None = None
    config_path_is_relative: bool = True
    tags: dict[str, Any] | None = None
    variations: list[ConfigVariation] = []
    logging_config: LinkageLogging | None = None

    @model_validator(mode="after")
    def _require_config_or_config_path(self):
        if (self.config is None) and (self.config_path is None):
            raise ValueError("Either `config` or `config_path` must be provided.")
        return self


class DatasetImportInstructions(BaseModel):
    """
    Defines, how to import a dataset to the data owner service
    """
    type: str
    dataset_id: int
    location: str


# Experiment
class ExperimentDefinition(BaseModel):
    name: str
    dataset_creation_config: DatasetCreationConfig | None = None
    protocol_config: LinkageProtocolConfig | None = None
    add_timestamp: bool = False

    @model_validator(mode="after")
    def _require_at_least_one_config(self):
        if (self.dataset_creation_config is None) and (self.protocol_config is None):
            raise ValueError(
                "Either `dataset_creation_config` or `protocol_config` must be provided.")
        return self


# Analysis
class MlFlowRunSelection(BaseModel):
    search_experiments: list[str]| None = None
    filter_string: str | None = None
    run_ids: list[str] | None = None

class MlFlowResultLoaderConfig(BaseModel):
    run_selection: MlFlowRunSelection
    download_dump: bool = True
    import_to_services: bool = False