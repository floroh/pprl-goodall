from pprl_linkage_unit_service_api_client import BatchMatchProjectDto

from goodall.api_helper.lu_api import (
    get_projects,
    get_project,
    delete_project,
)
from goodall.ui.components.api.lu_api_streamlit import get_record_pairs_cached
from goodall.api_helper.parser import get_project_quality_results
from goodall.result_analysis.pair_evaluation import combine_FP
from goodall.ui.components.projects import (
    project_refresh,
    project_selector,
    get_indexed_state_key,
    prepareProjectsForDisplay,
)
from goodall.ui.components.project_comparison import (
    get_merged_record_pair_df,
    referenceLineStyle,
    analyse_changes_by_type,
    count_type_changes,
)
from goodall.ui.constants import linkTypeColorMap, SELECTED_PROJECT_ID
from goodall.ui.streamlit_utils import (
    st,
    sts,
    del_state_if_exists,
    get_state_or_default,
)
from goodall.utils.utils import downsampling_if_possible
import plotly.express as px

if st.button("Clear All Cache"):
    st.cache_data.clear()

if "projects" not in sts:
    sts["projects"] = get_projects()

selected_project_id = None
selected_project_id2 = None

projects: list[BatchMatchProjectDto] = sts["projects"]

st.header("Linkage projects (" + str(len(projects)) + ")")
projects = prepareProjectsForDisplay(projects)
for project in projects:
    col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 2, 1, 3, 1])
    prjId = project.project_id
    with col1:
        project_selector(prjId, 0)
    with col2:
        project_selector(prjId, 1)
    with col3:
        btn = st.button(project.method, key=prjId + project.method)
        if btn:
            del_state_if_exists("selected_project_id")
    with col4:
        st.write("datasetId: " + str(project.dataset_id))
        st.write("currentState: " + str(project.current_state))
    with col5:
        quality_result = get_project_quality_results(project)
        if quality_result is not None:
            st.table(quality_result)
    with col6:
        btn_delete = st.button("Delete", key=prjId)
        if btn_delete:
            delete_project(prjId)
            sts["projects"] = get_projects()
            st.rerun()

project_refresh()

