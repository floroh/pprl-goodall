from pprl_protocol_manager_service_api_client import MultiLayerProtocol

import streamlit as st
from streamlit import session_state as sts

from goodall.api_helper import pm_api
from goodall.ui.components.protocol_list import (
    render_protocol_list,
    render_selected_protocol_json,
)


if "protocols" not in sts:
    sts["protocols"] = pm_api.get_protocols()
protocols: list[MultiLayerProtocol] = sts["protocols"]

render_protocol_list((protocols))
with st.expander("Protocol json", expanded=False):
    render_selected_protocol_json()
