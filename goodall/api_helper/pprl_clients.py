from enum import Enum

import pprl_data_owner_service_api_client as do
import pprl_linkage_unit_service_api_client as lu
import pprl_protocol_manager_service_api_client as pm


class Service(Enum):
    Protocol_Manager = 0
    Linkage_unit = 1
    Data_owner_1 = 2


def get_client(service: Service):
    match service:
        case Service.Protocol_Manager:
            return pm.ApiClient(pm.Configuration(host=get_endpoint(service)))
        case Service.Linkage_unit:
            return lu.ApiClient(lu.Configuration(host=get_endpoint(service)))
        case Service.Data_owner_1:
            return do.ApiClient(do.Configuration(host=get_endpoint(service)))


def get_endpoint(service: Service):
    match service:
        case Service.Protocol_Manager:
            return get_protocol_manager_endpoint()
        case Service.Linkage_unit:
            return get_linkage_unit_endpoint()
        case Service.Data_owner_1:
            return get_data_owner_1_endpoint()


def get_protocol_manager_endpoint():
    return "http://localhost:8085"


def get_data_owner_1_endpoint():
    return "http://localhost:8081"


def get_linkage_unit_endpoint():
    return "http://localhost:8082"
