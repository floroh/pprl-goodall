
import streamlit as st
import pprl_linkage_unit_service_api_client as lu

from pprl_protocol_manager_service_api_client import MultiLayerProtocol, ReportGroup
from st_link_analysis import NodeStyle, EdgeStyle, st_link_analysis, Event
from streamlit import session_state as sts


from goodall.api_helper import pm_api, lu_api
from goodall.api_helper.parser import (
    parse_serialized_table_to_dataframe,
)
from goodall.api_helper.pprl_clients import Service
from goodall.result_analysis.pair_evaluation import *
from goodall.ui.PPRL_Services_UI import *
from goodall.ui.components.datasets import get_dataset_ids, get_dataset_analysis_result
from goodall.ui.components.project_comparison import get_merged_record_pair_df
from goodall.ui.pages.Datasets import render_data_owner_dataset_description
from goodall.ui.streamlit_utils import del_state_if_exists


def prepareProtocolsForDisplay(protocols: list[MultiLayerProtocol]):
    if NUMBER_OF_SHOW_PROJECTS not in sts:
        sts[NUMBER_OF_SHOW_PROJECTS] = 5
    selAllProtocols = st.checkbox(
        "Show all protocols", key="show_all_protocols", value=False
    )
    btnResetProtocolNumber = st.button("Reset protocol view")
    if btnResetProtocolNumber:
        sts[NUMBER_OF_SHOW_PROJECTS] = 10
    btnShowMoreProtocols = st.button("Show more protocols")
    if btnShowMoreProtocols:
        sts[NUMBER_OF_SHOW_PROJECTS] = sts[NUMBER_OF_SHOW_PROJECTS] + 10

    if not selAllProtocols:
        protocols = protocols[-sts[NUMBER_OF_SHOW_PROJECTS]:]
    st.text("Showing last " + str(len(protocols)) + " protocols")
    return protocols


def btn_protocol_refresh():
    btnReloadProtocols = st.button("Refresh list", key="refresh_protocols")
    if btnReloadProtocols:
        protocol_refresh()
        st.rerun()

def btn_protocol_unselect(sidebar: bool = False):
    if sidebar:
        btn = st.sidebar.button("Unselect active protocol", key="unselect_protocol_side")
    else:
        btn = st.button("Unselect active protocol", key="unselect_protocol")
    if btn:
        del_state_if_exists(SELECTED_PROTOCOL_ID)


def protocol_refresh():
    st.session_state["protocols"] = pm_api.get_protocols()


def section_create_protocol(show_only_datasets_with_name: bool = True):
    col1, col2, = st.columns([1, 3])
    with col1:
        dataset_ids = get_dataset_ids(Service.Data_owner_1)
        dataset_ids = [did for did in dataset_ids if did != -1]
        dataset_name_mapping = {
            2010: "North Carolina Voter Registry 10k-10k-1k",
            2012: "North Carolina Voter Registry 10k-10k-2k",
            2032: "North Carolina Voter Registry 50k-50k-10"
        }
        if show_only_datasets_with_name:
            dataset_names = [
                dataset_name_mapping[
                    dataset_id] if dataset_id in dataset_name_mapping else str(dataset_id)
                for dataset_id in dataset_ids
                if dataset_id in dataset_name_mapping
            ]
        else:
            dataset_names = [str(dataset_id) for dataset_id in dataset_ids]
        if dataset_names is None or len(dataset_names) == 0:
            st.warning("No datasets available")
            st.stop()
        sel_dataset = st.selectbox("Select dataset",
                                   dataset_names, index=0)
        sel_dataset_id = dataset_ids[dataset_names.index(sel_dataset)]
        # st.text(sel_dataset_id)
        options = ["RBF", "RBF-ABF-PPCR", "ABF-PPCR", "RBF-PPCR"]
        select_protocol_type = st.segmented_control("Select protocol type", options,
                                                    selection_mode="single",
                                                    default=options[0])
        match select_protocol_type:
            case "RBF" | "RBF-ABF-PPCR" | "RBF-PPCR":
                sel_init_thr = st.slider("Initial threshold",
                                         min_value=0.6,
                                         max_value=1.0,
                                         step=0.05, value=0.8)
        btnCreateProtocol = st.button("Create protocol", key="create_protocol")
        if btnCreateProtocol:
            match select_protocol_type:
                case "RBF-ABF-PPCR":
                    protocol = pm_api.create_example_3_layer_protocol(
                        do_dataset_id=sel_dataset_id,
                        lu_dataset_id=sel_dataset_id + 200,
                        initial_threshold=sel_init_thr,
                        ppcr_budget=100,
                        ppcr_batch_size_config=[5, 20]
                    )
                case "ABF-PPCR":
                    protocol = pm_api.create_example_abf_ppcr_protocol(
                        do_dataset_id=sel_dataset_id,
                        lu_dataset_id=sel_dataset_id + 100,
                    )
                case "RBF-PPCR":
                    protocol = pm_api.create_example_rbf_ppcr_layer_protocol(
                        do_dataset_id=sel_dataset_id,
                        lu_dataset_id=sel_dataset_id + 200,
                        ppcr_batch_size_config=[10]
                    )
            # st.success("Created new protocol with id " + protocol.protocol_id)
            st.success("Created new protocol")
            del_state_if_exists("auto_continue_protocol")
            del_state_if_exists("stop_auto_continue")
            del_state_if_exists("evaluation_mode")
            get_dataset_analysis_result.clear()
            get_merged_record_pair_df.clear()
            lu_api.get_record_pairs.clear()
            sts[SELECTED_PROTOCOL_ID] = protocol.protocol_id
            protocol_refresh()
    with col2:
        sel_get_dataset_description = st.toggle("Show dataset description")
        if sel_get_dataset_description:
            sts["selected_service"] = Service.Data_owner_1
            render_data_owner_dataset_description(dataset_id=sel_dataset_id)


