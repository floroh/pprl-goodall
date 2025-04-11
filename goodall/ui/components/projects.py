import json

import streamlit as st
from plotly.graph_objs import Figure
from streamlit import session_state as sts
from plotly import express as px
from pprl_linkage_unit_service_api_client import (
    BatchMatchProjectPhase,
    ReportGroup,
    BatchMatchProjectDto,
)

from goodall.api_helper import lu_api
from goodall.api_helper.parser import (
    parse_serialized_table_to_dataframe,
    parse_serialized_table_dict_to_dataframe,
    remove_weighted_columns,
)
from goodall.plotting.link_improvement import plot_quality_history
from goodall.result_analysis.pair_evaluation import *
from goodall.ui.PPRL_Services_UI import *
from goodall.ui.components.plotting import add_plotly_chart_with_download_button
from goodall.ui.streamlit_utils import del_state_if_exists, get_state_or_default
from goodall.utils import downsampling_if_possible


def prepareProjectsForDisplay(projects: list[BatchMatchProjectDto]):
    if NUMBER_OF_SHOW_PROJECTS not in sts:
        sts[NUMBER_OF_SHOW_PROJECTS] = 10
    selAllProjects = st.checkbox(
        "Show all projects", key="show_all_projects", value=False
    )
    btnResetProjectNumber = st.button("Reset project view")
    if btnResetProjectNumber:
        sts[NUMBER_OF_SHOW_PROJECTS] = 10
    btnShowMoreProjects = st.button("Show more projects")
    if btnShowMoreProjects:
        sts[NUMBER_OF_SHOW_PROJECTS] = sts[NUMBER_OF_SHOW_PROJECTS] + 10

    if not selAllProjects:
        projects = projects[-sts[NUMBER_OF_SHOW_PROJECTS]:]
    st.text("Showing last " + str(len(projects)) + " projects")
    return projects


def project_refresh():
    btnReloadProjects = st.button("Refresh", key="refresh_projects")
    if btnReloadProjects:
        st.session_state["projects"] = lu_api.get_projects()
        del_state_if_exists(FETCH_RECORD_PAIRS)
        st.rerun()


def project_selector(project_id: str, index: int = 0):
    state_key = SELECTED_PROJECT_ID
    if index > 0:
        state_key = get_indexed_state_key(SELECTED_PROJECT_ID, index)
    btn = project_id_colored_button(
        project_id, state_key, get_indexed_state_key("prj", index) + project_id
    )
    if btn:
        st.session_state[state_key] = project_id
        del_state_if_exists(FETCH_RECORD_PAIRS)
        del_state_if_exists(SELECTED_METHOD)
        st.rerun()


def get_indexed_state_key(state_key, index):
    return state_key + str(index)


def project_id_colored_button(
        project_id: str, state_key: str = SELECTED_PROJECT_ID, key: str = None
):
    if state_key in st.session_state:
        if st.session_state[state_key] == project_id:
            project_id = ":red[" + project_id + "]"
    if key is not None:
        return st.button(project_id, key=key)
    return st.button(project_id)


def render_dump_record_pairs(df_record_pairs: pd.DataFrame):
    btn_dump_msal_data = st.button(
        "Dump record pairs to file", key="dump_record_pairs" + sts[SELECTED_PROJECT_ID]
    )
    if btn_dump_msal_data:
        df_record_pairs.to_csv("recordpairs.csv")


def render_plot_similarity_by_matchgrade(df_record_pairs: pd.DataFrame):
    render_plot_histogram(
        df_record_pairs,
        x_col="similarity",
        color="matchGrade",
        color_map=matchGradeColorMap,
    )
    st.dataframe(df_record_pairs.groupby(["matchGrade"]).size())


def render_plot_similarity_by_active(df_record_pairs: pd.DataFrame):
    render_plot_histogram(
        df_record_pairs, x_col="similarity", color="active", color_map=linkTypeColorMap
    )
    st.dataframe(df_record_pairs.groupby(["active"]).size())


def render_plot_similarity_by_link_type(df_record_pairs: pd.DataFrame):
    render_plot_histogram(
        df_record_pairs, x_col="similarity", color="type", color_map=linkTypeColorMap
    )
    st.dataframe(df_record_pairs.groupby(["type"]).size())


