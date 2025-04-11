import streamlit as st
import pprl_data_owner_service_api_client as do
import pprl_linkage_unit_service_api_client as lu
from pprl_data_owner_service_api_client import (
    DatasetAnalysisApi,
    AnalysisResultDto,
    EncodingIdDto,
)
from pprl_data_owner_service_api_client.models import AnalysisRequestDto
from pprl_linkage_unit_service_api_client import MatcherIdDto

from goodall.api_helper.parser import parse_serialized_table_to_dataframe
from goodall.api_helper.pprl_clients import Service, get_client
from goodall.ui.streamlit_utils import del_state_if_exists

st.set_page_config(layout="wide", page_title="Configurations")


@st.cache_data
def get_configs(service: Service) -> list:
    if service == Service.Linkage_unit:
        controller = lu.ConfigurationManagementApi(get_client(service))
    else:
        controller = do.ConfigurationManagementApi(get_client(service))
    return controller.get_configs()


def get_matching_config(service: Service, config_name: str):
    if service == Service.Linkage_unit:
        controller = lu.ConfigurationManagementApi(get_client(service))
        return controller.get_matching(
            MatcherIdDto.from_dict({"method": config_name})
        ).to_dict()["config"]
    else:
        controller = do.ConfigurationManagementApi(get_client(service))
        return controller.get_encoding(
            EncodingIdDto.from_dict({"method": config_name})
        ).to_dict()["config"]


sel_source = st.selectbox(
    "Select source",
    ["Select...", "Plain", "Encoded"],
    on_change=lambda: get_configs.clear(),
)
if sel_source == "Select...":
    del_state_if_exists("selected_service")
else:
    service = [
        Service.Data_owner_1 if sel_source == "Plain" else Service.Linkage_unit
    ].pop()
    st.session_state["selected_service"] = service

if "selected_service" in st.session_state:
    configs = get_configs(st.session_state["selected_service"])
    config_names = [config.method for config in configs]
    selected_config = st.selectbox("Select config", ["Select..."] + config_names)

    if selected_config is not None and selected_config != "Select...":
        st.text(selected_config)
        config = get_matching_config(
            st.session_state["selected_service"], selected_config
        )
        st.json(config)
