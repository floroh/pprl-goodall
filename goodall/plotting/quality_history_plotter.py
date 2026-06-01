from enum import Enum
from loguru import logger
import numpy as np
import pandas as pd
import plotly.io as pio
import plotly.graph_objects as go

from goodall.plotting.link_improvement import plot_quality_history
from goodall.result_analysis.multi_layer_evaluation.helper import get_run_description, \
    drop_results_before_reclassification

pio.templates.default = "plotly_white"

# Fix error message in plotly outputs
pio.kaleido.scope.mathjax = None
np.set_printoptions(legacy="1.25")


class IterationPlotStyle(Enum):
    AVERAGE_ONLY = 1
    AVERAGE_AND_RANGE = 2


class DataToShow(Enum):
    BUDGET_THRESHOLD = 1
    BUDGET_ERROR = 2
    BUDGET = 3
    ERROR = 4
    BUDGET_DATASET = 5
    HARDENING_DATASET = 6
    THRESHOLD = 7


class PlotDefinition:
    plot_mode = DataToShow.BUDGET_THRESHOLD
    iteration_plot_style = IterationPlotStyle.AVERAGE_AND_RANGE
    show_rbf_baseline = True
    show_abf_baseline = True
    exclude_results_before_reclassification = True
    filter_err = None
    filter_budget = None
    filter_dataset_ids = None
    filter_encoding = None
    name_color = "err"
    name_symbol = "rbfInitThreshold"
    reverse_colors = False
    skip_first_color = False
    legend_title = ""
    legend_x = -0.05
    legend_y = -0.3
    legend_width = 100
    file_name = "plot.pdf"