def render_plot_similarity_by_ground_truth_label(df_record_pairs: pd.DataFrame):
    render_plot_histogram(
        df_record_pairs, x_col="similarity", color="gtLabel", color_map=gtLabelColorMap
    )
    st.dataframe(df_record_pairs.groupby(["gtLabel"]).size())


def render_plot_histogram(
        df_record_pairs: pd.DataFrame,
        x_col: str,
        color: str,
        color_map: dict[str, str] = None,
        x_min: float = 0.5,
        render: bool = True,
) -> Figure:
    hist = px.histogram(
        df_record_pairs,
        x=x_col,
        color=color,
        barmode=sts["barmode"],
        nbins=50,
        color_discrete_map=color_map,
        range_x=[x_min, 1],
        height=300,  # Compact height
        # width=600  # Compact width
    )
    hist.update_traces(
        xbins=dict(  # bins used for histogram
            start=x_min, end=1.0, size=0.01
        )
    )
    # add_plotly_chart_with_download_button(hist)
    if render:
        st.plotly_chart(hist, use_container_width=True)
    return hist


def render_plot_similarity_vs_probability(df_record_pairs: pd.DataFrame):
    st.plotly_chart(
        px.scatter(
            df_record_pairs,
            x="similarity",
            y="probability",
            color="type",
            color_discrete_map=linkTypeColorMap,
            range_x=[0.5, 1],
        ),
        use_container_width=True,
    )


def render_plot_real_probabilities(df_record_pairs: pd.DataFrame, thresholds: list):
    df_real_probabilities = get_real_probabilities_by_thresholds(
        df_record_pairs, thresholds
    )
    st.plotly_chart(
        px.line(
            df_real_probabilities,
            x="similarity-upper-bound",
            y="real-probability",
            color="threshold",
            range_x=[0.5, 1],
        ),
        use_container_width=True,
    )


def render_plot_similarity_by_probability(
        df_record_pairs: pd.DataFrame, threshold_used: float = 0.6
):
    probability_method = st.sidebar.selectbox(
        "Probability method", ["default", "linear", "real-spline"]
    )
    left_distance = 0.05
    right_distance = 0.2
    if probability_method == "linear":
        left_distance = st.slider("left distance", 0.01, 0.2, left_distance)
        right_distance = st.slider("right distance", 0.05, 0.4, right_distance)
    current_df = df_record_pairs.copy()
    current_df["probability"] = get_probability(
        current_df, probability_method, threshold_used, left_distance, right_distance
    )
    current_df.sort_values(
        by=["type"], key=lambda x: x.map(linkTypeOrder), inplace=True
    )
    type_stats = get_type_stats_by_probability(current_df)
    left_col_top, right_col_top = st.columns(2)
    with left_col_top:
        barnorm_selection = st.sidebar.selectbox("Barnorm", ["None", "percent"])
        if barnorm_selection == "None":
            barnorm_selection = None
        st.plotly_chart(
            px.histogram(
                current_df,
                x="probability",
                color="type",
                barmode=sts["barmode"],
                nbins=100,
                color_discrete_map=linkTypeColorMap,
                range_x=[0.5, 1],
                barnorm=barnorm_selection,
            ),
            use_container_width=True,
        )
    with right_col_top:
        st.plotly_chart(
            px.scatter(
                downsampling_if_possible(current_df, 10000).sort_values(
                    by=["type"], key=lambda x: x.map(linkTypeOrder)
                ),
                x="similarity",
                y="probability",
                color="type",
                color_discrete_map=linkTypeColorMap,
                range_x=[0.5, 1],
            ),
            use_container_width=True,
        )
    left_col, middle_col, right_col = st.columns(3)
    with left_col:
        st.dataframe(type_stats)
    with middle_col:
        type_columns = []
        for expected_type in list_of_expected_types:
            if expected_type in type_stats:
                type_columns.append(expected_type)
        y_columns_colors = [(linkTypeColorMap[col]) for col in type_columns]
        type_columns_all = [(col + "/all") for col in type_columns]
        st.plotly_chart(
            px.line(
                type_stats,
                x="max-probability",
                y=type_columns_all,
                color_discrete_sequence=y_columns_colors,
            )
        )
    with right_col:
        type_stats_long = type_stats.melt(
            id_vars=["max-probability"], value_vars=type_columns
        )
        st.plotly_chart(
            px.bar(
                type_stats_long,
                x="max-probability",
                y="value",
                color="type",
                color_discrete_map=linkTypeColorMap,
            )
        )