def btn_select_most_recent_protocol_selector(index: int = 0):
    protocol_refresh()
    btnSelectNewestProtocol = st.sidebar.button("Select last protocol",
                                                key="select_most_recent_protocol")
    if btnSelectNewestProtocol:
        protocols = st.session_state["protocols"]
        state_key = get_indexed_state_key(SELECTED_PROTOCOL_ID, index)
        if len(protocols) > 0:
            set_active_protocol(protocols[-1].protocol_id, state_key)


def btn_protocol_selector(protocol_id: str, index: int = 0):
    state_key = get_indexed_state_key(SELECTED_PROTOCOL_ID, index)
    btn = btn_protocol_id_colored(
        protocol_id, state_key, get_indexed_state_key("pr", index) + protocol_id
    )
    if btn:
        clean_labeling_states()
        set_active_protocol(protocol_id, state_key)


def set_active_protocol(protocol_id, state_key):
    st.session_state[state_key] = protocol_id
    st.rerun()


def get_indexed_state_key(state_key: str, index: int = 0) -> str:
    if index > 0:
        return state_key + str(index)
    else:
        return state_key


def btn_protocol_id_colored(
        protocol_id: str, state_key: str = SELECTED_PROTOCOL_ID, key: str = None
):
    if state_key in st.session_state:
        if st.session_state[state_key] == protocol_id:
            protocol_id = ":red[" + protocol_id + "]"
    if key is not None:
        return st.button(protocol_id, key=key)
    return st.button(protocol_id)


def render_dump_record_pairs(df_record_pairs: pd.DataFrame):
    btn_dump_msal_data = st.button(
        "Dump record pairs to file", key="dump_record_pairs" + sts[SELECTED_PROTOCOL_ID]
    )
    if btn_dump_msal_data:
        df_record_pairs.to_csv("recordpairs.csv")


def get_layer_color(name: str):
    if name == "RBF":
        return "blue"
    elif name == "ABF":
        return "orange"
    elif "CR" in name:
        return "green"
    else:
        return "gray"


def render_report_groups(report_groups: list[ReportGroup]):
    global col1, col2
    if report_groups is not None:
        for report_group in report_groups:
            reports = report_group.reports
            for report in reports.values():
                is_expanded = report.name in ["Overview", "Improved links history"]
                with st.expander(report.name, expanded=is_expanded):
                    show_report = True
                    if ">>>" in report.name:
                        show_report = False
                        btn = st.button("Show", key="show_report" + report.name)
                        if btn:
                            show_report = True
                    if show_report:
                        if report.type == "TEXT":
                            st.text(report.report)
                        elif report.type == "TABLE":
                            df_report = parse_serialized_table_to_dataframe(
                                report.table
                            )
                            col1, col2 = st.columns(2)
                            with col1:
                                st.dataframe(df_report, use_container_width=True)
                            with col2:
                                st.text("Additional information")




