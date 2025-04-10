import argparse
import csv
import os
import time
from typing import List

from pprl_protocol_manager_service_api_client import MultiLayerProtocol
from goodall.api_helper import pm_api


def create_protocol(path: str) -> MultiLayerProtocol:
    with open(path, 'r') as file:
        data = file.read()
        protocol = MultiLayerProtocol.model_validate_json(data)
        protocol = pm_api.create_protocol(protocol)
        return protocol

def get_protocol_definition_paths(directory: str) -> List[str]:
    json_files = []
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        if os.path.isfile(file_path) and filename.endswith('.json'):
            json_files.append(file_path)
    json_files.sort()
    return json_files


def run_protocols_and_log(paths: List[str], repetitions: int, csv_file: str):
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['experiment-definition', 'repetition', 'protocolId'])
        current_experiment = 0
        total_experiments = len(paths) * repetitions
        for path in paths:
            current_repetition = 0
            while current_repetition < repetitions:
                start_time = time.time()
                protocol = create_protocol(path)
                protocol_id = protocol.protocol_id
                print(f"Running {current_experiment * repetitions + current_repetition + 1}/{total_experiments}: {path}, repetition {current_repetition}, protocol id {protocol_id}")
                writer.writerow([path, current_repetition, protocol_id])
                file.flush()

                pm_api.run_protocol_no_stop(protocol_id)
                current_repetition += 1
                end_time = time.time()
                print(f"\tFinished in {end_time - start_time} seconds")
            current_experiment += 1

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("experiment_set",
                        help="Set of experiments for a paper figure (fig3, fig4_left, fig4_right, fig5)")  # Add arguments here
    parser.add_argument("--reduce_threshold_density", action=argparse.BooleanOptionalAction,
                        help="Use 3 instead of 11 initial thresholds [t_opt - 0.05, t_opt, t_opt + 0.05]")  # Add arguments here
    args = parser.parse_args()
    experiment_set = args.experiment_set
    paths = get_protocol_definition_paths(os.path.join("experiment-definitions", args.experiment_set))
    if args.reduce_threshold_density:
        paths = [p for p in paths if any(substring in p for substring in ["t0.0.", "t-0.05.", "t0.05."])]
    output_directory = os.path.join("results", experiment_set)
    if not os.path.exists(output_directory):
        os.mkdir(output_directory)
    repetitions = 1 if experiment_set == "baselines" else 3
    run_protocols_and_log(paths, repetitions, os.path.join(output_directory, "protocol_log.csv"))

if __name__ == '__main__':
    main()