def render_matching_method(method: str):
    if sts[SELECTED_METHOD_DISPLAY] == "Classifier":
        st.header("Classifier for method " + method)
        classifier_description = lu_api.get_classifier_description(method)
        st.text(classifier_description)
    else:
        st.header("Config for method " + method)
        classifier_config = lu_api.get_config(method).config
        render_classifier_result_iterations(classifier_config)
        st.subheader("Method config")
        st.json(classifier_config)


def render_quality_comparison(quality_results: dict[str, pd.DataFrame]):
    st.header("Stored quality results")
    df_histories: pd.DataFrame = None
    for name, df in quality_results.items():
        df["type"] = name
        if df_histories is None:
            df_histories = df
        else:
            df_histories = pd.concat([df_histories, df], ignore_index=True)
    st.dataframe(df_histories)
    quality_history = plot_quality_comparison(df_histories)
    st.plotly_chart(quality_history, use_container_width=True)
    btn_dump_msal_data = st.button("Dump data to file", key="dump_msal_data")
    if btn_dump_msal_data:
        df_histories.to_csv("quality_history.csv")

    for name, df in sts[MSAL_HISTORY_DATA].items():
        st.subheader(name)
        btn_delete_data = st.button("Delete", key="delete_data" + name)
        if btn_delete_data:
            del sts[MSAL_HISTORY_DATA][name]
            st.rerun()
        quality_history = create_quality_history_plot(df)
        st.plotly_chart(quality_history, use_container_width=True)


def plot_quality_comparison(
        df_histories: pd.DataFrame,
        x_column: str = "#Improved",
        name_color: str = "type",
        name_symbol: str = None,
        dataset_category: str = "plaintextDatasetId"
):
    optimal_results = df_histories[df_histories["#Improved"] < 0]
    if dataset_category in optimal_results:
        optimal_results.drop_duplicates(subset=[dataset_category], inplace=True)
    optimal_initial_score = optimal_results[
        "F1-score"
    ].iloc[0]
    initial_score = df_histories[df_histories["#Improved"] == 0]["F1-score"].iloc[0]
    quality_history = plot_quality_history(
        df_histories,
        initial_score,
        optimal_initial_score,
        x_column=x_column,
        name_color=name_color,
        name_symbol=name_symbol,
    )

    abf_baseline = {
        "E1S": 0.899,
        "E1M": 0.9121,
        "E1L": 0.9187,
        "E2S": 0.7175,
        "E2M": 0.7743
    }
    show_dataset_names = False
    if len(optimal_results) > 1 and dataset_category in optimal_results:
        show_dataset_names = True
    for i, row in optimal_results.iterrows():
        result = optimal_results.iloc[i]
        dataset_suffix = ""
        if show_dataset_names:
            dataset_suffix = " " + result[dataset_category]
        quality_history.add_hline(
            y=result["F1-score"],
            line=dict(color="Green", width=2, dash="dash"),
            annotation_text="Baseline RBF" + dataset_suffix,
            annotation_position="top left",
            annotation_font_size=12
        )
        if dataset_category in result:
            dataset_for_abf = result[dataset_category]
            dataset_for_abf = dataset_for_abf.replace('-XOR', '')
            dataset_suffix = dataset_suffix.replace('-XOR', '')
            quality_history.add_hline(
                y=abf_baseline[dataset_for_abf],
                line=dict(color="orangered", width=2, dash="dot"),
                annotation_text="Baseline ABF" + dataset_suffix,
                annotation_position="top left",
                annotation_font_size=12
            )
        # if show_dataset_names:
        #     quality_history.add_hline(
        #         y=result["F1-score"],
        #         line=dict(color="Green", width=2, dash="dot"),
        #         annotation_text="Baseline " + result[dataset_category],
        #         annotation_position="top left",
        #         annotation_font_size=10
        #     )
        # else:
        #     quality_history.add_hline(
        #         y=result["F1-score"],
        #         line=dict(color="Green", width=2, dash="dot"),
        #     )
        optimal_initial_score = df_histories[df_histories["#Improved"] == 0]
    return quality_history


