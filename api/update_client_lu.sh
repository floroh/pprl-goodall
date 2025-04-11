#!/usr/bin/env sh
mv ./api/lu-api-docs.json ./api/lu-api-docs-bak.json
curl http://localhost:8082/v3/api-docs | python -m json.tool > ./api/lu-api-docs.json
rm -rf ./api/pprl-linkage-unit-service-api-client
docker run --rm --user "$(id -u):$(id -g)" -v "${PWD}"/api:/local openapitools/openapi-generator-cli:v7.9.0 generate -i /local/lu-api-docs.json -g python -o /local/pprl-linkage-unit-service-api-client --skip-validate-spec --additional-properties=packageName=pprl_linkage_unit_service_api_client
pip uninstall -y pprl_linkage_unit_service_api_client
poetry install