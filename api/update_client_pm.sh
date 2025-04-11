#!/usr/bin/env sh
mv ./api/pm-api-docs.json ./api/pm-api-docs-bak.json
curl http://localhost:8085/v3/api-docs | python -m json.tool > ./api/pm-api-docs.json
rm -rf ./api/pprl-protocol-manager-service-api-client
docker run --rm --user "$(id -u):$(id -g)" -v "${PWD}"/api:/local openapitools/openapi-generator-cli:v7.9.0 generate -i /local/pm-api-docs.json -g python -o /local/pprl-protocol-manager-service-api-client --skip-validate-spec --additional-properties=packageName=pprl_protocol_manager_service_api_client
pip uninstall -y pprl_protocol_manager_service_api_client
poetry install