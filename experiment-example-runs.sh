#!/usr/bin/sh

# Import csv dataset based on the North Carolina Voter Registry
docker compose run --rm pprl-goodall-cli run -c test-create-import-csv.json

# Generate and corrupt dataset variants
docker compose run --rm pprl-goodall-cli run -c test-create-generate.json
docker compose run --rm pprl-goodall-cli run -c test-create-corrupt.json

# Create mlflow experiment runs with all required configuration for encoding etc.
docker compose run --rm pprl-goodall-cli schedule -i test-datasets.json -c test-linkage-rbf-weights.json

# Sequentially execute the scheduled experiment runs
docker compose run --rm pprl-goodall-cli execute

# Update the mlflow runs and derive additional metrics from the logs
docker compose run --rm pprl-goodall-cli update -e test-linkage