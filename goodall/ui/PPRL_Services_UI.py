import streamlit as st


service_overview_page = st.Page(
    "server_pages/Services.py", title="Services Overview", icon=":material/dashboard:"
)
mlflow_page = st.Page(
    "server_pages/MlFlow.py", title="Result analysis", icon=":material/monitor_heart:"
)
datasets_page = st.Page(
    "server_pages/Datasets.py", title="Datasets", icon=":material/dataset:"
)
dataset_creator_page = st.Page(
    "server_pages/Dataset_creator.py", title="Dataset creator", icon=":material/dataset:"
)
configurations_page = st.Page(
    "server_pages/Configurations.py", title="Configurations", icon=":material/settings:"
)
projects_page = st.Page(
    "server_pages/Projects.py", title="Projects", icon=":material/list:"
)
# projects_comparison_page = st.Page(
#     "server_pages/Projects_Comparison.py",
#     title="Project comparison",
#     icon=":material/sync_alt:",
# )
protocol_creator_page = st.Page(
    "server_pages/Protocol_creator.py",
    title="Protocol creator",
    icon=":material/create:",
)
protocols_page = st.Page(
    "server_pages/Protocols.py", title="Protocols", icon=":material/list:"
)
analysis_page = st.Page(
    "server_pages/Analysis.py", title="Analysis", icon=":material/analytics:"
)
mlal_demo_page = st.Page(
    "server_pages/Multi-layer_protocol_demo.py",
    title="Multi-layer active learning",
    icon=":material/refresh:",
)

pg = st.navigation(
    {
        "Infrastructure": [service_overview_page],
        "Mlflow experiments": [mlflow_page],
        "Setup": [datasets_page, dataset_creator_page, configurations_page],
        "Projects": [projects_page],
        "Protocols": [protocols_page, protocol_creator_page, analysis_page],
        "Demos": [mlal_demo_page],
    }
)
st.set_page_config(
    layout="wide",
    page_title="Goodall - PPRL evaluation framework",
    page_icon=":material/data_object:",
)
pg.run()
