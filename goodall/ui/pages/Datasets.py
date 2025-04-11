import streamlit as st
from streamlit import session_state as sts

from goodall.api_helper.parser import parse_serialized_table_to_dataframe
from goodall.api_helper.pprl_clients import Service, get_client
from goodall.ui.streamlit_utils import del_state_if_exists
from goodall.ui.components.datasets import *

st.set_page_config(layout="wide", page_title="Datasets")

sel_source = st.selectbox(
    "Select source",
    ["Select...", "Plain", "Encoded"],
    on_change=lambda: get_dataset_ids.clear(),
)
if sel_source == "Select...":
    del_state_if_exists("selected_service")
else:
    service = [
        Service.Data_owner_1 if sel_source == "Plain" else Service.Linkage_unit
    ].pop()
    st.session_state["selected_service"] = service

sts["record_limit"] = st.sidebar.number_input("Record limit", min_value=1, value=20)

if "selected_service" in st.session_state:
    dataset_ids = get_dataset_ids(st.session_state["selected_service"])

    st.header("Dataset descriptions")
    left_col, right_col = st.columns(2)
    with left_col:
        selected_dataset = st.selectbox("Select dataset", ["Select..."] + dataset_ids)
    with right_col:
        selected_dataset2 = st.selectbox(
            "Select dataset 2", ["Select..."] + dataset_ids
        )

    sel_analysis_type = st.selectbox(
        "Select analysis type",
        ["DATASET_DESCRIPTION", "TAG_BASED_DATASET_ANALYSIS"],
        on_change=lambda: get_dataset_ids.clear(),
    )

    if selected_dataset is not None and selected_dataset != "Select...":
        if selected_dataset2 is not None and selected_dataset2 != "Select...":
            left_col, right_col = st.columns(2)
            with left_col:
                render_data_owner_dataset_description(selected_dataset, analysis_type=sel_analysis_type)
            with right_col:
                render_data_owner_dataset_description(selected_dataset2, index=1, analysis_type=sel_analysis_type)
        else:
            render_data_owner_dataset_description(selected_dataset, analysis_type=sel_analysis_type)
