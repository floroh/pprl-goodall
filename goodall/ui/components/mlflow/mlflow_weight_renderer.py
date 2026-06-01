import pandas as pd
import streamlit as st

from goodall.plotting.plotly_helper import get_box_plots
from goodall.tracking.mlflow_utils import COL_DATASET_RUN_ID
from goodall.ui.components.mlflow.mlflow import filter_by_column
from goodall.ui.components.mlflow.mlflow_result_renderer import MlflowResultRenderer, \
    group_and_aggregate, parse_metrics_wide_to_long, filter_by_selected_metrics, \
    show_metric_correlation, show_r_p_curve, add_combined_group_column, \
    sort_by_metric_and_group_tags
from goodall.ui.components.protocol_tag_analyzer_from_mlflow import \
    ProtocolTagFromMlflowAnalyzer, get_df_tags


class MlflowWeightRenderer(MlflowResultRenderer):
    def __init__(self, df_dataset_runs: pd.DataFrame | None = None):
        super().__init__(df_dataset_runs)

    def render(self, df_children: pd.DataFrame):
        df_children = self.join_dataset_name_if_possible(df_children)
        df_baseline = None
        analysis_mode = st.pills("Analysis mode", ["Aggregation", "Tags"],
                                 default="Aggregation")
        if analysis_mode == "Aggregation":
            use_relative_metrics = st.checkbox("Use relative metrics to baseline", False)
            if use_relative_metrics:
                baseline_selection = st.selectbox("Baseline",
                                                       ["Unicorn", "ABF wFS", "RBF static k", "ABF weights", "RBF:Auto-W:wFS", "non-freq"])
                if baseline_selection == "Unicorn":
                    baseline_mask = df_children["tags.linkage.method"] == "PT-DL-Unicorn"
                elif baseline_selection == "ABF wFS":
                    baseline_mask = df_children["tags.linkage.weight.method"] == "ABF:Auto-W:wFS"
                elif baseline_selection == "ABF weights":
                    baseline_mask = df_children["tags.linkage.weight.method"].str.startswith("ABF:")
                elif baseline_selection == "RBF static k":
                    baseline_mask = df_children["tags.linkage.weight.method"] == "RBF:Static-k"
                elif baseline_selection == "RBF:Auto-W:wFS":
                    baseline_mask = df_children["tags.linkage.weight.method"] == "RBF:Auto-W:wFS"
                elif baseline_selection == "non-freq":
                    baseline_mask = ~df_children["tags.linkage.weight.method"].str.contains("freq")
                df_baseline = df_children[baseline_mask]
                df_children = df_children[~baseline_mask]
                matching_dataset_ids = df_baseline[COL_DATASET_RUN_ID].unique()
                df_children = df_children[
                    df_children[COL_DATASET_RUN_ID].isin(matching_dataset_ids)]
                st.info(f"Found {len(df_baseline)} baseline results.\n"
                        f"{len(df_children)} children have matching baseline.")

        if st.checkbox("Fill n/a with 0"):
            df_children = df_children.fillna("0", inplace=False)
        df_children = filter_by_column(df_children, "tags.linkage.method.encoding")

        df_children[["dataset_origin", "dataset_mod", "dataset_size", "dataset_overlap"]] = (
            df_children["dataset_name"].str.split("-", expand=True)
        )
        if analysis_mode == "Aggregation":
            self.render_aggregation(df_children, use_relative_metrics,
                                    df_baseline=df_baseline)
        elif analysis_mode == "Tags":
            self.render_tags(df_children)

    def render_tags(self, df_children: pd.DataFrame):
        st.dataframe(df_children)

        @st.cache_data
        def get_tags(selected_run_id: str) -> pd.DataFrame:
            return get_df_tags(selected_run_id)

        run_ids = df_children["run_id"].tolist()
        selected_run_id = st.selectbox("Select run", run_ids)
        selected_run_id_2 = st.selectbox("Select run 2", [None] + run_ids)

        @st.cache_data
        def get_tag_analyzer_input(mlflow_run_id: str):
            experiment_tags = get_tags(mlflow_run_id)
            st.info(f"Got {len(experiment_tags)} experiment tags")
            df_selection = df_children[df_children["run_id"] == mlflow_run_id]
            dataset_run_ids = df_selection["dataset_run_id"].tolist()
            assert len(dataset_run_ids) == 1
            dataset_run_id = dataset_run_ids[0]
            best_thr = df_selection["metrics.bestthr"].tolist()
            assert len(best_thr) == 1
            best_thr = best_thr[0]
            dataset_tags = get_tags(dataset_run_id)
            st.info(f"Got {len(dataset_tags)} dataset tags")
            return pd.concat([experiment_tags, dataset_tags]), best_thr

        df_tags, best_thr = get_tag_analyzer_input(selected_run_id)
        tag_analyzer = ProtocolTagFromMlflowAnalyzer(mlflow_run_id=selected_run_id,
                                                     df_tags=df_tags)
        tag_analyzer.ref_thr = best_thr
        if selected_run_id_2:
            df_tags_2, best_thr_2 = get_tag_analyzer_input(selected_run_id_2)
            tag_analyzer.df_tags_2 = df_tags_2
            tag_analyzer.ref_thr_2 = best_thr_2

        tag_analyzer.analyze()


    def render_aggregation(self, df_children: pd.DataFrame,
                           use_relative_metrics: bool = False,
                           df_baseline: pd.DataFrame | None = None):

        if st.checkbox("Use weight set names if available", value = True):
            weight_value_mapping = {
                "FN=1.00|MN=1.00|LN=1.00|CI=1.00|ZIP=1.00|YOB=1.00|POB=1.00": "Equal",
                "FN=2.00|MN=1.00|LN=2.00|CI=1.00|ZIP=1.00|YOB=2.00|POB=1.00": "Core",
                "FN=3.00|MN=2.00|LN=3.00|CI=1.00|ZIP=1.00|YOB=3.00|POB=2.00": "Core+"
            }
            df_children.replace(
                {"tags.linkage.weight.values": weight_value_mapping}
                , inplace=True
            )

        def get_weight_method(weight_method: str, weight_values: str) -> str:
            if "config" in weight_method:
                return f"{weight_method}: {weight_values}"
            else:
                return f"{weight_method}"

        df_children["weight_method"] = df_children.apply(
            lambda row: get_weight_method(row["tags.linkage.weight.method"],
                                          row["tags.linkage.weight.values"]),
            axis=1)

        df_children = filter_by_column(df_children, "weight_method")

        options = ["tags.linkage.weight.method", "tags.linkage.weight.values",
                   "weight_method", "tags.linkage.attributes",
                   "tags.linkage.method.encoding", "dataset_name",
                   "dataset_origin", "dataset_mod", "dataset_overlap", "dataset_size"]
        group_by_tags = st.multiselect("Group by", options, default="weight_method")
        if group_by_tags:
            st.dataframe(df_children)
            if group_by_tags == 1:
                selected_col = group_by_tags[0]
            else:
                selected_col = "group"
                add_combined_group_column(df_children, group_by_tags)

            group_and_aggregate(df_children, group_by_tags)
            disabled_metrics = ["f1-score", "recall", "precision", "AUC.noYaxisPt"]
            disabled_metrics_search = ["runtime", "blocking.", "brier", "fstar", "ece",
                                       "dataset.", "precision", "recall"]
            if use_relative_metrics:
                disabled_metrics_search.extend([".loss.", "accuracy"])
            df_long = parse_metrics_wide_to_long(df_children)
            df_long, selected_metrics = filter_by_selected_metrics(df_long,
                                                                   group_by_tags,
                                                                   disabled_metrics=disabled_metrics,
                                                                   disabled_metrics_search=disabled_metrics_search
                                                                   )
            if use_relative_metrics:
                st.dataframe(df_baseline)
                baseline_metrics = [c for c in df_baseline.columns if
                                    str(c).startswith("metrics.")]
                selected_metric_columns = [f"metrics.{m}" for m in selected_metrics]
                available_metrics_columns = [m for m in selected_metric_columns if
                                             m in baseline_metrics]
                # st.info(available_metrics_columns)
                baseline_metrics = [COL_DATASET_RUN_ID] + available_metrics_columns
                df_baseline = df_baseline[baseline_metrics].copy()
                drop_columns = [c for c in df_children.columns if str(c).startswith("metrics.") and c not in baseline_metrics]
                df_children.drop(columns=drop_columns, inplace=True)

                # Merge children with baseline metrics
                df_merged = df_children.merge(
                    df_baseline,
                    on=COL_DATASET_RUN_ID,
                    suffixes=("_child", "_baseline")
                )

                relative_metrics_method = st.selectbox("Baseline combination method",
                                                       ["Skill score", "Diff"], index=1)
                # Compute skill score for each selected metric: 1 - (child / baseline)
                for col in available_metrics_columns:
                    if relative_metrics_method == "Skill score":
                        if "brier" in col:
                            df_merged[col] = 1 - (
                                    df_merged[f"{col}_child"] / df_merged[
                                f"{col}_baseline"])
                        else:
                            df_merged[col] = df_merged[f"{col}_child"] / df_merged[
                                f"{col}_baseline"]
                    elif relative_metrics_method == "Diff":
                        df_merged[col] = df_merged[f"{col}_child"] - df_merged[
                            f"{col}_baseline"]
                    else:
                        st.error("Unsupported metric combination method.")

                # Drop temporary merged columns
                drop_cols = [f"{col}_child" for col in available_metrics_columns] + [
                    f"{col}_baseline" for col in available_metrics_columns]
                df_merged = df_merged.drop(columns=drop_cols)

                # Replace df_children with the normalized values
                # df_children = df_merged
                st.dataframe(df_merged)
                df_long = parse_metrics_wide_to_long(df_merged)
                df_long = sort_by_metric_and_group_tags(df_long, group_by_tags)

            st.plotly_chart(get_box_plots(df_long,
                                          x_col="metric_name",
                                          y_col="metric",
                                          color_col=selected_col
                                          ))
            show_metric_correlation(df_children, selected_metrics)
            show_r_p_curve(df_children, selected_col)
        else:
            st.dataframe(df_children)