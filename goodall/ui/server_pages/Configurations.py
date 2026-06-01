import pprl_data_owner_service_api_client as do
import pprl_linkage_unit_service_api_client as lu
from pprl_data_owner_service_api_client import (
    EncodingIdDto,
)
from pprl_linkage_unit_service_api_client import MatcherIdDto

from goodall.api_helper.pprl_clients import Service, get_client
from goodall.ui.streamlit_utils import (
    st,
    sts,
)


@st.cache_data
def get_configs(service: Service) -> list:
    if service == Service.Linkage_unit:
        controller = lu.ConfigurationManagementApi(get_client(service))
    else:
        controller = do.ConfigurationManagementApi(get_client(service))
    return controller.get_configs()


def get_config(service: Service, config_name: str):
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


def delete_config(service: Service, config_name: str, project: str | None = None):
    if service == Service.Linkage_unit:
        controller = lu.ConfigurationManagementApi(get_client(service))
        return controller.remove1(
            MatcherIdDto.from_dict({"method": config_name, "project": project})
        )
    else:
        controller = do.ConfigurationManagementApi(get_client(service))
        return controller.remove1(
            EncodingIdDto.from_dict({"method": config_name, "project": project})
        )

sel_source = st.segmented_control(
    "Select source",
    ["Encoding", "Matching"],
    on_change=lambda: get_configs.clear(),
)
if not sel_source:
    st.stop()

service = [
    Service.Data_owner_1 if sel_source == "Encoding" else Service.Linkage_unit
].pop()
sts["selected_service"] = service

if "selected_service" in sts:
    configs = get_configs(sts["selected_service"])
    config_names = [config.method for config in configs]
    selected_config = st.selectbox("Select config", ["Select..."] + config_names)

    if selected_config is not None and selected_config != "Select...":
        st.text(selected_config)
        if sel_source == "Encoding":
            if st.button("Delete config"):
                delete_config(sts["selected_service"], selected_config)
                get_configs.clear()
                st.rerun()
        config = get_config(sts["selected_service"], selected_config)
        st.json(config)
