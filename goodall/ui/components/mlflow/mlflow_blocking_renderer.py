import pandas as pd
import streamlit as st

from goodall.plotting.plotly_helper import get_box_plots
from goodall.tracking.experiment_modifier import TAG_LINKAGE_METHOD_BLOCKING
from goodall.ui.components.mlflow.mlflow import filter_by_column
from goodall.ui.components.mlflow.mlflow_result_renderer import MlflowResultRenderer, \
    group_and_aggregate, parse_metrics_wide_to_long, filter_by_selected_metrics, \
    show_r_p_curve, add_combined_group_column


class MlflowBlockingRenderer(MlflowResultRenderer):
    def __init__(self, df_dataset_runs: pd.DataFrame | None = None):
        super().__init__(df_dataset_runs)

    def render(self, df_children: pd.DataFrame):
        df_children = self.join_dataset_name_if_possible(df_children)
        blocking_method_col = f"tags.{TAG_LINKAGE_METHOD_BLOCKING}"
        if st.checkbox("Include derived blocking metrics"):
            df_children["metrics.blocking.pc-r"] = df_children["metrics.blocking.pc"] - df_children["metrics.recall.bestthr"]
            df_children["metrics.blocking.r-to-pc"] = df_children["metrics.recall.bestthr"] / df_children["metrics.blocking.pc"]
            df_children["metrics.blocking.pq-to-p"] = df_children["metrics.blocking.pq"] / df_children["metrics.precision.bestthr"]
            df_children["metrics.blocking.r-to-pc.hand2018-p50"] = df_children["metrics.recall.hand2018-p50"] / df_children["metrics.blocking.pc"]
            df_children["metrics.blocking.pq-to-p.hand2018-p50"] = df_children["metrics.blocking.pq"] / df_children["metrics.precision.hand2018-p50"]
        # df_children["dataset_short_name"] = df_children["tags.dataset.name"].apply(get_dataset_short_name)

        df_children = filter_by_column(df_children, blocking_method_col)
        encoding_method_col = "tags.linkage.method.encoding"
        df_children = filter_by_column(df_children, encoding_method_col)
        options = [blocking_method_col, "dataset_name", encoding_method_col]
        group_by_tags = st.multiselect("Group by", options, default=options[0])
        if group_by_tags:
            add_combined_group_column(df_children, group_by_tags)
            st.dataframe(df_children)
            group_and_aggregate(df_children, group_by_tags)
            disabled_metrics = ["f1-score", "recall", "precision", "AUC.noYaxisPt"]
            disabled_metrics_search = ["runtime", "brier", "fstar", "ece"]
            disabled_metrics_search.extend([".loss.", "dataset.", "accuracy"])
            disabled_metrics_search.extend([".blockcount", ".paircount"])
            df_long = parse_metrics_wide_to_long(df_children)
            df_long, selected_metrics = filter_by_selected_metrics(df_long, group_by_tags,
                                                      disabled_metrics=disabled_metrics,
                                                      disabled_metrics_search=disabled_metrics_search
                                                      )
            fig = get_box_plots(df_long, x_col="metric_name", y_col="metric",
                                  color_col="group")
            if st.button("Export"):
                fig.write_image(file="tmp.pdf")
            st.plotly_chart(fig)
            show_r_p_curve(df_children, "group-no-ds")
        else:
            st.dataframe(df_children)