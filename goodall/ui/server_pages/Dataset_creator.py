import streamlit
from pprl_data_generator_service_api_client import UsvrSelectionConfig
from pprl_data_owner_service_api_client import (
    DatasetCorruptionRequestDto,
    DatasetGenerationConfigCreatorDto,
)
from pprl_protocol_manager_service_api_client import (
    DatasetGeneratorDto,
    GermanyGeneratorConfig,
)

from goodall.api_helper import do_api, dg_api, pm_api
from goodall.api_helper.pprl_clients import Service
from goodall.ui.components.datasets import get_dataset_ids
from goodall.ui.streamlit_utils import st,  \
    st_cache_wrapper


def render_corrupter():
    get_dataset_ids.clear()
    dataset_ids = get_dataset_ids(Service.Data_owner_1)
    selected_dataset = st.selectbox("Select dataset", ["Select..."] + dataset_ids)
    if selected_dataset is not None and selected_dataset != "Select...":
        output_dataset = st.text_input("Output dataset id", selected_dataset + 1000)

        methods = do_api.corrupter_controller.get_dataset_generation_methods()
        selected_method = st.selectbox("Select method", methods)
        if st.button("Get generation config"):
            config = do_api.corrupter_controller.get_dataset_generation_config(
                DatasetGenerationConfigCreatorDto(
                    referenceDatasetId=selected_dataset, name=selected_method
                )
            )
            st.json(config.to_json())
        btnCreateDataset = st.button("Corrupt")
        if btnCreateDataset:
            do_api.corrupter_controller.corrupt_dataset(
                dataset_corruption_request_dto=DatasetCorruptionRequestDto(
                    inputDatasetId=selected_dataset,
                    outputDatasetId=int(output_dataset),
                    configCreator=DatasetGenerationConfigCreatorDto(
                        name=selected_method
                    ),
                )
            )


def render_german_generator():
    output_dataset = st.text_input("Output dataset id", 5000)
    number_of_records = st.text_input("Number of records", 1000)
    seed = st.text_input("Randomness seed", "abcd")
    include_households = st.checkbox("Include households?", True)

    if st.button("Generate"):
        gen_return_id = pm_api.do_preparation_controller.add_generated_dataset(
            DatasetGeneratorDto(
                datasetId=int(output_dataset),
                germanyGeneratorConfig=GermanyGeneratorConfig(
                    numberOfRecords=int(number_of_records),
                    includeHouseholdStructures=include_households,
                    seed=seed
                ),
            )
        )
        streamlit.success(f"Generated dataset id: {gen_return_id}")

def render_selector():
    cluster_type = st.selectbox("Select cluster type", ["nc", "ohio"])

    selected_action = st.selectbox("Select action", ["Get clusters", "Generate"])
    if selected_action == "Get clusters":
        number_of_clusters = st.text_input("Number of clusters", 1000)
        if st.button("Execute"):
            clusters = st_cache_wrapper(dg_api.get_clusters,
                cluster_type, int(number_of_clusters))
            st.json(clusters[0])
    elif selected_action == "Generate":
        output_dataset = st.text_input("Output dataset id")
        number_of_records = st.text_input("Number of records", 1000)
        overlap = st.slider("Overlap", min_value=0, max_value=1, step=0.05)
        if st.button("Generate"):
            gen_return_id = pm_api.do_preparation_controller.add_generated_dataset(
                DatasetGeneratorDto(
                    datasetId=int(output_dataset) if output_dataset else None,
                    usvrSelectionConfig=UsvrSelectionConfig(
                        clusterType=cluster_type,
                        numRecordsA=int(number_of_records),
                        numRecordsB=int(number_of_records),
                        numDuplicates=int(number_of_records * overlap)
                    ),
                )
            )
            streamlit.success(f"Generated dataset id: {gen_return_id}")


creation_methods = ["Germany Generator", "Corrupter", "Selector"]
selected_method = st.selectbox("Select method", creation_methods)
if selected_method is not None and selected_method != "Select...":
    if selected_method == "Selector":
        render_selector()
    elif selected_method == "Germany Generator":
        render_german_generator()
    elif selected_method == "Corrupter":
        render_corrupter()
