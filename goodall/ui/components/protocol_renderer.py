import re
import time
from typing import Callable

import pandas as pd
import streamlit as st
from PIL.ImageOps import scale
from numpy.random import get_state
from pprl_linkage_unit_service_api_client import BatchMatchProjectDto
from pprl_protocol_manager_service_api_client import MultiLayerProtocol, Layer, \
    ProcessingStep
from streamlit import session_state as sts

from goodall.api_helper import pm_api, lu_api
from goodall.api_helper.lu_api import get_record_pairs_as_dataframe
from goodall.api_helper.parser import parse_serialized_table_to_dataframe, \
    get_project_quality_results
from goodall.api_helper.pprl_clients import Service
from goodall.result_analysis.pair_evaluation import combine_FP, combine_MatchGrade, \
    get_type_stats_by_probability
from goodall.ui.PPRL_Services_UI import SELECTED_PROTOCOL_ID
from goodall.ui.components.clerical_review_renderer import ClericalReviewRenderer
from goodall.ui.components.comparison_renderer import subsubheader
from goodall.ui.components.datasets import get_ppcr_privacy_analysis, \
    get_dataset_privacy_analysis, get_dataset_analysis_result, \
    process_dataset_dataframe, get_records_as_dataframe, order_columns, order_rows, \
    add_reference_results
from goodall.ui.components.plotting import render_quality_development, plot_gini, \
    plot_availability
from goodall.ui.components.project_comparison import get_merged_record_pair_df, \
    count_type_changes, compute_change_statistics, plot_type_correspondences, \
    plot_type_changes, plot_match_grade_correspondences
from goodall.ui.components.projects import render_report
from goodall.ui.components.protocol_helper import get_current_classifier_threshold
from goodall.ui.components.protocols import get_layer_color, render_report_groups, \
    clean_labeling_states
from goodall.ui.components.rbf_adaption_renderer import RecordLevelLayerAdaptionRenderer
from goodall.ui.streamlit_utils import get_state_or_default, god, \
    state_exists_and_equals, state_exists_and_is_in, del_state_if_exists


def add_vertical_spacer(height: str = "50px"):
    st.markdown(f"<div style='height: {height};'></div>",
                unsafe_allow_html=True)


