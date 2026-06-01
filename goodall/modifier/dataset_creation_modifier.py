from pathlib import Path
from loguru import logger

from pprl_data_owner_service_api_client import DatasetCorruptionRequestDto
from pprl_protocol_manager_service_api_client import DatasetGeneratorDto, DatasetCsvDto

from goodall.models.experiment_definitions import DatasetCreationPipeline, \
    DatasetCreationConfig, DatasetCreationType
from goodall.modifier.dataset_creation_modifier_implementations import \
    DatasetCreationModifierImplementation, DEFAULT_CONFIG_MODIFIERS
from goodall.modifier.utils import _handle_ranges, _load_json_file
from goodall.tracking.linkage_protocol_manager import _preparing_dataset_run_ids


class DatasetCreationModifier:
    """
    Manager for applying variation modifiers to a base pipeline.
    """

    def __init__(self,
                 config_base_path: Path | None = None,
                 modifiers: dict[
                                str,
                                DatasetCreationModifierImplementation
                            ] | None = None):
        self.config_base_path = config_base_path if config_base_path else Path("")
        if modifiers is None:
            self.modifiers = DEFAULT_CONFIG_MODIFIERS.copy()
        else:
            self.modifiers = modifiers

    def create_configs(self, config: DatasetCreationConfig) -> list[
        DatasetCreationPipeline]:

        config_path = self.config_base_path
        basic_pipeline = config.config
        if basic_pipeline is None:
            relative_config_path = Path(config.config_path)
            config_path = self.config_base_path / relative_config_path
            with open(config_path, "r") as file:
                data = file.read()
                basic_pipeline = DatasetCreationPipeline.model_validate_json(data)
            config_path = config_path.parent

        if basic_pipeline.input:
            _preparing_dataset_run_ids(basic_pipeline.input)
        for stage in basic_pipeline.stages:
            if not stage.config:
                stage_config_path = stage.config_path
                if stage.config_path_is_relative:
                    stage_config_path = config_path / Path(stage_config_path)
                payload = _load_json_file(stage_config_path)
                match stage.type:
                    case DatasetCreationType.CsvImport:
                        stage.config = DatasetCsvDto.model_validate(payload)
                    case DatasetCreationType.Generation:
                        stage.config = DatasetGeneratorDto.model_validate(payload)
                    case DatasetCreationType.Corruption:
                        stage.config = DatasetCorruptionRequestDto.model_validate(
                            payload)
                    case DatasetCreationType.Selection:
                        stage.config = DatasetGeneratorDto.model_validate(payload)

        pipelines = [basic_pipeline]
        for variation in config.variations:
            if variation.as_range:
                variation.replacements = _handle_ranges(variation.replacements)
            modifier = self.modifiers.get(variation.type)
            if modifier is None:
                logger.warning(f"Unknown variation type {variation.type}")
                continue

            new_pipelines: list[DatasetCreationPipeline] = []

            for pipeline in pipelines:
                for replacement in variation.replacements:
                    new_pipeline = DatasetCreationPipeline.model_validate_json(
                        pipeline.model_dump_json())
                    new_pipeline = modifier.modify(new_pipeline, replacement)
                    new_pipelines.append(new_pipeline)
            pipelines = new_pipelines
        return pipelines