def add_imbalance_info(df_histories: pd.DataFrame):
    df_histories["TM"] = df_histories["TP"] + df_histories["FN"]
    df_histories["TNM"] = df_histories["TN"] + df_histories["FP"]
    df_histories["AM"] = df_histories["TP"] + df_histories["FP"]
    df_histories["ANM"] = df_histories["TN"] + df_histories["FN"]
    # df_histories['Total'] = df_histories['TM'] + df_histories['TNM']
    df_histories["TMR"] = df_histories["TM"] / df_histories["#Non-replaced"]
    df_histories["AMR"] = df_histories["AM"] / df_histories["#Non-replaced"]
    return df_histories


def zigzag(seq):
    results = [], []
    for i, e in enumerate(seq):
        results[i % 2].append(e)
    return results


def render_classifier_result_iterations(classifier_config: str):
    st.subheader("Quality results by iteration")
    try:
        classifier = json.loads(classifier_config)["linker"]["classifier"]
        result_tables = [
            parse_serialized_table_dict_to_dataframe(res)
            for res in classifier["qualityResultsByIteration"]
        ]
        # for result_table in result_tables:
        #     result_table.rename(columns={'Description': 'Thr'}, inplace=True)
        simple, scaled = zigzag(result_tables)
        st.json(classifier, expanded=False)
        with st.expander("Raw", expanded=False):
            leftCol, rightCol = st.columns(2)
            with leftCol:
                st.text("Scaled to frequency distribution")
                for qs in scaled:
                    st.dataframe(
                        qs.rename(
                            columns={"Description": "Thr", "Accuracy (w)": "Acc (w)"}
                        )
                    )
            with rightCol:
                st.text("Simple")
                for qs in simple:
                    st.dataframe(
                        qs.rename(
                            columns={"Description": "Thr", "Accuracy (w)": "Acc (w)"}
                        )
                    )

        measure = st.selectbox(
            "Measure",
            [
                "F1-score",
                "F1-score (w)",
                "Accuracy",
                "Accuracy (w)",
                "Error",
                "ErrorDiff",
            ],
            index=3,
        )
        leftCol, rightCol = st.columns(2)
        with leftCol:
            st.text("Scaled to frequency distribution")
            fig1 = compute_classifier_result_iteration_heatmap(scaled, measure)[0]
            st.plotly_chart(fig1)
        with rightCol:
            st.text("Simple")
            fig2 = compute_classifier_result_iteration_heatmap(simple, measure)[0]
            st.plotly_chart(fig2)
    except:
        st.info("No quality results")
        # raise
    pass


def compute_classifier_result_iteration_heatmap(iteration_results, measure: str):
    i = 0
    r = None
    previous_thr = []
    best_thr = []
    for c in iteration_results:
        c.insert(0, "Iteration", i)
        # c['Acc'] = (c['TP'] + c['TN']) / (c['TP'] + c['TN'] + c['FP'] + c['FN'])
        c["Error"] = c["FP"] + c["FN"]
        c["Error"] = 1 - c["Error"] / c["Error"].max()
        c["ErrorDiff"] = c["FP"] - c["FN"]
        c["ErrorDiff"] = c["ErrorDiff"].abs()
        c["ErrorDiff"] = 1 - c["ErrorDiff"] / c["ErrorDiff"].max()
        previous_thr.append(float(c.iloc[0]["Description"]))
        best_thr.append(float(c.loc[c[measure].idxmax()]["Description"]))
        if r is None:
            r = c
        else:
            r = pd.concat([r, c])
        i = i + 1
    # st.dataframe(r)
    new_df = r.pivot(index="Description", columns="Iteration")[measure]
    # print(previous_thr)
    # st.dataframe(new_df)
    fig = px.imshow(
        new_df, text_auto=True, aspect="auto", color_continuous_scale="Greys"
    )
    for idx, x in enumerate(previous_thr):
        fig.add_shape(
            type="rect",
            x0=idx - 0.5,
            y0=(x - 0.005),
            x1=idx + 0.5,
            y1=(x + 0.005),
            line=dict(color="Blue"),
        )
    for idx, x in enumerate(best_thr):
        fig.add_shape(
            type="rect",
            x0=idx - 0.5,
            y0=x - 0.005,
            x1=idx + 0.5,
            y1=x + 0.005,
            line=dict(color="Red"),
        )
    return fig, previous_thr