class ProtocolRenderer:

    def __init__(self, protocol: MultiLayerProtocol):
        self.protocol = protocol
        self.projects = {}

    def update_protocol(self):
        # sleep(1)
        self.protocol = pm_api.update_protocol(self.protocol)

    def fetch_protocol(self):
        self.protocol = pm_api.get_protocol(sts[SELECTED_PROTOCOL_ID])

    def update_projects(self):
        for layer in self.protocol.layers:
            self.update_project(layer)

    def update_project(self, layer: Layer):
        project = lu_api.get_project(layer.project_id)
        self.projects[layer.name] = project

    def run_next_steps(self, step_count: int = 1):
        for i in range(step_count):
            self.protocol = pm_api.run_protocol_single_step(
                sts[SELECTED_PROTOCOL_ID])

    def get_project(self, layer) -> BatchMatchProjectDto:
        if layer.name not in self.projects:
            self.update_project(layer)
        return self.projects[layer.name]

    def render(self, steps_on_the_right: bool = True):
        if steps_on_the_right:
            col1, col2 = st.columns([3, 1])
            with col1:
                if get_state_or_default("manual_cr", False):
                    if self.next_is_clerical_review_step():
                        renderer = ClericalReviewRenderer(self.protocol)
                        is_completed = renderer.render_clerical_review()
                        add_vertical_spacer(height="100px")

                        if is_completed:
                            self.protocol = renderer.protocol
                            self.update_protocol()
                            self.run_next_steps()
                            st.rerun()
                # else:
                self.render_protocol_layers_full()
            with col2:
                st.subheader("")
                with st.container(border=True):
                    self.render_project_quality(self.protocol.layers[0])
                self.render_protocol_steps_vertically()
        else:
            self.render_protocol_layers_full()
            self.render_protocol_steps_horizontally()

    def render_protocol_layers_full(self):
        self.render_protocol_layers(self.render_protocol_layer_header)
        self.render_protocol_layers(self.render_protocol_layer_inspection,
                                    "Inspect data")
        self.render_protocol_layers(self.render_protocol_layer_configuration, "Configuration")
        self.render_protocol_layers(self.render_protocol_layer_privacy, "Privacy measures")
        self.render_protocol_layers(self.render_protocol_layer_quality,
                                    "Quality measures")
        self.render_protocol_layers_steps()
        # add_vertical_spacer(height="100px")
        # st.divider()
        if get_state_or_default("knowledge_mode", "Simple") == "Evaluation":
            self.render_protocol_layers(self.render_protocol_layer_description)

    def render_protocol_layers_steps(self, joined_list: bool = True):
        if joined_list:
            with st.expander("Processing steps", expanded=True):
                if self.protocol.step_queue is not None:
                    for step in list(reversed(self.protocol.step_queue)):
                        self.render_protocol_layers_step(step)
                else:
                    st.markdown(
                        "<p style='text-align: center; font-size: small;'>Nothing planned yet</p>",
                        unsafe_allow_html=True)
                st.markdown(
                    "<div style='text-align: center; font-size: small; color: gray;'>Upcoming</div>",
                    unsafe_allow_html=True)
                st.markdown(
                    """
                    <hr style="margin: 5px 0; border: none; border-top: 1px solid #ccc;" />
                    """,
                    unsafe_allow_html=True,
                )
                st.markdown(
                    "<div style='text-align: center; font-size: small; color: gray;'>Previous</div>",
                    unsafe_allow_html=True)

                if self.protocol.step_history is not None:
                    for step in list(reversed(self.protocol.step_history)):
                        self.render_protocol_layers_step(step)
        else:
            with st.container(border=True):
                st.text("Upcoming")
                if self.protocol.step_queue is not None:
                    for step in list(reversed(self.protocol.step_queue)):
                        self.render_protocol_layers_step(step)
            with st.container(height=600):
                st.text("History")
                if self.protocol.step_history is not None:
                    for step in list(reversed(self.protocol.step_history)):
                        self.render_protocol_layers_step(step)

    def render_protocol_layers_step(self, step: ProcessingStep):
        col1, col2, col3 = st.columns(3)
        with col1:
            self.render_processing_step(step, with_layer_name=False, only_layer="RBF")
        with col2:
            self.render_processing_step(step, with_layer_name=False, only_layer="ABF")
        with col3:
            self.render_processing_step(step, with_layer_name=False, only_layer="PPCR")

    def render_protocol_layers(self, layer_renderer: Callable[[Layer], None],
                               expander_title: str | None = None):
        # st.subheader("Linkage units")
        if expander_title is not None:
            with st.expander(expander_title):
                self._render_protocol_layers(layer_renderer)
        else:
            self._render_protocol_layers(layer_renderer)

    def _render_protocol_layers(self, layer_renderer):
        col1, col2, col3 = st.columns(3)
        with col1:
            layer = self.get_layer_with_name("RBF")
            if layer is not None:
                layer_renderer(layer)
        with col2:
            layer = self.get_layer_with_name("ABF")
            if layer is not None:
                layer_renderer(layer)
        with col3:
            layer = self.get_layer_with_name("PPCR")
            if layer is not None:
                layer_renderer(layer)

    def render_protocol_layer_header(self, layer: Layer):
        color = get_layer_color(layer.name)
        st.subheader(f":{color}[{self._get_display_name(layer.name)}]")

    def render_protocol_layer_inspection(self, layer: Layer):
        # with st.expander("Inspect data"):
        show_records = st.toggle("Show records", key=f"show_record{layer.name}")
        if show_records:
            df = get_records_as_dataframe(Service.Linkage_unit,
                                          self.get_project(layer).dataset_id,
                                          get_state_or_default("record_limit", 20))
            df = df.rename(columns=lambda col: col.replace("PLZ", "ZIP"))
            df = process_dataset_dataframe(df)
            # if layer.name == "RBF":
            #     df = df["RBF"]
            if df.empty:
                st.info("No records found.")
            else:
                df = df.drop(columns=["datasetId", "id.unique", "encodingId.project"])
                df = df.drop(columns=df.columns[df.columns.str.contains("_DEV")])
                st.dataframe(df, hide_index=True)
        show_pairs = st.toggle("Show pairs", key=f"show_pairs{layer.name}")
        if show_pairs:
            df = get_record_pairs_as_dataframe(self.get_project(layer).project_id,
                                               [])
            if df.empty:
                st.info("No pairs found.")
            else:
                df = df.drop(columns=["projectId", "tags"])
                st.dataframe(df, hide_index=True)

    def render_protocol_layer_privacy(self, layer: Layer):
        match layer.name:
            case "RBF":
                df_privacy = get_dataset_privacy_analysis(layer.project_id,
                                                          "AttributePrivacy",
                                                          )
                if not df_privacy.empty:
                    st.plotly_chart(plot_gini(df_privacy,
                                              y_limit = 0.4,
                                              title="Gini Index of Record-level Bloom Filter")
                                    , use_container_width=True)
                pass
            case "ABF":
                ref_dataset_id = self.protocol.plaintext_dataset_id + 100
                df_privacy = get_dataset_privacy_analysis(layer.project_id,
                                                          "AttributePrivacy",
                                                          ref_dataset_id)
                if not df_privacy.empty:
                    df_avail = get_dataset_privacy_analysis(layer.project_id,
                                                            "AttributeAvailability",
                                                            ref_dataset_id)
                    # st.plotly_chart(plot_availability(df_avail),
                    #                 use_container_width=True)
                    # st.dataframe(df_avail)
                    st.plotly_chart(plot_gini(df_privacy), use_container_width=True)
                    # st.dataframe(df_privacy)
            case "PPCR":
                prj = self.get_project(self.get_layer_with_name("ABF"))
                ref_dataset_id = prj.dataset_id
                df_avail = get_dataset_privacy_analysis(layer.project_id,
                                                        "AttributeAvailability",
                                                        ref_dataset_id=ref_dataset_id)
                if not df_avail.empty:
                    st.plotly_chart(plot_availability(df_avail),
                                    use_container_width=True)
                    # st.dataframe(df_avail)
                    # btn_run_ppcr_privacy_analysis = st.button(
                    #     "Analyse k-Anonymity privacy")
                    # if btn_run_ppcr_privacy_analysis:
                    #     df_privacy = get_ppcr_privacy_analysis(layer.project_id,
                    #                                            self.protocol.plaintext_dataset_id)
                    #     st.dataframe(df_privacy)

    def render_protocol_layer_quality(self, layer: Layer):
        match layer.name:
            case "RBF":
                subsubheader("Overall linkage quality")
                prj = self.get_project(layer)
                render_quality_development(prj)
            case "ABF":
                subsubheader("Prediction changes based on attribute-level comparison")
                count, fig = self.render_label_changes(layer)
                if count == 0:
                    return
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
                sts["ABF-count"] = count
            case "PPCR":
                subsubheader("Prediction changes based on masked clerical review")
                count, fig = self.render_label_changes(layer)
                if count == 0:
                    return
                sts["PPCR-count"] = count
                abf_count = get_state_or_default("ABF-count", count)
                scale_factor = float(count)/abf_count
                fig.update_layout(height=100)
                # fig.update_layout(height=int(600*scale_factor))
                st.plotly_chart(fig, use_container_width=True)

    def render_label_changes(self, layer):
        if layer.name == "RBF":
            left_properties = ["ALL", "replaced"]
            right_properties = ["IMPROVED_LINK"]
        else:
            left_properties = ["ALL", "UNREPORTABLE_LINK"]
            right_properties = ["REPORTED_LINK"]
        dfM = get_merged_record_pair_df(
            layer.project_id,
            layer.project_id,
            left_properties,
            right_properties,
        )
        # st.dataframe(dfM, hide_index=True)
        dfM = combine_FP(dfM)
        dfM = combine_MatchGrade(dfM)

        if dfM.empty:
            return 0, None
        if get_state_or_default("knowledge_mode", "Evaluation") == "Evaluation":
            stats = compute_change_statistics(dfM)
            # st.dataframe(stats, hide_index=True)
            fig = plot_type_correspondences(stats)
            # st.plotly_chart(fig, use_container_width=True)
        else:
            stats = compute_change_statistics(dfM, "matchGrade")
            # st.dataframe(stats, hide_index=True)
            fig = plot_match_grade_correspondences(stats)
            # fig.update_layout(height=100)
            # st.plotly_chart(fig, use_container_width=True)
        fig.update_layout(
            title=dict(text=""),  # Hide the title by setting it to an empty string
            margin=dict(t=0, b=0)
        )
        # fig.update_layout(
        #     title=dict(
        #         x=0.5,  # Center-align the title
        #         xanchor="center",
        #         y=0.9,  # Vertical alignment (optional)
        #         pad=dict(t=0, b=0),  # Top and bottom padding
        #     )
        # )
        return dfM.shape[0], fig

    def render_protocol_layer_configuration(self, layer: Layer):
        # with st.popover("Edit"):
        #     err_choices = [0.0, 0.1, 0.2]
        #     if layer.error_rate in err_choices:
        #         err_choices_index = err_choices.index(layer.error_rate)
        #         sel_err = st.selectbox("Error-Rate", err_choices,
        #                                index=err_choices_index,
        #                                key="sel_error_rate" + layer.name)
        #         layer.error_rate = sel_err
        # st.json(layer.to_json(), expanded=False)
        def get_status_text(layer: Layer) -> str:
            active_status = god(layer.active, False)
            active_symbol = "✅" if active_status else "❌"
            return f"Active: {active_symbol}"

        def get_colored_text(layer: Layer, text: str) -> str:
            active_status = god(layer.active, False)
            if not active_status:
                return f":grey[{text}]"
            return text

        # with st.container(height=200):
        if self.protocol.layers[0].name != layer.name:
            if layer.max_batches is not None and layer.max_batches > 0:
                _num_of_batches = god(layer.current_batch, 0)
                st.progress(float(_num_of_batches) / layer.max_batches,
                            text=get_colored_text(layer, f"Batch: {_num_of_batches}/{layer.max_batches}"))
            # st.markdown(get_colored_text(layer, f"Batch: {god(layer.current_batch, 0)}/{layer.max_batches}"))
            st.markdown(get_colored_text(layer, f"Batch size: {layer.batch_size}"))
            if layer.budget > 0:
                _num_of_reviews = god(layer.number_of_reviews, 0)
                st.progress(float(_num_of_reviews) / layer.budget,
                            text=get_colored_text(layer, f"Budget: {_num_of_reviews}/{layer.budget}"))
            else:
                st.markdown(get_colored_text(layer, f"Budget: {layer.number_of_reviews}"))

        match layer.name:
            case "RBF":
                self.render_threshold_status(layer)
                # st.text(get_status_text(layer))
                if get_state_or_default("manual_thr", False):
                    # st.text("manual_thr available")
                    if self.rbf_classification_update_possible():
                        # st.text("rbf classifciation possible")
                        # lu_api.get_record_pairs.clear()
                        renderer = RecordLevelLayerAdaptionRenderer(self.protocol)
                        is_adapted = renderer.render_threshold_adaption()
                        if is_adapted:
                            self.protocol = renderer.protocol
                            self.update_protocol()
                            self.run_next_steps()
                            del_state_if_exists("stop_auto_continue")
                            st.rerun()

    def render_threshold_status(self, layer, multi_line: bool = True):
        def get_optimal_threshold(protocol_renderer, layer: Layer) -> str:
            try:
                prj = protocol_renderer.get_project(layer)
                report = prj.phases["CLASSIFICATION"].report_groups[
                    "Linkage quality evaluation"].reports[
                    "Overview"]
                df_report = parse_serialized_table_to_dataframe(
                    report.table)
                return protocol_renderer._get_best_threshold_from_quality_overview(
                    df_report)
            except Exception as e:
                return "?"

        try:
            current_threshold = get_current_classifier_threshold(layer)
        except Exception as e:
            current_threshold = "?"

        if multi_line:
            st.text(f"Current threshold: {current_threshold}")
            st.text(f"Initial threshold: {layer.initial_threshold}")
            if state_exists_and_equals("knowledge_mode", "Evaluation"):
                st.text(f"Optimal threshold: {get_optimal_threshold(self, layer)}")
        else:
            thr_text = f"Threshold: {layer.initial_threshold} -> {current_threshold}"
            if state_exists_and_equals("knowledge_mode", "Evaluation"):
                thr_text = f"{thr_text} (optimal: {get_optimal_threshold(self, layer)})"
            st.text(thr_text)

    def render_protocol_layer_description(self, layer: Layer):
        match layer.name:
            case "RBF":
                # if self.protocol.layers[0].name == layer.name:
                self.render_project_layer_quality(layer)
            case "ABF":
                # if self.protocol.layers[0].name == layer.name:
                self.render_project_layer_quality(layer)
            case "PPCR":
                self.render_project_layer_quality(layer)

    def render_project_quality(self, layer: Layer):
        if get_state_or_default("knowledge_mode", "Simple") != "Evaluation":
            return
        project = self.get_project(layer)
        df_quality_results = get_project_quality_results(project)
        if df_quality_results is None or df_quality_results.empty:
            return
        options = ["Initial result", "Optimal threshold", "Attribute-level linkage"]
        if layer.name != "RBF":
            options.remove("Optimal threshold")
        quality_comparison_mode = st.segmented_control(
            "Reference result", options, default=options[0], selection_mode="single"
        )

        colF1, colR, colP = st.columns(3)
        f1 = df_quality_results.at[0, 'F1-score']
        recall = df_quality_results.at[0, 'recall']
        precision = df_quality_results.at[0, 'precision']

        delta_f1 = None
        delta_recall = None
        delta_precision = None
        match quality_comparison_mode:
            case "Initial result":
                df_reference_result = get_project_quality_results(project,
                                                                  report_name="Improved links history")
                delta_f1 = f1 - df_reference_result.at[1, "F1-score"]
                delta_recall = recall - df_reference_result.at[1, "recall"]
                delta_precision = precision - df_reference_result.at[1, "precision"]
            case "Optimal threshold":
                df_reference_result = get_project_quality_results(project,
                                                                  report_name="Improved links history")
                delta_f1 = f1 - df_reference_result.at[0, "F1-score"]
                delta_recall = recall - df_reference_result.at[0, "recall"]
                delta_precision = precision - df_reference_result.at[0, "precision"]

        def round_if_not_none(value, precision: int = 3):
            return value if value is None else round(value, precision)

        colF1.metric("F1-score", round(f1, 3), delta=round_if_not_none(delta_f1))
        colR.metric("Recall", round(recall, 3), delta=round_if_not_none(delta_recall))
        colP.metric("Precision", round(precision, 3),
                    delta=round_if_not_none(delta_precision))

    def render_project_layer_quality(self, layer: Layer):
        project_id = layer.project_id
        with st.spinner("Fetching project..."):
            prj = self.get_project(layer)
            if state_exists_and_equals("view_mode", "Expert"):
                st.json(prj.to_json(), expanded=False)
            if "CLASSIFICATION" in prj.phases:
                phase = prj.phases["CLASSIFICATION"]
                if state_exists_and_equals("knowledge_mode", "Evaluation"):
                    report = phase.report_groups["Linkage quality evaluation"].reports[
                        "Improved links history"]
                    render_report(report, is_expanded=True, double_column=False,
                                  key_postfix=project_id)
                # if state_exists_and_equals("mode.dev", False):
                if state_exists_and_equals("knowledge_mode", "Evaluation"):
                    if layer.name == "RBF":
                        report = \
                            phase.report_groups["Linkage quality evaluation"].reports[
                                "Thresholds"]
                        render_report(report, is_expanded=True, double_column=False,
                                      key_postfix=project_id)
                    report = phase.report_groups["Record pairs"].reports[
                        "Property counts"]
                    render_report(report, is_expanded=True, double_column=False,
                                  key_postfix=project_id)
                if state_exists_and_is_in("knowledge_mode", ["Enhanced", "Evaluation"]):
                    if layer.name == "RBF":
                        report = phase.report_groups["Record pairs"].reports[
                            "Similarity distribution"]
                        render_report(report, is_expanded=True, double_column=False,
                                      key_postfix=project_id)

    def _get_best_threshold_from_quality_overview(self, df: pd.DataFrame):
        for desc in df['Description']:
            if desc.startswith('Best'):
                match = re.search(r'\(([^)]+)\)', desc)
                if match:
                    try:
                        return float(match.group(1))
                    except ValueError:
                        return None
        return None

    def _get_display_name(self, name):
        match name:
            case "RBF":
                # return "$L_R$ (Record-level)"
                return "Record-level comparison"
            case "ABF":
                # return "$L_A$ (Attribute-level)"
                return "Attribute-level comparison"
            case "PPCR":
                # return "$L_C$ (Masked clerical review)"
                return "Masked clerical review"

    def next_is_clerical_review_step(self):
        if self.protocol.step_queue is not None and len(self.protocol.step_queue) > 0:
            next_step = self.protocol.step_queue[0]
            if next_step.type == "RECLASSIFY_PAIRS" and 'projectId' in next_step.properties:
                layer = self.get_layer_of_project_id(next_step.properties['projectId'])
                if layer.name == "PPCR":
                    return True
        return False

    def next_is_threshold_adaption_step(self):
        if self.protocol.step_queue is not None and len(self.protocol.step_queue) > 0:
            next_step = self.protocol.step_queue[0]
            if next_step.type == "RECLASSIFY_PAIRS" and 'projectId' in next_step.properties:
                layer = self.get_layer_of_project_id(next_step.properties['projectId'])
                if layer.name == "RBF":
                    return True
        if self.protocol.step_history is not None and len(
                self.protocol.step_history) > 0:
            previous_step = self.protocol.step_history[0]
            if previous_step.type == "RUN_INITIAL_LINKAGE" and 'projectId' in previous_step.properties:
                layer = self.get_layer_of_project_id(
                    previous_step.properties['projectId'])
                if layer.name == "RBF":
                    return True
        return False

    def rbf_classification_update_possible(self) -> bool:
        if self.protocol.step_queue is not None and len(self.protocol.step_queue) > 0:
            next_step = self.protocol.step_queue[0]
            if ((next_step.type == "UPDATE_MATCHER"
                 or next_step.type == "RECLASSIFY_PAIRS"
                 or next_step.type == "DETERMINE_UNCERTAIN_LINKS")
                    and 'projectId' in next_step.properties):
                layer = self.get_layer_of_project_id(next_step.properties['projectId'])
                if layer.name == "RBF":
                    return True
        return False

    def render_protocol_steps_vertically(self,
                                         show_steps: bool = True):
        with st.container(border=True):
            st.subheader("Protocol execution control")
            if show_steps:
                subsubheader("Next step")
                if self.protocol.step_queue is not None:
                    for step in self.protocol.step_queue:
                        self.render_processing_step(step, with_layer_name=False, )
                else:
                    st.text("Nothing yet")
                # st.subheader("History")
                # if self.protocol.step_history is not None:
                #     with st.container(height=600):
                #         for step in list(reversed(self.protocol.step_history)):
                #             self.render_processing_step(step, with_layer_name=False, )
            btn_next_step = st.button("Continue protocol", key="next_protocol_step")
            stop_auto_continue = get_state_or_default("stop_auto_continue", False)
            # if stop_auto_continue:
            #     sts["auto_continue_protocol"] = False
            auto_continue = st.toggle(
                "Autocontinue", key="auto_continue_protocol", value=False,
                disabled=stop_auto_continue
            )
            manual_cr = st.toggle("Manual clerical review", key="manual_cr", value=True)
            # sts["manual_cr"] = manual_cr
            if self.get_layer_with_name("RBF") is not None:
                manual_thr = st.toggle("Manual threshold adaption", key="manual_thr",
                                       value=True)
            else:
                manual_thr = False

        with st.container(border=True):
            st.subheader("Analysis settings")
            evaluation_mode = st.toggle("Evaluation mode", value=get_state_or_default("knowledge_mode", "Simple")=="Evaluation", key="evaluation_mode")
            if evaluation_mode:
                sts["knowledge_mode"] = "Evaluation"
            else:
                sts["knowledge_mode"] = "Simple"
            # sts["knowledge_mode"] = st.selectbox("Knowledge mode",
            #                                              ["Simple", "Evaluation"],
            #                                              # ["Simple", "Enhanced", "Evaluation"],
            #                                              index=1)
            btn_clean_analysis_cache = st.button("Refresh",
                                             key="clean_analysis_cache",
                                             # on_change=get_dataset_analysis_result.clear()
                                             )
            if btn_clean_analysis_cache:
                get_dataset_analysis_result.clear()
                get_merged_record_pair_df.clear()
                lu_api.get_record_pairs.clear()
                get_records_as_dataframe.clear()
                st.rerun()
        # sts["manual_thr"] = manual_thr
        auto_delayed_rerun = auto_continue and not stop_auto_continue
        seconds_to_wait = st.sidebar.slider("Auto run wait (s)", min_value=1,
                                            max_value=10, value=2)
        immediate_rerun = False
        if btn_next_step or auto_delayed_rerun:
            del_state_if_exists("stop_auto_continue")
            clean_labeling_states()
            with st.spinner("Running..."):
                self.run_next_steps()
            immediate_rerun = True
            sts["stop_auto_continue"] = False
            # if clean_analysis_cache:
            #     get_dataset_analysis_result.clear()
            #     get_merged_record_pair_df.clear()
            if self.protocol.step_history is not None and \
                    self.protocol.step_history[-1].type == "IDLE":
                st.info(f"Stopped due to: IDLE")
                sts["stop_auto_continue"] = True
                auto_delayed_rerun = False
            if self.next_is_clerical_review_step():
                if manual_cr:
                    sts["stop_auto_continue"] = True
                    auto_delayed_rerun = False
                    # immediate_rerun = True
            if self.next_is_threshold_adaption_step():
                if manual_thr:
                    sts["stop_auto_continue"] = True
                    auto_delayed_rerun = False
                    lu_api.get_record_pairs.clear()
                    # immediate_rerun = True
            if auto_delayed_rerun:
                wait_bar = st.progress(0, text="Starting next step...")
        if auto_delayed_rerun:
            seconds = 0
            wait_bar.progress(0)
            while seconds < seconds_to_wait:
                time.sleep(1)
                seconds += 1
                progress = float(seconds / seconds_to_wait)
                wait_bar.progress(progress, text="Starting next step...")
            st.rerun()
        if immediate_rerun:
            st.rerun()

    def render_protocol_steps_horizontally(self):
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            st.subheader("History")
            if self.protocol.step_history is not None:
                with st.container(height=600):
                    for step in list(reversed(self.protocol.step_history)):
                        self.render_processing_step(step)
        with col2:
            st.subheader("Upcoming")
            if self.protocol.step_queue is not None:
                with st.container(height=600):
                    for step in self.protocol.step_queue:
                        self.render_processing_step(step)
        with col3:
            btnNextStep = st.button("Run next step", key="next_protocol_step")
            autoContinue = st.checkbox(
                "Autocontinue", key="auto_continue_protocol", value=False
            )
            if btnNextStep or autoContinue:
                # while True:
                with st.spinner("Running..."):
                    pm_api.run_protocol_single_step(sts[SELECTED_PROTOCOL_ID])
                    st.rerun()

    def render_processing_step(self, step: ProcessingStep,
                               with_layer_name: bool = True,
                               only_layer: str | None = None,
                               ):
        if step is not None:
            layer = None
            if 'projectId' in step.properties:
                layer = self.get_layer_of_project_id(step.properties['projectId'])
                # st.text(layer.name + " " + only_layer)
                if only_layer is not None and not only_layer == layer.name:
                    return
            with st.container(border=True):
                properties_copy = step.properties.copy()
                runtime = properties_copy.pop('runtime', None)
                if runtime is not None:
                    runtime_html = f'<div style="color: gray; font-size: smaller; text-align: right;">{round(float(runtime), 1)}s</div>'
                else:
                    runtime_html = ''

                type_displays = {
                    "RECLASSIFY_PAIRS": "Reclassify",
                    "UPDATE_SUBPROJECT_WITH_UNCERTAIN_LINKS": "Fetch uncertain links and reencoded records",
                    "DETERMINE_UNCERTAIN_LINKS": "Determine uncertain links",
                    "UPDATE_MATCHER": "Update classification model",
                    "REPORT_PAIRS": "Report reviewed predictions",
                    "RUN_INITIAL_LINKAGE": "Run initial linkage",
                    "TRANSFER_ENCODED_DATASET": "Transfer initial encoded dataset",
                }
                step_name = step.type
                if step.type in type_displays:
                    step_name = type_displays[step.type]
                if layer is None:
                    color = "gray"
                else:
                    color = get_layer_color(layer.name)
                st.markdown(
                    f"""
                    <div style="display: flex; justify-content: space-between; align-items: center; width: 100%; padding-bottom: 20px;">
                        <div style="font-weight: bold; text-align: left; text-decoration: underline; text-underline-offset: 5px; text-decoration-thickness: 3px; text-decoration-color: {color};">{step_name}</div>
                        {runtime_html}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                self.render_processing_step_properties(properties_copy, with_layer_name)
                render_report_groups(list(step.report_groups.values()))

    def render_processing_step_properties(self, properties: dict[str, str],
                                          with_layer_name: bool = True):
        if with_layer_name:
            if 'projectId' in properties:
                layer = self.get_layer_of_project_id(properties['projectId'])
                color = get_layer_color(layer.name)
                st.markdown(f":{color}[{layer.name}]")
        properties_copy = properties.copy()
        if 'projectId' in properties_copy:
            del properties_copy['projectId']
        if len(properties_copy) > 0:
            # st.json(properties_copy)
            df = pd.DataFrame(list(properties_copy.items()),
                              columns=["Property", "Value"])
            st.dataframe(df, use_container_width=True, hide_index=True,
                         column_config=None)

    def get_layer_with_name(self, name: str):
        for layer in self.protocol.layers:
            if layer.name == name:
                return layer

    def get_layer_of_project_id(self, project_id: str):
        for layer in self.protocol.layers:
            if layer.project_id == project_id:
                return layer
