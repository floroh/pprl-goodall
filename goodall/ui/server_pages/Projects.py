from pprl_linkage_unit_service_api_client import BatchMatchProjectDto

from goodall.api_helper import lu_api
from goodall.api_helper.lu_api import delete_project
from goodall.api_helper.parser import get_project_quality_results, parse_record_pair_df, \
    get_best_result_and_threshold_from_quality_overview
from goodall.modifier.record_pair_filter import filter_pairs
from goodall.plotting.quality_history_plotter import QualityHistoryPlotter
from goodall.result_analysis.pair_evaluation import (
    find_threshold_used,
    combine_FP,
    combine_MatchGrade,
)
from goodall.ui.components.api import lu_api_streamlit
from goodall.ui.components.plotting import add_plot_size_sidebar
from goodall.ui.components.projects import (
    prepareProjectsForDisplay,
    project_selector,
    render_matching_method,
    project_refresh,
    render_phase,
    render_classifier_result_iterations,
    render_dump_record_pairs,
    render_plot_similarity_by_matchgrade,
    render_plot_similarity_by_link_type,
    render_plot_similarity_by_ground_truth_label,
    render_plot_similarity_by_probability,
    render_plot_similarity_vs_probability,
    render_plot_real_probabilities,
)
from goodall.ui.constants import (
    SELECTED_PROJECT_ID,
    SELECTED_METHOD,
    SELECTED_METHOD_DISPLAY,
    COMBINE_FP,
    COMBINE_MATCHGRADES,
    FETCH_RECORD_PAIRS,
    MSAL_HISTORY_DATA,
)
from goodall.ui.streamlit_utils import (
    st,
    sts,
    del_state_if_exists,
    state_exists_and_equals,
)
from goodall.utils.utils import range_include_right, downsampling_if_possible
import pandas as pd


if "projects" not in sts:
    sts["projects"] = lu_api.get_projects()
projects: list[BatchMatchProjectDto] = sts["projects"]

st.header("Linkage projects (" + str(len(projects)) + ")")
prj_list = [project.project_id for project in projects]
prj_list.insert(0, "All projects")
prj_filter = st.selectbox("Select project", prj_list)
if prj_filter != "All projects":
    index_of_selected_project = prj_list.index(prj_filter)
    list_with_adjacent_projects = prj_list[
        max(0, index_of_selected_project - 3) : min(
            len(prj_list), index_of_selected_project + 3
        )
    ]
    projects = [
        project
        for project in projects
        if project.project_id in list_with_adjacent_projects
    ]
projects = prepareProjectsForDisplay(projects)

add_plot_size_sidebar()
show_best_thr = st.sidebar.toggle("Show best thr result in overview")
for project in projects:
    col1, col2, col3, col4, col5 = st.columns([1, 2, 1, 3, 1])
    with col1:
        project_selector(project.project_id)
        st.text(project.last_update)
    with col2:
        btn = st.button(project.method, key=project.project_id + "#" + project.method)
        if btn:
            del_state_if_exists(SELECTED_PROJECT_ID)
            sts[SELECTED_METHOD] = project.method
            sts[SELECTED_METHOD_DISPLAY] = "Config"
        btnClassifier = st.button(
            "Classifier", key=project.project_id + "#" + project.method + "#Classifier"
        )
        if btnClassifier:
            del_state_if_exists(SELECTED_PROJECT_ID)
            sts[SELECTED_METHOD] = project.method
            sts[SELECTED_METHOD_DISPLAY] = "Classifier"
    with col3:
        st.write("datasetId: " + str(project.dataset_id))
        st.write("currentState: " + str(project.current_state))
    with col4:
        quality_result = get_project_quality_results(project)
        if quality_result is not None:
            st.dataframe(quality_result, hide_index=True)
        if show_best_thr:
            quality_result = get_project_quality_results(project, report_name="Overview")
            df_best, thr = get_best_result_and_threshold_from_quality_overview(quality_result)
            if df_best is not None:
                st.text(f"Best result for threshold {thr}")
                st.dataframe(df_best, hide_index=True)
    with col5:
        btn_delete = st.button("Delete", key="del" + project.project_id)
        if btn_delete:
            delete_project(project.project_id)
            sts["projects"] = lu_api.get_projects()
            st.rerun()
        if "PROJECT_ID_TO_REPORT_TO" in project.configs:
            btn_delete_with_parents = st.button(
                "Delete (+parents)", key="delWithParents" + project.project_id
            )
            if btn_delete_with_parents:
                delete_project(project.project_id, delete_parents=True)
                sts["projects"] = lu_api.get_projects()
                st.rerun()

project_refresh()

if SELECTED_METHOD in sts:
    render_matching_method(sts[SELECTED_METHOD])