if SELECTED_PROJECT_ID in sts:
    selected_project_id = sts[SELECTED_PROJECT_ID]
    prj2_key = get_indexed_state_key(SELECTED_PROJECT_ID, 1)
    if prj2_key in sts:
        selected_project_id2 = sts[prj2_key]
        st.write(
            "Selected projects: " + selected_project_id + " and " + selected_project_id2
        )

        prj0 = get_project(selected_project_id)
        prj1 = get_project(selected_project_id2)
        # if selected_project_id == selected_project_id2:
        #     st.error('Selected the same project twice')
        #     st.stop()
        if prj0.dataset_id != prj1.dataset_id:
            st.warning("Project do not have the same dataset id")
        # record_pairs = None
        # record_pairs2 = None
        if st.button("Clear merged cache"):
            get_merged_record_pair_df.clear()
        if st.button("Clear pair cache"):
            get_record_pairs_cached.clear()

        btnSelectDefaultSide = st.selectbox("Default side", ["x", "y"], index=1)
        if btnSelectDefaultSide:
            sts["reference_side"] = btnSelectDefaultSide

        btnLeftProperties = st.selectbox(
            "Left properties",
            [
                "active",
                "ALL",
                "replaced",
                "IMPROVED_LINK",
                "REPORTED_LINK",
                "UNREPORTABLE_LINK",
            ],
            index=5,
        )
        if btnLeftProperties:
            props = [btnLeftProperties]
            if (props[0] == "replaced") | (props[0] == "UNREPORTABLE_LINK"):
                props.append("ALL")
            if "left_properties" in sts:
                if not (sts["left_properties"] == props):
                    get_record_pairs_cached.clear()
                    get_merged_record_pair_df.clear()
            sts["left_properties"] = props

        btnRightProperties = st.selectbox(
            "Right properties",
            [
                "active",
                "ALL",
                "replaced",
                "IMPROVED_LINK",
                "REPORTED_LINK",
                "UNREPORTABLE_LINK",
            ],
            index=4,
        )
        if btnRightProperties:
            props = [btnRightProperties]
            if (props[0] == "replaced") | (props[0] == "UNREPORTABLE_LINK"):
                props.append("ALL")
            if "right_properties" in sts:
                if not (sts["right_properties"] == props):
                    get_record_pairs_cached.clear()
                    get_merged_record_pair_df.clear()
            sts["right_properties"] = props

        dfM_all = None
        btnGetPairs = st.button(
            "Get record pairs", key="fetch_record_pairs" + selected_project_id
        )
        if btnGetPairs:
            sts["fetch_record_pairs"] = True

        if "fetch_record_pairs" in sts:
            dfM_all = get_merged_record_pair_df(
                selected_project_id,
                selected_project_id2,
                get_state_or_default("left_properties", None),
                get_state_or_default("right_properties", None),
            )

        if dfM_all is not None:
            combineFP = st.selectbox("Combine FPs/Fpd", [True, False])
            if combineFP:
                sts["combineFP"] = combineFP
            st.text("Merged size:" + str(dfM_all.count()[0]))
            downsampling_selection = st.selectbox(
                "Downsampling", ["No", "1000", "10000", "100000"]
            )
            if downsampling_selection is not None:
                if downsampling_selection == "No":
                    del_state_if_exists("downsampling")
                else:
                    sts["downsampling"] = int(downsampling_selection)
            print(downsampling_selection)
            if "downsampling" in sts:
                dfM = downsampling_if_possible(dfM_all, sts["downsampling"])
            else:
                dfM = dfM_all
            if ("combineFP" in sts) & (sts["combineFP"] is True):
                dfM = combine_FP(dfM)
            if st.button("Show merged dataframe"):
                st.dataframe(dfM)
            st.text("Number of common pairs in both projects: " + str(len(dfM)))
            default_type = "type_" + get_state_or_default("reference_side", "x")
            if st.button("Types"):
                count_type_changes(dfM)
            if st.button("Probabilities"):
                dfProbs = dfM.sort_values(by=["probability_x"])
                prob_scatter = px.scatter(
                    dfProbs,
                    x="probability_x",
                    y="probability_y",
                    color=default_type,
                    color_discrete_map=linkTypeColorMap,
                    range_x=[0.5, 1],
                )
                prob_scatter.add_shape(
                    type="line", x0=0.5, y0=0.5, x1=1.0, y1=1.0, line=referenceLineStyle
                )
                st.plotly_chart(prob_scatter)
                prob_diff_plot = px.scatter(
                    dfProbs,
                    x="probability_x",
                    y="probability_diff",
                    color=default_type,
                    color_discrete_map=linkTypeColorMap,
                    range_x=[0.5, 1],
                )
                prob_diff_plot.add_hline(y=0, line=referenceLineStyle)
                st.plotly_chart(prob_diff_plot)
                analyse_changes_by_type(dfM, "probability")
            if st.button("Similarities"):
                dfSims = dfM.sort_values(by=["similarity_x"])
                simScatterPlot = px.scatter(
                    dfSims,
                    x="similarity_x",
                    y="similarity_y",
                    color=default_type,
                    color_discrete_map=linkTypeColorMap,
                    range_x=[0.5, 1],
                )
                simScatterPlot.add_shape(
                    type="line", x0=0.5, y0=0.5, x1=1.0, y1=1.0, line=referenceLineStyle
                )
                st.plotly_chart(simScatterPlot)
                sim_diff_plot = px.scatter(
                    dfSims,
                    x="similarity_x",
                    y="similarity_diff",
                    color=default_type,
                    color_discrete_map=linkTypeColorMap,
                    range_x=[0.5, 1],
                )
                sim_diff_plot.add_hline(y=0, line=referenceLineStyle)
                st.plotly_chart(sim_diff_plot)
                # if st.button('Similarity changes'):
                analyse_changes_by_type(dfM, "similarity")

            columns = [
                "similarity_x",
                "probability_x",
                "similarity_y",
                "probability_y",
                "similarity_diff",
                "probability_diff",
            ]
            btnXselection = st.selectbox("X", columns)
            btnYselection = st.selectbox("Y", columns)
            if btnXselection:
                sts["plot_x_column"] = btnXselection
            if btnYselection:
                sts["plot_y_column"] = btnYselection
            x_column = get_state_or_default("plot_x_column", "similarity_x")
            y_column = get_state_or_default("plot_y_column", "probability_y")
            scatter = px.scatter(
                dfM,
                x=x_column,
                y=y_column,
                color=default_type,
                color_discrete_map=linkTypeColorMap,
            )
            if "_diff" in y_column:
                scatter.add_shape(
                    type="line", x0=0.5, y0=0, x1=1.0, y1=0, line=referenceLineStyle
                )
            else:
                scatter.add_shape(
                    type="line", x0=0.5, y0=0.5, x1=1.0, y1=1.0, line=referenceLineStyle
                )
            st.plotly_chart(scatter)
            st.text("Debug stop")
