from goodall.api_helper.pprl_clients import Service
from goodall.ui.components.datasets import (
    get_dataset_ids,
    delete_dataset,
    render_data_owner_dataset_description, get_dataset_dto,
)
from goodall.ui.streamlit_utils import (
    st,
    sts,
)

sel_source = st.segmented_control(
    "Select source",
    ["Plain", "Encoded"],
    on_change=lambda: get_dataset_ids.clear(),
)
if not sel_source:
    st.stop()

service = [
    Service.Data_owner_1 if sel_source == "Plain" else Service.Linkage_unit
].pop()
sts["selected_service"] = service

sts["record_limit"] = st.sidebar.number_input("Record limit", min_value=1, value=20)
sts["include_additional_results"] = st.sidebar.toggle("Include additional results", value=False)

if "selected_service" in sts:
    selected_service = sts["selected_service"]
    dataset_ids = get_dataset_ids(selected_service)

    st.header("Dataset descriptions")
    left_col, right_col = st.columns(2)
    with left_col:
        selected_dataset = st.selectbox("Select dataset", ["Select..."] + dataset_ids)
        if selected_dataset is not None and selected_dataset != "Select...":
            st.json(get_dataset_dto(sts["selected_service"], selected_dataset)
                    .model_dump_json())

    with right_col:
        selected_dataset2 = st.selectbox(
            "Select dataset 2", ["Select..."] + dataset_ids
        )
        if selected_dataset2 is not None and selected_dataset2 != "Select...":
            st.json(get_dataset_dto(sts["selected_service"], selected_dataset2)
                    .model_dump_json())

    sel_analysis_type = st.selectbox(
        "Select analysis type",
        ["DATASET_DESCRIPTION", "TAG_BASED_DATASET_ANALYSIS"],
        on_change=lambda: get_dataset_ids.clear(),
    )

    if selected_dataset is not None and selected_dataset != "Select...":
        if st.button("Delete"):
            delete_dataset(selected_service, selected_dataset)
        if selected_dataset2 is not None and selected_dataset2 != "Select...":
            left_col, right_col = st.columns(2)
            with left_col:
                render_data_owner_dataset_description(
                    selected_dataset, analysis_type=sel_analysis_type
                )
            with right_col:
                render_data_owner_dataset_description(
                    selected_dataset2, index=1, analysis_type=sel_analysis_type
                )
        else:
            render_data_owner_dataset_description(
                selected_dataset, analysis_type=sel_analysis_type
            )
