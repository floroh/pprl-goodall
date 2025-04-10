# Multi-Layer Privacy-Preserving Record Linkage with Clerical Review based on gradual information disclosure
Reproducibility information for Paper
"Multi-Layer Privacy-Preserving Record Linkage with Clerical Review based on gradual information disclosure"
by Florens Rohde, Victor Christen, Martin Franke, Erhard Rahm

## Setup
### Hardware requirements
- nothing special, but high disk read and write speed is beneficial for the database operations
- runs on Lenovo Thinkpad T480s with 16GB memory and m.2 SSD (PCIe Gen3)

### Software requirements
- Docker (tested: v27.4.1)
- Python 3.12
- [Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer) (tested: v1.8.5)
  - `curl -sSL https://install.python-poetry.org | python3 - --version 1.8.5`

### Download datasets
```shell
cd datasets
./download_datasets.sh
```
### Start PPRL service test infrastructure
```shell
docker compose -f pprl-services/docker-compose.yml up -d
```
- includes
  - data owner service (localhost:8081)
  - linkage unit service (localhost:8082)
  - protocol manager service (localhost:8085)
  - shared MongoDB instance


## Run experiments
- Expect the following runtimes:
  - ~15min/experiment x 3 repetitions x 11 initial_thresholds
    - ... x (3 error_rates for b=100 + 2 further budgets for e=0.2) = 41h  # Fig 3, Fig 6 left
    - ... x (4 datasets * 2 budgets) = 66h  # Fig 4 (left and right: 33h each), Fig 6 right
    - ... x (3 datasets) = 25h  # Fig 5
  - Total: 132h
  - Reduced experiment set with 3 initial thresholds: 36h
    - add `--reduce_threshold_density` for 02_run_multi_layer_protocols.py
- Please note that there are components with randomness in the protocol without a fixed seed.
  - Thus, the results will vary on each run.

### Execution order
```shell
# Required steps for all of the following sets
poetry install
poetry shell
python -m goodall.01_import_plaintext_datasets

# ABF Baselines
python -m goodall.02_run_multi_layer_protocols baselines  # Faster than other experiments
python -m goodall.03_fetch_results baselines  # Prints F1 scores of ABF Baselines and ABF values for Table 4

# The following experiment sets are independent and can be run on different machines to reproduce the respective experiments.
# It is also beneficial for the runtimes to separate them when using a single machine as it reduces the database size
# and query response times. This can be accomplished by following the steps:
docker compose -f pprl-services/docker-compose.yml down
mv pprl-services/btw-mongo-storage pprl-services/btw-mongo-storage.old # Choose other target when doing this more than once
docker compose -f pprl-services/docker-compose.yml up -d
python -m goodall.01_import_plaintext_datasets  # Import the plaintext datasets again


# Experiment set: E1M dataset
python -m goodall.02_run_multi_layer_protocols --reduce_threshold_density fig3
python -m goodall.03_fetch_results fig3
python -m goodall.04_quality_plots fig3_left
python -m goodall.04_quality_plots fig3_right
python -m goodall.05_privacy_plots fig6_left
python -m goodall.06_privacy_table  # Prints KABF values for Table 4

# Experiment set: E1S and E1L datasets
python -m goodall.02_run_multi_layer_protocols --reduce_threshold_density fig4_left
python -m goodall.03_fetch_results fig4_left
python -m goodall.04_quality_plots fig4_left

# Experiment set: E2S and E2M datasets
python -m goodall.02_run_multi_layer_protocols --reduce_threshold_density fig4_right
python -m goodall.03_fetch_results fig4_right
python -m goodall.04_quality_plots fig4_right
python -m goodall.05_privacy_plots fig6_right

# Experiment set: E1-XOR datasets
python -m goodall.02_run_multi_layer_protocols --reduce_threshold_density fig5
python -m goodall.03_fetch_results fig5
python -m goodall.04_quality_plots fig5
```