def rename_attributes(attribute_name_replacements: dict[str, str],
                      records: list[lu.RecordDto] = [],
                      pairs: list[lu.RecordPairDto] = []):
    for old, new in attribute_name_replacements.items():
        for record in records:
            if old in record.attributes:
                record.attributes[new] = record.attributes.pop(old)
        for pair in pairs:
            if pair.attribute_similarities is not None and old in pair.attribute_similarities:
                pair.attribute_similarities[new] = pair.attribute_similarities.pop(old)


def get_protocol_step_graph(protocol: MultiLayerProtocol):
    elements = {
        "nodes": [
            {"data": {"id": 1, "label": "DO", "name": "Data Owner"}},
            {"data": {"id": 2, "label": "RBF", "name": "RBF"}},
            {"data": {"id": 3, "label": "ABF", "name": "ABF"}},
            {"data": {"id": 4, "label": "PPCR", "name": "PPCR"}},
        ],
        "edges": [
            {"data": {"id": 6, "label": "REPORT LABELS",
                      "description": "report pair labels", "source": 3, "target": 2}},
            {"data": {"id": 7, "label": "PROVIDE REENCODED RECORDS", "source": 1,
                      "target": 3}},
            {"data": {"id": 9, "label": "Fetch ids of uncertain pairs", "source": 2,
                      "target": 1}},
            {"data": {"id": 10, "label": "RECLASSIFY",
                      "description": "Reclassify pairs", "source": 2, "target": 2}},
            {"data": {"id": 11, "label": "RECLASSIFY",
                      "description": "Reclassify pairs", "source": 3, "target": 3}},
            {"data": {"id": 12, "label": "UPDATE_MODEL",
                      "description": "Update classification model", "source": 2,
                      "target": 2}},
            {"data": {"id": 13, "label": "UPDATE_MODEL",
                      "description": "Update classification model", "source": 3,
                      "target": 3}},
        ],
    }

    # Style node & edge groups
    node_styles = [
        NodeStyle("DO", "#2A629A", "name", "place"),
        NodeStyle("RBF", "#FF7F3E", "name", "storage"),
        NodeStyle("ABF", "#FF7F3E", "name", "key"),
        NodeStyle("PPCR", "#2A629A", "name", "person"),
    ]
    style = st.sidebar.selectbox("Curve style",
                                 ["haystack", "straight", "straight-triangle", "bezier",
                                  "unbundled-bezier", "segments", "round-segments",
                                  "taxi", "round-taxi"])
    edge_styles = [
        EdgeStyle("REPORT LABELS", caption='description', directed=True, labeled=None),
        EdgeStyle("PROVIDE REENCODED RECORDS", caption='label', directed=True,
                  curve_style=style, labeled=None),
        EdgeStyle("RECLASSIFY", caption='description', directed=True,
                  color='red',
                  curve_style='straight', labeled=None),
        EdgeStyle("UPDATE_MODEL", caption='description', directed=True,
                  color='blue',
                  curve_style=style, labeled=None),
    ]

    layout = {
        "name": "preset",
        "padding": 20,
        "animationDuration": 500,
        "fit": True,
        "animate": True,
        "nodeDimensionsIncludeLabels": True,
        "directed": True,
        "spacingFactor": 2.5,
        "positions": {
            "1": {
                "x": 100,
                "y": 50
            },
            "2": {
                "x": 50,
                "y": 100
            },
            "3": {
                "x": 100,
                "y": 100
            },
            "4": {
                "x": 150,
                "y": 100
            },
        }
    }

    def my_call_back() -> None:
        pass
        # val = st.session_state["protocol-graph"]
        # sts["last_graph_action"] = val
        # if val["action"] == "clicked_node":
        #     sts["selected_node"] = val["data"]["target_id"]

    events = [
        Event("clicked_node", "click tap", "node"),
        Event("another_name", "dblclick dbltap", "*"),
    ]
    # Render the component
    out = st_link_analysis(elements, layout, node_styles, edge_styles,
                           on_change=my_call_back, key="protocol-graph")
    st.json(out)
    # st.json(sts["last_graph_action"])
    # st.text(f"Selected node:{sts['selected_node']}")


def clean_labeling_states():
    del_state_if_exists("pairs")
    del_state_if_exists("records")
    del_state_if_exists("labeled_pairs")
    del_state_if_exists("manual_pair_labelings")
    del_state_if_exists("pair_labelings")
    del_state_if_exists("stop_auto_continue")
