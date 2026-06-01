from abc import ABC, abstractmethod
from typing import Any
from loguru import logger

from pprl_data_owner_service_api_client import DatasetCorruptionRequestDto
from pprl_protocol_manager_service_api_client import DatasetCsvDto, DatasetGeneratorDto

from goodall.models.experiment_definitions import DatasetCreationPipeline, \
    DatasetCreationType


class DatasetCreationModifierImplementation(ABC):
    """Base class for modifiers."""

    @abstractmethod
    def modify(self, pipeline: DatasetCreationPipeline,
               new_value: Any) -> DatasetCreationPipeline:
        """
        Return a modified copy of `pipeline` with `new_value` applied.
        """
        raise NotImplementedError


class SelectorSeedModifier(DatasetCreationModifierImplementation):
    def modify(self, pipeline: DatasetCreationPipeline,
               new_value: Any) -> DatasetCreationPipeline:
        counter = 0
        for stage in pipeline.stages:
            if stage.type == DatasetCreationType.Selection:
                try:
                    config: DatasetGeneratorDto = stage.config
                    config.usvr_selection_config.ordering_seed = new_value
                    counter = counter + 1
                except Exception:
                    continue

        if counter == 0:
            logger.error("Modifier is not applicable.")
            raise RuntimeError("Modifier is not applicable.")
        return pipeline

class SelectorTime1YearModifier(DatasetCreationModifierImplementation):
    def modify(self, pipeline: DatasetCreationPipeline,
               new_value: Any) -> DatasetCreationPipeline:
        counter = 0
        for stage in pipeline.stages:
            if stage.type == DatasetCreationType.Selection:
                try:
                    config: DatasetGeneratorDto = stage.config
                    config.usvr_selection_config.time_filter.min_days = 365 * new_value
                    config.usvr_selection_config.time_filter.max_days = 365 * (new_value + 1) - 1
                    counter = counter + 1
                except Exception:
                    continue

        if counter == 0:
            logger.error("Modifier is not applicable.")
            raise RuntimeError("Modifier is not applicable.")
        return pipeline

class SelectorTimeYearSpanModifier(DatasetCreationModifierImplementation):
    def modify(self, pipeline: DatasetCreationPipeline,
               new_value: Any) -> DatasetCreationPipeline:
        counter = 0
        for stage in pipeline.stages:
            if stage.type == DatasetCreationType.Selection:
                try:
                    config: DatasetGeneratorDto = stage.config
                    min_year, max_year = str(new_value).split("-")
                    config.usvr_selection_config.time_filter.min_days = 365 * int(min_year)
                    config.usvr_selection_config.time_filter.max_days = 365 * int(max_year) - 1
                    counter = counter + 1
                except Exception:
                    continue

        if counter == 0:
            logger.error("Modifier is not applicable.")
            raise RuntimeError("Modifier is not applicable.")
        return pipeline

class SelectorSizeModifier(DatasetCreationModifierImplementation):
    def modify(self, pipeline: DatasetCreationPipeline,
               new_value: Any) -> DatasetCreationPipeline:
        counter = 0
        for stage in pipeline.stages:
            if stage.type == DatasetCreationType.Selection:
                try:
                    config: DatasetGeneratorDto = stage.config
                    config.usvr_selection_config.num_records_a = new_value
                    config.usvr_selection_config.num_records_b = new_value
                    counter = counter + 1
                except Exception:
                    continue

        if counter == 0:
            logger.error("Modifier is not applicable.")
            raise RuntimeError("Modifier is not applicable.")
        return pipeline

class SelectorOverlapModifier(DatasetCreationModifierImplementation):
    def modify(self, pipeline: DatasetCreationPipeline,
               new_value: Any) -> DatasetCreationPipeline:
        counter = 0
        for stage in pipeline.stages:
            if stage.type == DatasetCreationType.Selection:
                try:
                    config: DatasetGeneratorDto = stage.config
                    abs_duplicates = config.usvr_selection_config.num_records_a * new_value
                    config.usvr_selection_config.num_duplicates = int(abs_duplicates)
                    counter = counter + 1
                except Exception:
                    continue

        if counter == 0:
            logger.error("Modifier is not applicable.")
            raise RuntimeError("Modifier is not applicable.")
        return pipeline

