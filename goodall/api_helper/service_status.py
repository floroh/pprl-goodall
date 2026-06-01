from loguru import logger
from goodall.api_helper import pm_api
from goodall.api_helper.pprl_clients import client_status
from goodall.models.services import ServiceStatus
from goodall.tracking.mlflow_utils import check_mlflow_server_connection, \
    check_mlflow_artifact_storage_connection

def get_service_health_checks(
        check_pprl_service_availability: bool = True,
        check_pm_connectivity: bool = True,
        check_mlflow: bool = False
) -> list[ServiceStatus]:
    results = []
    if check_pprl_service_availability:
        logger.info("Checking service status...")
        results.extend(client_status())
    if check_pm_connectivity:
        results.append(pm_api.check_connections())
    if check_mlflow:
        logger.info("Checking mlflow server connection...")
        results.append(check_mlflow_server_connection())
        logger.info("Checking mlflow artifact storage connection...")
        results.append(check_mlflow_artifact_storage_connection())
    return results