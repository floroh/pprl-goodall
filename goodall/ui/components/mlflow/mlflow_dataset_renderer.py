import pandas as pd
from mlflow import MlflowException

from goodall.result_analysis.dataset_analysis_result_parser import \
    get_report_groups_names, get_analysis_report, parse_sub_reports
from goodall.ui.components.datasets import plot_attribute_statistics, \
    render_dataset_analysis_report, plot_pairwise_schema, plot_attribute_availability, \
    plot_violin, plot_attribute_frequency_distributions, \
    get_attribute_most_frequent_values_tables, plot_pairwise_schemas_subplots
from goodall.ui.components.mlflow.mlflow import get_run_dataset_description
from goodall.ui.components.mlflow.mlflow_result_renderer import MlflowResultRenderer
import streamlit as st

from goodall.utils.constants import DATASET_NAME_MAPPING


class MlflowDatasetRenderer(MlflowResultRenderer):

    def render(self, selected_runs: pd.DataFrame, run_ids: list[str]):
        show_result_jsons = st.sidebar.toggle("Show result jsons", False)
        show_individual_results = st.sidebar.toggle("Show individual results", False)
        show_distributions = st.sidebar.toggle("Show distributions", True)
        plot_individual_results = st.sidebar.toggle("Plot individual results", False)
        use_dataset_names = st.sidebar.toggle("Use datasetname if available", True)
        show_additional_results = st.sidebar.toggle("Show additional results",
                                                    False)
        top_n_values = st.sidebar.number_input("Show top N", 5, 50, value=10)
        selected_report = st.segmented_control(
            "Select report",
            ["Overview", "AttributeAvailability", "AttributeLength",
             "AttributeMostFrequent", "ClusterPairwiseDiff",
             "ClusterPairwiseEqual", "ClusterPairwiseDiffPattern"],
        )

        if selected_report is not None:
            df_reports = {}
            df_sub_reports = None
            for idx, run_id in enumerate(run_ids):
                try:
                    result = get_run_dataset_description(run_id)
                except MlflowException:
                    st.warning(
                        f"Skipping run_id={run_id} due to missing dataset description")
                    continue
                dataset_name = run_id
                if use_dataset_names:
                    current_run = selected_runs.iloc[idx]

                    # try to use 'params.dataset_name', fallback to 'tags.mlflow.runName'
                    def valid(val):
                        return pd.notna(val) and str(val) != "None"

                    for col in ['params.dataset_name', 'tags.mlflow.runName']:
                        if col in current_run and valid(current_run[col]):
                            dataset_name = current_run[col]
                            for subs, new_name in DATASET_NAME_MAPPING.items():
                                if subs in dataset_name:
                                    dataset_name = new_name
                                    break
                            break
                if show_result_jsons or show_individual_results or plot_individual_results:
                    st.text(
                        dataset_name if run_id != dataset_name else f"{dataset_name} ({run_id})")
                if selected_report == "Overview":
                    if show_result_jsons:
                        st.json(result.to_json(), expanded=False)
                    if show_individual_results:
                        with st.expander("Show dataset description", expanded=False):
                            render_dataset_analysis_report(result,
                                                           show_additional_results=show_additional_results)
                else:
                    report_group_names = get_report_groups_names(result)
                    if "Cluster" in selected_report:
                        report_group_names = ["all"]
                    for report_group_name in report_group_names:
                        report_name = f"{selected_report}>>>SchemaFrequency" \
                            if selected_report == "ClusterPairwiseDiffPattern" \
                            else selected_report
                        report, df_report = get_analysis_report(result, report_name,
                                                                report_group_name=report_group_name)
                        df_reports[dataset_name] = df_report
                        if show_distributions:
                            df_sub_reports = parse_sub_reports(df_sub_reports,
                                                               result,
                                                               selected_report,
                                                               report_group_name,
                                                               dataset_name)
                    if plot_individual_results:
                        if selected_report == "ClusterPairwiseDiffPattern":
                            plot_pairwise_schema(df_report)

            if selected_report == "AttributeAvailability":
                plot_attribute_availability(df_reports)
            elif selected_report == "AttributeLength":
                if show_distributions and df_sub_reports is not None:
                    st.dataframe(df_sub_reports)
                    plot_violin(df_sub_reports, "length")
                plot_attribute_statistics(df_reports)
            elif selected_report == "AttributeMostFrequent":
                if show_distributions and df_sub_reports is not None:
                    x_lim = st.sidebar.number_input("Distribution x-lim", 5, 1000, 50)
                    if st.button("Save reports dataframe"):
                        from datetime import datetime
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"df_sub_reports_{timestamp}.csv"
                        df_sub_reports.to_csv(filename, index=False)
                        st.success(f"Saved to {filename}")
                    figs = plot_attribute_frequency_distributions(df_sub_reports,
                                                                  x_lim=x_lim)
                    most_frequent_values_df = get_attribute_most_frequent_values_tables(
                        df_sub_reports, top_n_values)
                    for attr_name, fig in figs.items():
                        st.subheader(f"Attribute: {attr_name}")
                        st.plotly_chart(fig)
                        st.dataframe(most_frequent_values_df[attr_name])
            elif selected_report == "ClusterPairwiseDiff":
                plot_attribute_statistics(df_reports)
            elif selected_report == "ClusterPairwiseEqual":
                plot_attribute_statistics(df_reports)
            elif selected_report == "ClusterPairwiseDiffPattern":
                # plot_pairwise_schemas(df_reports)
                plot_pairwise_schemas_subplots(df_reports)
