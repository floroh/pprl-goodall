import logging
from typing import List

import pprl_protocol_manager_service_api_client as pm
from pprl_protocol_manager_service_api_client import MultiLayerProtocol, DatasetCsvDto, \
    EncodedTransferRequestDto, ProtocolExecutionDto

from goodall.api_helper.pprl_clients import Service, get_client

client = get_client(Service.Protocol_Manager)
do_preparation_controller = pm.DataOwnerPreparationApi(client)
protocol_manager_controller = pm.PPRLProtocolManagerApi(client)

logger = logging.getLogger(__name__)


def add_data_owner_dataset(csv_dataset: DatasetCsvDto):
    do_preparation_controller.insert_from_csv(csv_dataset)


def transfer_encoded_dataset(transfer_request: EncodedTransferRequestDto) -> int:
    return protocol_manager_controller.transfer_encoded(transfer_request)


def get_protocol(protocol_id: str) -> MultiLayerProtocol:
    return protocol_manager_controller.get_multi_layer_protocol(protocol_id)


def get_example_protocol() -> MultiLayerProtocol:
    return protocol_manager_controller.get_example_multi_layer_protocol()


def delete_protocol(protocol_id: str):
    return protocol_manager_controller.delete_multi_layer_protocol(protocol_id)


def get_protocols() -> list[MultiLayerProtocol]:
    return protocol_manager_controller.find_all()


def create_example_3_layer_protocol(do_dataset_id: int = 2012,
                                    lu_dataset_id: int = 2212,
                                    initial_threshold: float = 0.75,
                                    ppcr_budget: int = 200,
                                    ppcr_batch_size_config: List[int]|None = None) -> MultiLayerProtocol:
    if ppcr_batch_size_config is None:
        ppcr_batch_size_config = [20]
    protocol = protocol_manager_controller.get_example_multi_layer_protocol(protocol_type="RBF-ABF-PPCR")
    protocol.plaintext_dataset_id = do_dataset_id
    protocol.initial_dataset_id = lu_dataset_id
    protocol.layers[0].initial_threshold = initial_threshold
    protocol.layers[2].budget = ppcr_budget
    protocol.layers[2].max_batches = 1
    protocol.layers[2].error_rate = 0.05
    protocol.layers[2].batch_size_config = ppcr_batch_size_config
    protocol.layers[2].batch_size = ppcr_batch_size_config[0]
    return protocol
    # return create_protocol(protocol)

def create_example_rbf_ppcr_layer_protocol(do_dataset_id: int = 2012,
                                    lu_dataset_id: int = 2212,
                                    initial_threshold: float = 0.75,
                                    ppcr_budget: int = 200,
                                    ppcr_batch_size_config: List[int]|None = None,
                                     max_batches: int = 10) -> MultiLayerProtocol:
    if ppcr_batch_size_config is None:
        ppcr_batch_size_config = [20]
    protocol = protocol_manager_controller.get_example_multi_layer_protocol(protocol_type="RBF-PPCR")
    protocol.plaintext_dataset_id = do_dataset_id
    protocol.initial_dataset_id = lu_dataset_id
    protocol.layers[0].initial_threshold = initial_threshold
    protocol.layers[1].budget = ppcr_budget
    protocol.layers[1].max_batches = max_batches
    protocol.layers[1].batch_size_config = ppcr_batch_size_config
    protocol.layers[1].batch_size = ppcr_batch_size_config[0]
    return create_protocol(protocol)

def create_example_abf_ppcr_protocol(do_dataset_id: int = 2012,
                                     lu_dataset_id: int = 2112,
                                     ppcr_budget: int = 200,
                                     ppcr_batch_size_config: List[int]|None = None,
                                     max_batches: int = 10) -> MultiLayerProtocol:
    if ppcr_batch_size_config is None:
        ppcr_batch_size_config = [5]
    protocol = protocol_manager_controller.get_example_multi_layer_protocol(protocol_type="ABF-PPCR")
    protocol.plaintext_dataset_id = do_dataset_id
    protocol.initial_dataset_id = lu_dataset_id
    protocol.layers[0].matcher_method = "DBSLeipzig/ABF/Freq/PB/Weka/WEKA_EXP_RANDOM_FOREST/trained/2112/675332752c3b2f74050b1acb"
    protocol.layers[1].budget = ppcr_budget
    protocol.layers[1].max_batches = max_batches
    protocol.layers[1].batch_size_config = ppcr_batch_size_config
    protocol.layers[1].batch_size = ppcr_batch_size_config[0]
    return create_protocol(protocol)


def create_protocol(protocol: MultiLayerProtocol) -> MultiLayerProtocol:
    return protocol_manager_controller.create_multi_layer_protocol(protocol)


def update_protocol(protocol: MultiLayerProtocol) -> MultiLayerProtocol:
    return protocol_manager_controller.update_multi_layer_protocol(protocol)


def skip_next_step_in_protocol(protocol: MultiLayerProtocol) -> MultiLayerProtocol:
    return protocol_manager_controller.skip_step_of_multi_layer_protocol(
        protocol.protocol_id)


def run_protocol_no_stop(protocol_id: str) -> MultiLayerProtocol:
    return run_protocol(ProtocolExecutionDto(protocol_id=protocol_id))


def run_protocol_single_step(protocol_id: str) -> MultiLayerProtocol:
    return run_protocol(
        ProtocolExecutionDto(protocol_id=protocol_id, number_of_steps=1))


def run_protocol(execution_dto: ProtocolExecutionDto) -> MultiLayerProtocol:
    return protocol_manager_controller.run_multi_layer_protocol(execution_dto)
