from pprl_protocol_manager_service_api_client import ProtocolAnalysisRequestDto

from goodall.api_helper.pm_api import protocol_analyzer_controller


def fetch_tags_of_protocol(protocol_id: str):
    tags = protocol_analyzer_controller.get_all_tags_as_table(ProtocolAnalysisRequestDto(protocolId=protocol_id))
    return tags