if SELECTED_PROJECT_ID in sts:
    prj = lu_api.get_project(sts[SELECTED_PROJECT_ID])
    # if 'error' in prj.to_dict() and prj['error'] is not None:
    if prj is None or "error" in prj.to_dict():
        if prj is None:
            st.error("Could not fetch project with id " + sts[SELECTED_PROJECT_ID])
        else:
            st.error(prj.to_dict())
        st.stop()
    st.json(prj.to_json(), expanded=False)

    if prj.phases is not None:
        st.header("Reports for " + sts[SELECTED_PROJECT_ID])
        render_phase(prj.phases, "BLOCKING")
        render_phase(prj.phases, "CLASSIFICATION")

    btn_show_classifier_description = st.button(label="Show classifier description")
    if btn_show_classifier_description:
        st.header("Classifier for method " + prj.method)
        classifier_description = lu_api.get_classifier_description(prj.method)
        st.text(classifier_description)
    # btn_show_thr_history = st.button(label='Show threshold history')
    # if btn_show_thr_history:
    classifier_config = lu_api.get_config(prj.method).config
    render_classifier_result_iterations(classifier_config)

    tab0, tab1 = st.tabs(["MSAL", "Pairs"])
    with tab0:
        btn_read_msal_data = st.button("Read data from file", key="read_msal_data")
        if btn_read_msal_data:
            sts[MSAL_HISTORY_DATA] = pd.read_csv("quality_history.csv")
        btn_clear_msal_data = st.button("Clear data", key="clear_msal_data")
        if btn_clear_msal_data:
            del_state_if_exists(MSAL_HISTORY_DATA)
        if MSAL_HISTORY_DATA in sts:
            plotter = QualityHistoryPlotter()
            plotter.plot_quality_comparison(sts[MSAL_HISTORY_DATA])

    with tab1:
        st.header("Record pairs")
        df_record_pairs = None
        selAllPairs = st.checkbox("All pairs")
        btnGetPairs = st.button(
            "Get record pairs", key=FETCH_RECORD_PAIRS + sts[SELECTED_PROJECT_ID]
        )
        if btnGetPairs:
            sts[FETCH_RECORD_PAIRS] = True

        if FETCH_RECORD_PAIRS in sts:
            with st.spinner("Fetching record pairs..."):
                properties = []
                if selAllPairs:
                    properties = ["ALL"]
                df_record_pairs = lu_api_streamlit.get_record_pairs_as_dataframe_cached(
                    sts[SELECTED_PROJECT_ID], properties
                )

        if df_record_pairs is not None:
            st.text("Number of pairs: " + str(len(df_record_pairs)))
            parse_record_pair_df(df_record_pairs)
            threshold_used = find_threshold_used(
                df_record_pairs
            )  # Determine from config or from types
            render_dump_record_pairs(df_record_pairs)

            sts[COMBINE_FP] = st.sidebar.selectbox("Combine FPs/Fpd", [True, False])
            if state_exists_and_equals(COMBINE_FP, True):
                df_record_pairs = combine_FP(df_record_pairs)
            sts[COMBINE_MATCHGRADES] = st.sidebar.selectbox(
                "Combine MatchGrades", [True, False], index=1
            )
            if state_exists_and_equals(COMBINE_MATCHGRADES, True):
                df_record_pairs = combine_MatchGrade(df_record_pairs)

            sts["barmode"] = st.sidebar.selectbox("Barmode", ["stack", "group"])

            propertyList = [
                "active",
                "replaced",
                "REPORTED_LINK",
                "IMPROVED_LINK",
                "UNREPORTABLE_LINK",
            ]
            keep_by_properties = st.multiselect("Select by property", propertyList)
            remove_by_properties = st.multiselect("Remove by property", propertyList)
            df_record_pairs = filter_pairs(
                df_record_pairs, keep_by_properties, remove_by_properties
            )
            st.text("Number of pairs: " + str(len(df_record_pairs)))
            st.dataframe(df_record_pairs)

            with st.expander("Similarity by match grade", expanded=False):
                render_plot_similarity_by_matchgrade(df_record_pairs)
            # with st.expander('Similarity by active', expanded=False):
            #     render_plot_similarity_by_active(df_record_pairs)
            with st.expander(
                "Similarity by evaluated link classification", expanded=True
            ):
                render_plot_similarity_by_link_type(df_record_pairs)
            with st.expander("Similarity by ground truth label", expanded=False):
                render_plot_similarity_by_ground_truth_label(df_record_pairs)
            with st.expander(
                "Probability by evaluated link classification", expanded=False
            ):
                render_plot_similarity_by_probability(df_record_pairs, threshold_used)
            with st.expander("Similarity vs probability", expanded=False):
                render_plot_similarity_vs_probability(
                    downsampling_if_possible(df_record_pairs, 100_000)
                )
            with st.expander("Similarity vs real-probability", expanded=False):
                thresholds = range_include_right(0.7, 0.85, 0.05)
                if threshold_used not in thresholds:
                    thresholds.insert(0, threshold_used)
                render_plot_real_probabilities(df_record_pairs, thresholds)
            st.text("Debug stop")