class QualityHistoryPlotter:

    def __init__(self, plot_def: PlotDefinition | None = None):
        if plot_def:
            self.plot_def = plot_def
        else:
            self.plot_def = PlotDefinition()

        self.plaintext_dataset_id_names = {}
        self.rbf_dataset_id_names = {}
        self.abf_baseline = {
            "E1S": 0.899,
            "E1M": 0.9121,
            "E1L": 0.9187,
            "E2S": 0.7175,
            "E2M": 0.7743,
        }

    @staticmethod
    def add_run_parameters_to_quality_results(df_runs: pd.DataFrame, quality_results: pd.DataFrame,
                                              layer_name: str = "RBF"):
        r = df_runs.copy(deep=True)
        r["type"] = r.apply(
            lambda row: get_run_description(row, include_repetition=False), axis=1
        )
        q = quality_results.copy(deep=True)
        q.drop(columns=["type"], inplace=True)
        q = q[q["layer_name"] == layer_name]
        q.rename(columns={"project": layer_name}, inplace=True)
        q = r[
                [
                    layer_name,
                    "repetition",
                    "type",
                    "ppcrBudget",
                    "ppcrErr",
                    "rbfInitThreshold",
                    "plaintextDatasetId",
                    "rbfDatasetId",
                ]
            ].merge(q, on=layer_name)
        # q = q.merge(
        #     r[
        #         [
        #             layer_name,
        #             "repetition",
        #             "type",
        #             "ppcrBudget",
        #             "ppcrErr",
        #             "rbfInitThreshold",
        #             "plaintextDatasetId",
        #             "rbfDatasetId",
        #         ]
        #     ],
        #     on=layer_name,
        # )
        q = q.drop(columns=[layer_name, "layer_name"])
        q.fillna({"iteration": -1}, inplace=True)
        return q

    def apply_result_filter(self, df_runs: pd.DataFrame) -> pd.DataFrame:
        if self.plot_def.filter_err is not None:
            df_runs = df_runs[df_runs["ppcrErr"] == self.plot_def.filter_err]
        if self.plot_def.filter_budget is not None:
            df_runs = df_runs[df_runs["ppcrBudget"] == self.plot_def.filter_budget]
        if self.plot_def.filter_dataset_ids is not None:
            if isinstance(self.plot_def.filter_dataset_ids, list):
                df_runs = df_runs[
                    df_runs["plaintextDatasetId"].isin(self.plot_def.filter_dataset_ids)
                ]
            else:
                df_runs = df_runs[
                    df_runs["plaintextDatasetId"] == self.plot_def.filter_dataset_ids]
        if self.plot_def.filter_encoding == "xor":
            df_runs = df_runs[df_runs["rbfDatasetId"] >= 2300]
        return df_runs

    def get_baseline(self, dataset_name: str, baseline_type: str) -> float | None:
        if baseline_type == "ABF":
            return self.abf_baseline.get(dataset_name, None)
        return None

    def plot_quality_comparison(
            self,
            df_histories: pd.DataFrame,
            x_column: str = "#Improved",
            name_color: str = "type",
            name_symbol: str = None,
            dataset_category: str = "plaintextDatasetId",
    ) -> go.Figure:
        fig_quality_history = plot_quality_history(
            df_histories,
            x_column=x_column,
            name_color=name_color,
            name_symbol=name_symbol,
            reverse_colors=self.plot_def.reverse_colors,
            skip_first_color=self.plot_def.skip_first_color
        )

        optimal_results = df_histories[df_histories["#Improved"] < 0]
        if dataset_category in optimal_results.columns:
            optimal_results.drop_duplicates(subset=[dataset_category], inplace=True)

        # Add baselines
        show_dataset_names = False
        # Show dataset names if there are multiple optimal results available (thus multiple datasets)
        if len(optimal_results) > 1 and dataset_category in optimal_results.columns:
            show_dataset_names = True
        logger.info(f"show_dataset_names={show_dataset_names}")
        pd.set_option('expand_frame_repr', False)
        logger.info(f"\n{optimal_results}")
        for i, row in optimal_results.iterrows():
            result = row #optimal_results.iloc[i]
            dataset_suffix = ""
            if show_dataset_names:
                dataset_suffix = " " + str(result[dataset_category])
            if self.plot_def.show_rbf_baseline:
                fig_quality_history.add_hline(
                    y=result["F1-score"],
                    line=dict(color="Green", width=2, dash="dash"),
                    annotation_text="Baseline RBF" + dataset_suffix,
                    annotation_position="top left",
                    annotation_font_size=12,
                )
            if dataset_category in row.index:  # Check column names
                dataset_for_abf = str(result[dataset_category])
                # dataset_for_abf = dataset_for_abf.replace("-XOR", "")
                # dataset_suffix = dataset_suffix.replace("-XOR", "")
                if self.plot_def.show_abf_baseline:
                    abf_baseline = self.get_baseline(dataset_for_abf, "ABF")
                    if abf_baseline:
                        fig_quality_history.add_hline(
                            y=abf_baseline,
                            line=dict(color="orangered", width=2, dash="dot"),
                            annotation_text="Baseline ABF" + dataset_suffix,
                            annotation_position="top left",
                            annotation_font_size=12,
                        )
            if self.plot_def.show_rbf_baseline:
                if show_dataset_names:
                    fig_quality_history.add_hline(
                        y=result["F1-score"],
                        line=dict(color="Green", width=2, dash="dot"),
                        annotation_text="Baseline " + result[dataset_category],
                        annotation_position="top left",
                        annotation_font_size=10
                    )
                else:
                    fig_quality_history.add_hline(
                        y=result["F1-score"],
                        line=dict(color="Green", width=2, dash="dot"),
                    )
        return fig_quality_history

    @staticmethod
    def aggregate_over_iterations(q: pd.DataFrame,
                                  group_by_columns: list) -> pd.DataFrame:
        q_agg_min_max = (
            q.groupby(group_by_columns)
            .aggregate(
                {
                    "F1-score": ["max", "min"],
                }
            )
            .reset_index()
        )
        aggregation_functions = {
            "recall": "mean",
            "precision": "mean",
            "F1-score": "mean",
            "TP": "sum",
            "FP": "sum",
            "FN": "sum",
            "#Improved": pd.Series.mode,
            "ppcrErr": "mean",
            "ppcrBudget": "mean",
            "rbfInitThreshold": "first",
        }
        if "rbfInitThreshold" in group_by_columns:
            del aggregation_functions["rbfInitThreshold"]

        q_agg = q.groupby(group_by_columns).aggregate(
            aggregation_functions).reset_index()
        # Select the last value for #Improved if mode returns multiple values
        q_agg["#Improved"] = q_agg["#Improved"].apply(
            lambda x: x[-1] if hasattr(x, "__len__") else x
        )

        q_agg["F1-score-avg"] = q_agg["F1-score"]
        q_agg["recallM"] = q_agg["TP"] / (q_agg["TP"] + q_agg["FN"])
        q_agg["precisionM"] = q_agg["TP"] / (q_agg["TP"] + q_agg["FP"])
        q_agg["F1-score"] = (
                2
                * q_agg["recallM"]
                * q_agg["precisionM"]
                / (q_agg["recallM"] + q_agg["precisionM"])
        )
        q_agg["F1-score-max"] = q_agg_min_max["F1-score"]["max"]
        q_agg["F1-score-min"] = q_agg_min_max["F1-score"]["min"]
        q_agg["ppcrBudget"] = q_agg["ppcrBudget"].astype(int)
        q_agg = q_agg.round({"ppcrErr": 1})
        return q_agg

    def create_figure(self, df_quality_results: pd.DataFrame,
                      df_runs: pd.DataFrame) -> go.Figure:
        df_runs = self.apply_result_filter(df_runs)
        q = self.add_run_parameters_to_quality_results(df_runs, df_quality_results)
        if self.plot_def.exclude_results_before_reclassification:
            q = drop_results_before_reclassification(q)


        q_agg = q
        q_agg.replace({"plaintextDatasetId": self.plaintext_dataset_id_names}, inplace=True)
        q_agg.replace({"rbfDatasetId": self.rbf_dataset_id_names}, inplace=True)
        dataset_category = "plaintextDatasetId"
        if self.plot_def.plot_mode == DataToShow.HARDENING_DATASET:
            dataset_category = "rbfDatasetId"
        if self.plot_def.exclude_results_before_reclassification:
            q_agg = self.aggregate_over_iterations(
                q_agg, ["type", "iteration", dataset_category, "rbfInitThreshold"]
            )
            if self.plot_def.plot_mode != DataToShow.BUDGET_THRESHOLD:
                q_agg = self.aggregate_over_iterations(q_agg,
                                                  ["type", "iteration", dataset_category])
        # q_agg.to_csv(
        #     os.path.join(output_directory, plot_def.file_name + ".csv"), index=False
        # )

        if self.plot_def.iteration_plot_style == IterationPlotStyle.AVERAGE_ONLY:
            q_agg.drop(columns=["F1-score-max", "F1-score-min"], inplace=True)

        q_agg["b"] = q_agg["ppcrBudget"]
        q_agg["err"] = q_agg["ppcrErr"]
        # q_agg["#Reviewed pairs in top layer"] = q_agg["#Improved"]
        fig_quality_history = self.plot_quality_comparison(
            q_agg,
            x_column="iteration",
            name_color=self.plot_def.name_color,
            name_symbol=self.plot_def.name_symbol,
            dataset_category=dataset_category,
        )
        # show_legend = True
        # fig_quality_history.update_layout(showlegend=show_legend)
        fig_quality_history.update_layout(
            autosize=False,
            font_size=14,
            width=500,
            height=400,
            margin=dict(l=5, r=5, b=5, t=5, pad=0),
            xaxis_title="#Reviewed pairs in top layer",
            xaxis_title_font_size=15,
            # xaxis_tickfont_size=14,
            yaxis_title="F1-score",
            yaxis_title_font_size=15,
            legend=dict(
                title=self.plot_def.legend_title,
                title_font_size=14,
                font_size=12,
                yanchor="bottom",
                y=self.plot_def.legend_y,
                xanchor="left",
                x=self.plot_def.legend_x,
                entrywidth=self.plot_def.legend_width,
                orientation="h",
            ),
        )
        return fig_quality_history
