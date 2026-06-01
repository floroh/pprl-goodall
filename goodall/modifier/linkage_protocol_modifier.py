from pathlib import Path
from loguru import logger

from pprl_protocol_manager_service_api_client import MultiLayerProtocol

from goodall.models.experiment_definitions import LinkageProtocolConfig
from goodall.modifier.linkage_protocol_modifier_implementations import \
    LinkageProtocolModifierImplementation, DEFAULT_CONFIG_MODIFIERS
from goodall.modifier.utils import _handle_ranges


class LinkageProtocolModifier:
    """
    Manager for applying variation modifiers to a base protocol.
    """

    def __init__(self,
                 config_base_path: Path | None = None,
                 modifiers: dict[
                                str,
                                LinkageProtocolModifierImplementation
                            ] | None = None):
        self.config_base_path = config_base_path if config_base_path else Path("")
        if modifiers is None:
            self.modifiers = DEFAULT_CONFIG_MODIFIERS.copy()
        else:
            self.modifiers = modifiers

    def create_configs(self, config: LinkageProtocolConfig) -> list[MultiLayerProtocol]:
        basic_protocol = config.config
        if basic_protocol is None:
            relative_config_path = Path(config.config_path)
            config_path = self.config_base_path / relative_config_path
            with open(config_path, "r") as file:
                data = file.read()
                basic_protocol = MultiLayerProtocol.model_validate_json(data)

        protocols = [basic_protocol]
        for variation in config.variations:
            if variation.as_range:
                variation.replacements = _handle_ranges(variation.replacements)
            modifier = self.modifiers.get(variation.type)
            if modifier is None:
                logger.warning(f"Unknown variation type {variation.type}")
                continue

            new_protocols: list[MultiLayerProtocol] = []
            for protocol in protocols:
                for replacement in variation.replacements:
                    new_protocol = MultiLayerProtocol.model_validate_json(
                        protocol.model_dump_json())
                    new_protocol = modifier.modify(new_protocol, replacement)
                    new_protocols.append(new_protocol)
            protocols = new_protocols
        return protocols
