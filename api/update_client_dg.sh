#!/usr/bin/env sh
mv ./api/dg-api-docs.json ./api/dg-api-docs-bak.json
curl http://localhost:8186/v3/api-docs | python -m json.tool > ./api/dg-api-docs.json
rm -rf ./api/pprl-data-generator-service-api-client
docker run --rm --user "$(id -u):$(id -g)" -v "${PWD}"/api:/local openapitools/openapi-generator-cli:v7.22.0 generate -i /local/dg-api-docs.json -g python -o /local/pprl-data-generator-service-api-client --skip-validate-spec --additional-properties=packageName=pprl_data_generator_service_api_client
pip uninstall -y pprl_data_generator_service_api_client
poetry install