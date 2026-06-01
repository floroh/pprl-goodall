import pathlib

from pprl_protocol_manager_service_api_client import MultiLayerProtocol

from goodall.api_helper import pm_api, pprl_clients
from goodall.ui.components.comparison_renderer import (
    render_multi_layer_comparison_examples,
)
from goodall.ui.components.protocol_introduction import render_protocol_introduction
from goodall.ui.components.protocol_list import (
    render_protocol_list,
    render_selected_protocol_json,
)
from goodall.ui.components.protocol_renderer import ProtocolRenderer
from goodall.ui.components.protocols import (
    btn_protocol_unselect,
    section_create_protocol,
    btn_select_most_recent_protocol_selector,
)
from goodall.ui.constants import SELECTED_PROTOCOL_ID
from goodall.ui.streamlit_utils import (
    st,
    sts,
    get_state_or_default,
    load_css,
)

load_css(pathlib.Path("static/css/styles.css"))

sts["view_mode"] = st.sidebar.selectbox("View mode", ["Simple", "Expert"])
sts["knowledge_mode"] = get_state_or_default("knowledge_mode", "Evaluation")
# sts["knowledge_mode"] = st.sidebar.selectbox("Knowledge mode",
#                                              ["Simple", "Evaluation"],
#                                              # ["Simple", "Enhanced", "Evaluation"],
#                                              index=1)

btn_protocol_unselect(sidebar=True)

if "protocols" not in sts:
    sts["protocols"] = pm_api.get_protocols()
protocols: list[MultiLayerProtocol] = sts["protocols"]

if sts["view_mode"] == "Expert":
    st.text("State")
    st.json(sts, expanded=False)
    btn_clear_state = st.button("Clear State")
    if btn_clear_state:
        for key in sts.keys():
            del sts[key]
        st.rerun()
    st.text("Protocols")
    st.json(protocols, expanded=False)

# del_state_if_exists("auto_continue_protocol")
tab_intro, tab_create, tab_run, tab_manage, tab_services = st.tabs(
    ["Introduction", "Setup", "Execution", "Management", "Technical background"]
)

with tab_intro:
    # st.header("Clerical review for Privacy-Preserving Record Linkage")
    st.markdown(
        "<h1 style='font-size: 2.5em;'>S<span style='color: gray;'>ec</span>URE" +
        "<span style='color: gray;'>match</span>: " +
        "Clerical Review for Privacy-Preserving Record Linkage</h1>",
        unsafe_allow_html=True,
    )
    col1, col2 = st.columns([2, 2])
    with col1:
        render_protocol_introduction()
    with col2:
        render_multi_layer_comparison_examples()
        # get_protocol_step_graph(None)
with tab_create:
    section_create_protocol(
        dataset_name_mapping={
            2010: "North Carolina Voter Registry 10k-10k-1k",
            2012: "North Carolina Voter Registry 10k-10k-2k",
            2032: "North Carolina Voter Registry 50k-50k-10",
        },
        protocol_options=["RBF-ABF-PPCR", "ABF-PPCR", "RBF-PPCR"],
    )

with tab_run:
    btn_select_most_recent_protocol_selector()
    if SELECTED_PROTOCOL_ID in sts:
        pr = pm_api.get_protocol(sts[SELECTED_PROTOCOL_ID])
        pr_renderer = ProtocolRenderer(pr)
        # if 'error' in prj.to_dict() and prj['error'] is not None:
        if pr is None or "error" in pr.to_dict():
            if pr is None:
                st.error(
                    "Could not fetch protocol with id " + sts[SELECTED_PROTOCOL_ID]
                )
            else:
                st.error(pr.to_dict())
            st.stop()
        if sts["view_mode"] == "Expert":
            st.json(pr.to_json(), expanded=False)
            st.header(f"Selected protocol: {sts[SELECTED_PROTOCOL_ID]}")
        pr_renderer.render()

with tab_manage:
    render_protocol_list(protocols)
    render_selected_protocol_json()

with tab_services:
    st.header("PPRL Services APIs")
    st.markdown("""
    The frontend is implemented as a [streamlit](https://streamlit.io/) app.\n
    The backend services for Data Owner and Linkage Unit as well as for management
    the protocol progress are implemented as
    [Spring Boot Applications](https://docs.spring.io/spring-boot/index.html).\n
    The backend services use [MongoDB](http://mongodb.com) for persistence of the 
    datasets, final and intermediate linkage results as well as the protocol 
    configuration and execution state.
    """)
    with st.expander("Data Owner Service", expanded=True):
        st.iframe(
            f"{pprl_clients.get_data_owner_1_endpoint()}/swagger-ui/index.html",
            height=800
        )
    with st.expander("Linkage Unit Service", expanded=False):
        st.iframe(
            f"{pprl_clients.get_linkage_unit_endpoint()}/swagger-ui/index.html",
            height=800
        )
    with st.expander("Protocol Manager Service", expanded=False):
        st.iframe(
            f"{pprl_clients.get_protocol_manager_endpoint()}/swagger-ui/index.html",
            height=800
        )
