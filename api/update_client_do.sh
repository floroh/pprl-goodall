#!/usr/bin/env sh
mv ./api/do-api-docs.json ./api/do-api-docs-bak.json
curl http://localhost:8081/v3/api-docs | python -m json.tool > ./api/do-api-docs.json
rm -rf ./api/pprl-data-owner-service-api-client
docker run --rm --user "$(id -u):$(id -g)" -v "${PWD}"/api:/local openapitools/openapi-generator-cli:v7.9.0 generate -i /local/do-api-docs.json -g python -o /local/pprl-data-owner-service-api-client --skip-validate-spec --additional-properties=packageName=pprl_data_owner_service_api_client
pip uninstall -y pprl_data_owner_service_api_client
poetry install