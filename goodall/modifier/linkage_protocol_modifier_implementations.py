from abc import ABC, abstractmethod
from typing import Any

from pprl_protocol_manager_service_api_client import MultiLayerProtocol


class LinkageProtocolModifierImplementation(ABC):
    """Base class for modifiers."""

    @abstractmethod
    def modify(self, protocol: MultiLayerProtocol,
               new_value: Any) -> MultiLayerProtocol:
        raise NotImplementedError


class InitialRbfThreshold(LinkageProtocolModifierImplementation):
    def modify(self, protocol: MultiLayerProtocol,
               new_value: Any) -> MultiLayerProtocol:
        counter = 0
        for layer in protocol.layers:
            if layer.name == "RBF":
                try:
                    layer.initial_threshold = new_value
                    counter = counter + 1
                except AttributeError:
                    continue
        if counter == 0:
            raise RuntimeError("Modifier is not applicable.")
        return protocol

class AttributeWeightMethod(LinkageProtocolModifierImplementation):

    def __init__(self, layer_name: str):
        self.layer_names = [layer_name]
        if layer_name == "A":
            self.layer_names = ["ABF", "PT"]

    def modify(self, protocol: MultiLayerProtocol,
               new_value: Any) -> MultiLayerProtocol:
        counter = 0
        for layer in protocol.layers:
            if layer.name in self.layer_names:
                try:
                    layer.attribute_weight_method = new_value
                    counter = counter + 1
                except AttributeError:
                    continue
        if counter == 0:
            raise RuntimeError("Modifier is not applicable.")
        return protocol

class AttributeWeights(LinkageProtocolModifierImplementation):

    def __init__(self, layer_name: str):
        self.layer_names = [layer_name]
        if layer_name == "A":
            self.layer_names = ["ABF", "PT"]

    def modify(self, protocol: MultiLayerProtocol,
               new_value: Any) -> MultiLayerProtocol:
        counter = 0
        for layer in protocol.layers:
            if layer.name in self.layer_names:
                try:
                    layer.initial_attribute_weights = new_value
                    counter = counter + 1
                except AttributeError as e:
                    continue
        if counter == 0:
            raise RuntimeError("Modifier is not applicable.")
        return protocol

class ClericalReviewBudget(LinkageProtocolModifierImplementation):
    def modify(self, protocol: MultiLayerProtocol,
               new_value: Any) -> MultiLayerProtocol:
        counter = 0
        for layer in protocol.layers:
            if layer.name == "PPCR":
                try:
                    layer.budget = int(new_value)
                    layer.batch_size = int(new_value / (5 * 2))
                    counter = counter + 1
                except AttributeError as e:
                    continue
        if counter == 0:
            raise RuntimeError("Modifier is not applicable.")
        return protocol

class ClericalReviewErrorRate(LinkageProtocolModifierImplementation):
    def modify(self, protocol: MultiLayerProtocol,
               new_value: Any) -> MultiLayerProtocol:
        counter = 0
        for layer in protocol.layers:
            if layer.name == "PPCR":
                try:
                    layer.error_rate = float(new_value)
                    counter = counter + 1
                except AttributeError as e:
                    continue
        if counter == 0:
            raise RuntimeError("Modifier is not applicable.")
        return protocol

class Repetition(LinkageProtocolModifierImplementation):
    def modify(self, protocol: MultiLayerProtocol,
               new_value: Any) -> MultiLayerProtocol:
        return protocol


class MatcherMethod(LinkageProtocolModifierImplementation):
    def __init__(self, layer_name: str):
        self.layer_names = [layer_name]

    def modify(self, protocol: MultiLayerProtocol,
               new_value: Any) -> MultiLayerProtocol:
        counter = 0
        for layer in protocol.layers:
            if layer.name in self.layer_names:
                try:
                    layer.matcher_method = new_value
                    counter = counter + 1
                except AttributeError:
                    continue
        if counter == 0:
            raise RuntimeError("Modifier is not applicable.")
        return protocol

DEFAULT_CONFIG_MODIFIERS: dict[str, LinkageProtocolModifierImplementation] = {
    "protocol:layer[PPCR].error_rate": ClericalReviewErrorRate(),
    "protocol:layer[PPCR].budget": ClericalReviewBudget(),
    "protocol:layer[RBF].initial_threshold": InitialRbfThreshold(),
    "protocol:layer[RBF].attribute_weight_method": AttributeWeightMethod(layer_name="RBF"),
    "protocol:layer[RBF].initial_attribute_weights": AttributeWeights(layer_name="RBF"),
    "protocol:layer[A].attribute_weight_method": AttributeWeightMethod(layer_name="A"),
    "protocol:layer[A].initial_attribute_weights": AttributeWeights(layer_name="A"),
    "protocol:layer[RBF].matcher_method": MatcherMethod(layer_name="RBF"),
    "protocol:copy": Repetition(),
}