class SelectorMinChangesModifier(DatasetCreationModifierImplementation):
    def modify(self, pipeline: DatasetCreationPipeline,
               new_value: Any) -> DatasetCreationPipeline:
        counter = 0
        for stage in pipeline.stages:
            if stage.type == DatasetCreationType.Selection:
                try:
                    config: DatasetGeneratorDto = stage.config
                    config.usvr_selection_config.change_filter.min_changes = new_value
                    counter = counter + 1
                except Exception:
                    continue

        if counter == 0:
            logger.error("Modifier is not applicable.")
            raise RuntimeError("Modifier is not applicable.")
        return pipeline


class CorruptorCreatorNameModifier(DatasetCreationModifierImplementation):
    def modify(self, pipeline: DatasetCreationPipeline,
               new_value: Any) -> DatasetCreationPipeline:
        counter = 0
        for stage in pipeline.stages:
            if stage.type == DatasetCreationType.Corruption:
                try:
                    config: DatasetCorruptionRequestDto = stage.config
                    config.config_creator.name = new_value
                    counter = counter + 1
                except Exception:
                    continue

        if counter == 0:
            logger.error("Modifier is not applicable.")
            raise RuntimeError("Modifier is not applicable.")
        return pipeline


class CorruptorCreatorOverlapModifier(DatasetCreationModifierImplementation):
    def modify(self, pipeline: DatasetCreationPipeline,
               new_value: Any) -> DatasetCreationPipeline:
        counter = 0
        for stage in pipeline.stages:
            if stage.type == DatasetCreationType.Corruption:
                try:
                    config: DatasetCorruptionRequestDto = stage.config
                    config.config_creator.override.source_overlap = new_value
                    counter = counter + 1
                except Exception:
                    continue

        if counter == 0:
            logger.error("Modifier is not applicable.")
            raise RuntimeError("Modifier is not applicable.")
        return pipeline


class CorruptorCreatorSeedModifier(DatasetCreationModifierImplementation):
    def modify(self, pipeline: DatasetCreationPipeline,
               new_value: Any) -> DatasetCreationPipeline:
        counter = 0
        for stage in pipeline.stages:
            if stage.type == DatasetCreationType.Corruption:
                try:
                    config: DatasetCorruptionRequestDto = stage.config
                    config.config_creator.override.seed = new_value
                    counter = counter + 1
                except Exception:
                    continue

        if counter == 0:
            logger.error("Modifier is not applicable.")
            raise RuntimeError("Modifier is not applicable.")
        return pipeline

class CorruptorCreatorSizeModifier(DatasetCreationModifierImplementation):
    def modify(self, pipeline: DatasetCreationPipeline,
               new_value: Any) -> DatasetCreationPipeline:
        counter = 0
        for stage in pipeline.stages:
            if stage.type == DatasetCreationType.Corruption:
                try:
                    config: DatasetCorruptionRequestDto = stage.config
                    config.config_creator.override.original_size = new_value
                    config.config_creator.override.modified_size = new_value
                    counter = counter + 1
                except Exception:
                    continue

        if counter == 0:
            logger.error("Modifier is not applicable.")
            raise RuntimeError("Modifier is not applicable.")
        return pipeline


class CsvImportPath(DatasetCreationModifierImplementation):
    def modify(self, pipeline: DatasetCreationPipeline,
               new_value: Any) -> DatasetCreationPipeline:
        counter = 0
        for stage in pipeline.stages:
            if stage.type == DatasetCreationType.CsvImport:
                try:
                    config: DatasetCsvDto = stage.config
                    config.path = new_value
                    counter = counter + 1
                except AttributeError:
                    continue
        if counter == 0:
            logger.error("Modifier is not applicable.")
            raise RuntimeError("Modifier is not applicable.")
        return pipeline


DEFAULT_CONFIG_MODIFIERS: dict[str, DatasetCreationModifierImplementation] = {
    "selection:usvr_selection_config.ordering_seed": SelectorSeedModifier(),
    "selection:size": SelectorSizeModifier(),
    "selection:overlap": SelectorOverlapModifier(),
    "selection:change.min": SelectorMinChangesModifier(),
    "selection:time.year": SelectorTime1YearModifier(),
    "selection:time.year_span": SelectorTimeYearSpanModifier(),
    "corruption:config_creator.override.seed": CorruptorCreatorSeedModifier(),
    "corruption:config_creator.override.size": CorruptorCreatorSizeModifier(),
    "corruption:config_creator.override.source_overlap": CorruptorCreatorOverlapModifier(),
    "corruption:config_creator.name": CorruptorCreatorNameModifier(),
    "csvImport:path": CsvImportPath(),
}
