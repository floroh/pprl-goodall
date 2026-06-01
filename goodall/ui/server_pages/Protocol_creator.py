from goodall.api_helper import pm_api
from goodall.ui.constants import SELECTED_PROTOCOL_ID
from goodall.ui.components.protocols import section_create_protocol
from goodall.ui.streamlit_utils import st, sts

section_create_protocol(show_only_datasets_with_name=False)

btnContinueProtocol = st.button("Run/Continue")
if btnContinueProtocol:
    pm_api.run_protocol_no_stop(sts[SELECTED_PROTOCOL_ID])
