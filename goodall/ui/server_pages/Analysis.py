import pandas as pd
from pprl_protocol_manager_service_api_client import MultiLayerProtocol

from goodall.api_helper import pm_api
from goodall.api_helper.pm_api import get_protocol
from goodall.ui.components.protocol_tag_analyzer_from_services import ProtocolTagFromServicesAnalyzer
from goodall.ui.constants import SELECTED_PROTOCOL_ID

from goodall.ui.streamlit_utils import (
    st,
    sts,
    del_state_if_exists,
)


if st.button("Refresh protocol list"):
    del_state_if_exists("protocols")
    del_state_if_exists(SELECTED_PROTOCOL_ID)

if "protocols" not in sts:
    sts["protocols"] = pm_api.get_protocols()
protocols: list[MultiLayerProtocol] = sts["protocols"]


@st.cache_data
def get_tags(protocol_id: str) -> pd.DataFrame:
    return ProtocolTagFromServicesAnalyzer.get_df_tags(protocol_id)


# protocols.reverse()
# if SELECTED_PROTOCOL_ID not in sts:
selected_protocol = st.selectbox(
    "Select protocol",
    protocols,
    format_func=lambda p: f"{p.last_update} {p.protocol_id}",
)
sts[SELECTED_PROTOCOL_ID] = selected_protocol.protocol_id

protocol_id = sts[SELECTED_PROTOCOL_ID]
st.text(f"Selected protocol: {protocol_id}")
st.write("plain dataset: " + str(selected_protocol.plaintext_dataset_id))
st.write("initial dataset: " + str(selected_protocol.initial_dataset_id))
use_non_gt_type = st.toggle("Simulate missing ground truth")
if st.button("Analyze"):
    pr = get_protocol(protocol_id)
    analyzer = ProtocolTagFromServicesAnalyzer(pr, get_tags(protocol_id))
    if use_non_gt_type:
        analyzer.simulate_missing_gt = use_non_gt_type
    # analyzer.render_tags()
    analyzer.analyze()
