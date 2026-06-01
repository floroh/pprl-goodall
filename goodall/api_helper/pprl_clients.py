import os
from enum import Enum

from dotenv import load_dotenv
from loguru import logger

import pprl_protocol_manager_service_api_client as pm
import pprl_data_generator_service_api_client as dg
import pprl_linkage_unit_service_api_client as lu
import pprl_data_owner_service_api_client as do

from goodall.models.services import ServiceStatus

load_dotenv(override=False)
logger.debug("loading env")


class Service(Enum):
    Protocol_manager = 0
    Data_generator = 1
    Linkage_unit = 2
    Data_owner_1 = 3
    Data_owner_2 = 4


def client_status() -> list[ServiceStatus]:
    """
    Checks the status of all services
    """
    results = []
    for service in Service:
        if service == Service.Data_owner_2:
            continue  # Exclude data owner 2 because it is not used for evaluations
        results.append(ServiceStatus(
            name=service.name.replace("_", " "),
            healthy=client_health_check(service),
            endpoint=get_endpoint(service),
        ))
    results.sort(key=lambda s: s.name)
    return results

def client_health_checks(as_string: bool = False) -> dict[str, bool] | dict[Service, bool]:
    """
    Checks the health of all services and returns a dict: Service -> health (True/False)
    """
    return {(service.name if as_string else service): client_health_check(service)
            for service in Service}

def client_health_check(service: Service):
    client = get_client(service)
    health_response = None
    try:
        match service:
            case Service.Protocol_manager:
                health_response = pm.ActuatorApi(client).health()
            case Service.Data_generator:
                health_response = dg.ActuatorApi(client).health()
            case Service.Linkage_unit:
                health_response = lu.ActuatorApi(client).health()
            case Service.Data_owner_1:
                health_response = do.ActuatorApi(client).health()
            case Service.Data_owner_2:
                health_response = do.ActuatorApi(client).health()
        if isinstance(health_response, dict):
            return health_response.get("status") == "UP"
        return False
    except Exception:
        return False

def get_client(service: Service):
    match service:
        case Service.Protocol_manager:
            return pm.ApiClient(pm.Configuration(host=get_endpoint(service)))
        case Service.Data_generator:
            return dg.ApiClient(dg.Configuration(host=get_endpoint(service)))
        case Service.Linkage_unit:
            return lu.ApiClient(lu.Configuration(host=get_endpoint(service)))
        case Service.Data_owner_1:
            return do.ApiClient(do.Configuration(host=get_endpoint(service)))
        case Service.Data_owner_2:
            return do.ApiClient(do.Configuration(host=get_endpoint(service)))


def get_endpoint(service: Service):
    endpoint = None
    match service:
        case Service.Protocol_manager:
            endpoint = get_protocol_manager_endpoint()
        case Service.Data_generator:
            endpoint = get_data_generator_endpoint()
        case Service.Linkage_unit:
            endpoint = get_linkage_unit_endpoint()
        case Service.Data_owner_1:
            endpoint = get_data_owner_1_endpoint()
        case Service.Data_owner_2:
            endpoint = get_data_owner_2_endpoint()
    logger.debug(f"Endpoint for {service.name}: {endpoint}")
    return endpoint


def get_protocol_manager_endpoint():
    return os.getenv("PPRL_SERVICES_PROTOCOL_MANAGER_ENDPOINT", "http://localhost:8085")


def get_data_generator_endpoint():
    return os.getenv("PPRL_SERVICES_DATA_GENERATOR_ENDPOINT", "http://localhost:8086")


def get_linkage_unit_endpoint():
    return os.getenv("PPRL_SERVICES_LINKAGE_UNIT_ENDPOINT", "http://localhost:8082")


def get_data_owner_1_endpoint():
    return os.getenv("PPRL_SERVICES_DATA_OWNER_ENDPOINT", "http://localhost:8081")


def get_data_owner_2_endpoint():
    return os.getenv("PPRL_SERVICES_DATA_OWNER_2_ENDPOINT", "http://localhost:8083")
