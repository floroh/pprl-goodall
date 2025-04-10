import argparse
import os
from enum import Enum
from typing import Tuple

import numpy as np
import pandas as pd
import plotly.io as pio

from goodall.multi_layer_evaluation.helper import get_run_description, \
    drop_results_before_reclassification, plot_quality_comparison

pio.templates.default = "plotly_white"

# Fix error message in plotly outputs
pio.kaleido.scope.mathjax = None
np.set_printoptions(legacy='1.25')

plaintext_dataset_id_names = {2030: "E1S", 2032: "E1M", 2034: "E1L", 2040: "E2S", 2042: "E2M"}

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


class PlotDefinition:
    plot_mode = DataToShow.BUDGET
    iteration_plot_style = IterationPlotStyle.AVERAGE_AND_RANGE
    filter_err = None
    filter_budget = None
    filter_dataset = None
    filter_encoding = None
    name_color = 'err'
    name_symbol = "b"
    reverse_colors = False
    skip_first_color = False
    legend_title = ""
    legend_x = -0.05
    legend_y = -0.3
    legend_width = 100
    file_name = "plot.pdf"

project_type = "rbfProject"

def read_combined_results(directories: list[str]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    df_runs = None
    df_quality_results = None
    for directory in directories:
        prj_table_path = os.path.join(directory, "projectTable.csv")
        run_results_path = os.path.join(directory, "results_per_iteration.csv")
        dfRun = pd.read_csv(prj_table_path)
        dfRun = dfRun[dfRun.columns.drop(list(dfRun.filter(regex='Unnamed')))]
        quality_result = pd.read_csv(run_results_path)
        quality_result = quality_result[quality_result.columns.drop(list(quality_result.filter(regex='Unnamed')))]
        if df_runs is None:
            df_runs = dfRun
            df_quality_results = quality_result
        else:
            df_runs = pd.concat([df_runs, dfRun])
            df_quality_results = pd.concat([df_quality_results, quality_result])
        return df_runs, df_quality_results


def get_plot_definition(figure: str) -> PlotDefinition:
    plot_definition = PlotDefinition()
    if figure == "fig3_left":
        plot_definition.plot_mode = DataToShow.ERROR
        plot_definition.name_color = "err"
        plot_definition.name_symbol = "b"
        plot_definition.reverse_colors = True
        plot_definition.legend_title = "(err, b)"
        plot_definition.filter_budget = 100
        plot_definition.filter_dataset = [2032]
        plot_definition.file_name = "2032-error.pdf"
    elif figure == "fig3_right":
        plot_definition.plot_mode = DataToShow.BUDGET
        plot_definition.name_color = "err"
        plot_definition.name_symbol = "b"
        plot_definition.legend_title = "(err, b)"
        plot_definition.filter_err = 0.2
        plot_definition.filter_dataset = [2032]
        plot_definition.file_name = "2032-budget.pdf"
    elif figure == "fig4_left":
        plot_definition.plot_mode = DataToShow.BUDGET_DATASET
        plot_definition.name_color = "plaintextDatasetId"
        plot_definition.name_symbol = "b"
        plot_definition.legend_title = "(Dataset, b)"
        plot_definition.legend_y = -0.25
        plot_definition.filter_err = 0.2
        plot_definition.legend_width = 60
        plot_definition.filter_dataset = [2030, 2034]
        plot_definition.file_name = "E1L_S.pdf"
    elif figure == "fig4_right":
        plot_definition.plot_mode = DataToShow.BUDGET_DATASET
        plot_definition.name_color = "plaintextDatasetId"
        plot_definition.name_symbol = "b"
        plot_definition.legend_title = "(Dataset, b)"
        plot_definition.legend_y = -0.25
        plot_definition.filter_err = 0.2
        plot_definition.legend_width = 60
        plot_definition.filter_dataset = [2040, 2042]
        plot_definition.file_name = "E2M_S.pdf"
    elif figure == "fig5":
        plot_definition.plot_mode = DataToShow.HARDENING_DATASET
        plot_definition.name_color = "rbfDatasetId"
        plot_definition.name_symbol = "b"
        plot_definition.legend_title = "(Dataset, b)"
        plot_definition.legend_x = -0.1
        plot_definition.legend_y = -0.25
        plot_definition.legend_width = 90
        plot_definition.skip_first_color = True
        plot_definition.filter_budget = 300
        plot_definition.filter_dataset = [2030, 2032, 2034]
        plot_definition.filter_encoding = "xor"
        plot_definition.file_name = "223x-300-xor.pdf"
    else:
        raise RuntimeError(f"Undefined figure: {figure}")
    return plot_definition


def prepare_quality_results(df_runs: pd.DataFrame, quality_results: pd.DataFrame):
    r = df_runs.copy(deep=True)
    r["type"] = r.apply(
        lambda row: get_run_description(row, include_repetition=False), axis=1
    )
    q = quality_results.copy(deep=True)
    q.drop(columns=["type"], inplace=True)
    q = q[q["project_type"] == project_type]
    q.rename(columns={"project": project_type}, inplace=True)
    q = q.merge(
        r[[
            project_type,
            "repetition",
            "type",
            "ppcrBudget",
            "ppcrErr",
            "rbfInitThreshold",
            "plaintextDatasetId",
            "rbfDatasetId"
        ]],
        on=project_type,
    )
    q = q.drop(columns=[project_type, "project_type"])
    q.fillna({"iteration": -1}, inplace=True)
    return q


def aggregate_over_iterations(q: pd.DataFrame, group_by_columns: list) -> pd.DataFrame:
    q_agg_min_max = (
        q.groupby(group_by_columns)
        .aggregate(
            {
                "F1-score": ["max", "min"],
            }
        ).reset_index()
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

    q_agg = (
        q.groupby(group_by_columns)
        .aggregate(aggregation_functions)
        .reset_index()
    )
    # Select the last value for #Improved if mode returns multiple values
    q_agg['#Improved'] = q_agg['#Improved'].apply(
        lambda x: x[-1] if hasattr(x, "__len__") else x)

    q_agg["F1-score-avg"] = q_agg["F1-score"]
    q_agg["recallM"] = q_agg["TP"] / (q_agg["TP"] + q_agg["FN"])
    q_agg["precisionM"] = q_agg["TP"] / (q_agg["TP"] + q_agg["FP"])
    q_agg["F1-score"] = (
            2 * q_agg["recallM"] * q_agg["precisionM"] /
            (q_agg["recallM"] + q_agg["precisionM"])
    )
    q_agg["F1-score-max"] = q_agg_min_max["F1-score"]["max"]
    q_agg["F1-score-min"] = q_agg_min_max["F1-score"]["min"]
    q_agg["ppcrBudget"] = q_agg["ppcrBudget"].astype(int)
    q_agg.replace({"plaintextDatasetId": plaintext_dataset_id_names},
                  inplace=True)
    q_agg.replace({"plaintextDatasetId": {2012: "E0M"}}, inplace=True)
    q_agg.replace({"rbfDatasetId": {2230: "E1S", 2232: "E1M", 2234: "E1L", 2240: "E2S", 2242: "E2M"}}, inplace=True)
    q_agg.replace(
        {"rbfDatasetId": {2330: "E1S-XOR", 2332: "E1M-XOR", 2334: "E1L-XOR", 2340: "E2S-XOR", 2342: "E2M-XOR"}},
        inplace=True)
    q_agg = q_agg.round({"ppcrErr": 1})
    return q_agg


def apply_result_filter(df_runs: pd.DataFrame, plot_def: PlotDefinition) -> pd.DataFrame:
    if plot_def.filter_err is not None:
        df_runs = df_runs[df_runs["ppcrErr"] == plot_def.filter_err]
    if plot_def.filter_budget is not None:
        df_runs = df_runs[df_runs["ppcrBudget"] == plot_def.filter_budget]
    if plot_def.filter_dataset is not None:
        if isinstance(plot_def.filter_dataset, list):
            df_runs = df_runs[df_runs["plaintextDatasetId"].isin(plot_def.filter_dataset)]
        else:
            df_runs = df_runs[df_runs["plaintextDatasetId"] == plot_def.filter_dataset]
    if plot_def.filter_encoding == "xor":
        df_runs = df_runs[df_runs["rbfDatasetId"] >= 2300]
    return df_runs


def render_plot(plot_def: PlotDefinition, directories: list[str]):
    output_directory = directories[0]
    df_runs, df_quality_results = read_combined_results(directories)
    df_runs = apply_result_filter(df_runs, plot_def)
    q2 = prepare_quality_results(df_runs, df_quality_results)
    q = drop_results_before_reclassification(q2)

    q_agg = q
    dataset_category = "plaintextDatasetId"
    if plot_def.plot_mode == DataToShow.HARDENING_DATASET:
        dataset_category = "rbfDatasetId"
    q_agg = aggregate_over_iterations(q_agg,
                                      ["type", "iteration", dataset_category,
                                       "rbfInitThreshold"])
    q_agg = aggregate_over_iterations(q_agg,
                                      ["type", "iteration", dataset_category])
    q_agg.to_csv(os.path.join(output_directory, plot_def.file_name + ".csv"), index=False)

    if plot_def.iteration_plot_style == IterationPlotStyle.AVERAGE_ONLY:
        q_agg.drop(columns=["F1-score-max", "F1-score-min"], inplace=True)

    q_agg["b"] = q_agg["ppcrBudget"]
    q_agg["err"] = q_agg["ppcrErr"]
    # q_agg["#Reviewed pairs in top layer"] = q_agg["#Improved"]
    fig_quality_history = plot_quality_comparison(
        q_agg,
        x_column="iteration",
        name_color=plot_def.name_color,
        name_symbol=plot_def.name_symbol,
        dataset_category=dataset_category,
        reverse_colors=plot_def.reverse_colors,
        skip_first_color=plot_def.skip_first_color,
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
            title=plot_def.legend_title,
            title_font_size=14,
            font_size=12,
            yanchor="bottom",
            y=plot_def.legend_y,
            xanchor="left",
            x=plot_def.legend_x,
            entrywidth=plot_def.legend_width,
            orientation="h",
        ),
    )

    output_filename = os.path.join(output_directory, plot_def.file_name)
    fig_quality_history.write_image(
        file=output_filename)
    # for d in fig_quality_history.data:
    #     d.update(showlegend=show_legend)
    print("Created plot: " + output_filename)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("figure",
                        help="Name of the figure (fig3_left, fig3_right, fig4_left, fig4_right, fig5)")  # Add arguments here
    args = parser.parse_args()
    figure = args.figure
    result_directory = "results"

    if "fig3" in figure:
        output_directory = os.path.join(result_directory, "fig3")
    else:
        output_directory = os.path.join(result_directory, figure)

    if not os.path.exists(output_directory):
        raise RuntimeError("Result directory " + output_directory + " does not exist")
    render_plot(get_plot_definition(figure), [output_directory])

if __name__ == '__main__':
    main()
