from pprl_protocol_manager_service_api_client import MultiLayerProtocol

from goodall.api_helper import pm_api
from goodall.api_helper.pm_api import delete_protocol, get_protocol
from goodall.ui.PPRL_Services_UI import SELECTED_PROTOCOL_ID
from goodall.ui.components.protocols import prepareProtocolsForDisplay, btn_protocol_refresh, btn_protocol_unselect, \
    btn_protocol_selector, get_indexed_state_key
import streamlit as st

from goodall.ui.streamlit_utils import del_state_if_exists

sts = st.session_state


def render_protocol_list(protocols: list[MultiLayerProtocol]):
    st.header("Linkage protocols (" + str(len(protocols)) + ")")
    protocols = prepareProtocolsForDisplay(protocols)

    for protocol in protocols:
        col1, col2, col3, col4 = st.columns([1, 1, 2, 1])
        with col1:
            btn_protocol_selector(protocol.protocol_id)
            st.text(protocol.last_update)
        with col2:
            st.write("plain dataset: " + str(protocol.plaintext_dataset_id))
            st.write("initial dataset: " + str(protocol.initial_dataset_id))
        with col3:
            btn_delete = st.button("Delete", key="del" + protocol.protocol_id)
            if btn_delete:
                delete_protocol(protocol.protocol_id)
                sts["protocols"] = pm_api.get_protocols()
                del_state_if_exists(get_indexed_state_key(SELECTED_PROTOCOL_ID))
                st.rerun()
    btn_protocol_refresh()
    btn_protocol_unselect()

def render_selected_protocol_json():
    if SELECTED_PROTOCOL_ID in sts:
        pr = get_protocol(sts[SELECTED_PROTOCOL_ID])
        st.json(pr.to_json(), expanded=True)