def render_phase(phases: dict[str, BatchMatchProjectPhase], name: str):
    if name in phases:
        phase = phases.get(name)
        st.subheader(name)
        if phase is not None:
            render_report_groups(list(phase.report_groups.values()))


def render_report_groups(report_groups: list[ReportGroup]):
    if report_groups is not None:
        for report_group in report_groups:
            reports = report_group.reports
            for report in reports.values():
                is_expanded = report.name in ["Overview", "Improved links history"]
                render_report(report, is_expanded=is_expanded)


def render_report(report, is_expanded: bool = False, double_column: bool = True, key_postfix: str = ""):
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
                df_report = remove_weighted_columns(df_report)
                if "Improved links history" in report.name:
                    df_report = add_imbalance_info(df_report)
                if double_column:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.dataframe(df_report, use_container_width=True)
                    with col2:
                        render_report_df(df_report, report)
                else:
                    is_not_rendered_as_table = render_report_df(df_report, report)
                    if is_not_rendered_as_table:
                        btn = st.checkbox("Show data", key=f"is_not_rendered_as_table{key_postfix}{report.name}")
                        if btn:
                            st.dataframe(df_report, use_container_width=True)
                    else:
                        st.dataframe(df_report, use_container_width=True)




def render_report_df(df_report, report) -> bool:
    if "Property counts" in report.name:
        df_copy = df_report.copy()
        df_copy.drop(columns=["countActive"], inplace=True)
        # df_copy['Single-Property'] = df_report['Property'].str.strip('[]').str.split(',')
        df_copy["Single-Property"] = [
            x.strip("[]").split(",")
            for x in df_copy["Property"]
        ]
        df_copy["Single-Property"] = [
            [p.strip() for p in x]
            for x in df_copy["Single-Property"]
        ]
        df_copy = df_copy.explode(
            "Single-Property"
        ).reset_index()
        # df_copy['Single-Property'] = df_copy['Single-Property'].str.strip()
        df_copy = df_copy.groupby(["Single-Property"]).sum()
        df_copy.drop(
            columns=["Property", "index"], inplace=True
        )
        st.dataframe(df_copy, use_container_width=True)
        return True
    elif "Similarity distribution" in report.name:
        fig = px.bar(df_report, x="bin", y="count")
        add_plotly_chart_with_download_button(fig)
        return True
    elif "Thresholds" in report.name:
        fig = px.line(
            df_report,
            x="threshold",
            y=["recall", "precision", "F1-score"],
        )
        st.plotly_chart(fig, use_container_width=True)
        return True
    elif "Improved links history" in report.name:
        quality_history = create_quality_history_plot(
            df_report
        )
        if get_state_or_default("mode.dev", False):
            add_plotly_chart_with_download_button(
                quality_history
            )
            inputDataName = st.text_input(
                "Name", value=str("PPCR (err=0.0)")
            )
            btnStoreData = st.button("Store data")
            if btnStoreData:
                previous_data = get_state_or_default(
                    MSAL_HISTORY_DATA, {}
                )
                previous_data[inputDataName] = df_report
                st.session_state[MSAL_HISTORY_DATA] = (
                    previous_data
                )
        else:
            st.plotly_chart(quality_history)
        return True
    return False


def create_quality_history_plot(dfReport):
    optimal_initial_score = dfReport[dfReport["#Improved"] < 0]["F1-score"].iloc[0]
    initial_score = dfReport[dfReport["#Improved"] == 0]["F1-score"].iloc[0]
    quality_history = plot_quality_history(
        dfReport, initial_score, optimal_initial_score
    )
    return quality_history
