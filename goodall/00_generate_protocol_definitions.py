from pprl_protocol_manager_service_api_client import MultiLayerProtocol

from goodall.api_helper.pm_api import protocol_manager_controller

optimal_thresholds = {
    2032: 0.80,
    2230: 0.76,
    2232: 0.75,
    2234: 0.75,
    2240: 0.73,
    2242: 0.71,
    2330: 0.69,
    2332: 0.67,
    2334: 0.66,
}


def generate_values_in_range(center: float = 0.0, delta: float = 0.05, step_size: float = 0.01):
    values = []
    start = round(center - delta, 2)
    end = round(center + delta, 2)

    current = start
    while current <= (end + 0.001):
        values.append(round(current, 2))  # Round to avoid floating-point precision issues
        current += step_size
    return values


def write_protocol_definition_to_file(protocol: MultiLayerProtocol, path: str):
    with open(path, "w") as file:
        dump = protocol.model_dump_json(indent=2, exclude_none=True)
        file.write(dump)


def get_protocol_definition(
        plaintext_dataset_id: int,
        budget: int,
        error_rate: float,
        threshold_delta: float,
        xor_hardening: bool = False,
) -> MultiLayerProtocol:

    protocol = protocol_manager_controller.get_example_multi_layer_protocol(protocol_type="RBF-ABF-PPCR")

    encoded_dataset_id = plaintext_dataset_id + 200
    if xor_hardening:
        protocol.layers[0].encoding_method = "DBSLeipzig/RBF/NCVR-F-avg-xor"
        encoded_dataset_id += 100

    ppcr_batch_size_config = [int(budget / 10)]

    optimal_threshold = optimal_thresholds[encoded_dataset_id]

    protocol.plaintext_dataset_id = plaintext_dataset_id
    protocol.initial_dataset_id = encoded_dataset_id
    protocol.layers[0].initial_threshold = round(optimal_threshold + threshold_delta, 2)
    protocol.layers[1].max_batches = 9
    protocol.layers[2].budget = budget
    protocol.layers[2].max_batches = 2
    protocol.layers[2].error_rate = error_rate
    protocol.layers[2].batch_size_config = ppcr_batch_size_config
    protocol.layers[2].batch_size = ppcr_batch_size_config[0]
    protocol.layers[2].encoding_method = "DBSLeipzig/Plain/Selective"
    return protocol


if __name__ == "__main__":
    plaintext_dataset_id = 2030  # E1S
    # plaintext_dataset_id = 2032  # E1M
    # plaintext_dataset_id = 2034  # E1L
    # plaintext_dataset_id = 2040  # E2S
    # plaintext_dataset_id = 2042  # E2M
    threshold_deltas = generate_values_in_range(step_size=0.01)
    budget = 300
    error_rate = 0.2
    xor_hardening = False
    for threshold_delta in threshold_deltas:
        protocol = get_protocol_definition(
            plaintext_dataset_id=plaintext_dataset_id,
            budget=budget,
            error_rate=error_rate,
            threshold_delta=threshold_delta,
            xor_hardening=xor_hardening,
        )

        path = "experiment-definitions/fig5/"
        path += f"{plaintext_dataset_id}"
        path += f"-b{budget}"
        path += f"-e{error_rate}"
        path += f"-t{threshold_delta}"
        path += f".json"

        write_protocol_definition_to_file(protocol, path)
