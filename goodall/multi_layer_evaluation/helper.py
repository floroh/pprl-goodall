import numpy as np
import pandas as pd
from pprl_linkage_unit_service_api_client import AnalysisResultDto, DatasetAnalysisApi, AnalysisRequestDto

from goodall.api_helper.pprl_clients import Service, get_client
from goodall.plotting.link_improvement import plot_quality_history


def plot_quality_comparison(
        df_histories: pd.DataFrame,
        x_column: str = "#Improved",
        name_color: str = "type",
        name_symbol: str = None,
        dataset_category: str = "plaintextDatasetId",
        reverse_colors: bool = False,
        skip_first_color: bool = False,
):
    optimal_results = df_histories[df_histories["#Improved"] < 0]
    if dataset_category in optimal_results:
        optimal_results.drop_duplicates(subset=[dataset_category], inplace=True)
    quality_history = plot_quality_history(
        df_histories,
        x_column=x_column,
        name_color=name_color,
        name_symbol=name_symbol,
        reverse_colors=reverse_colors,
        skip_first_color=skip_first_color,
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
    return quality_history

def get_dataset_analysis_result(service: Service, dataset_id: str) -> AnalysisResultDto:
    analysis_controller = DatasetAnalysisApi(get_client(service))
    return analysis_controller.run_analysis(
        analysis_request_dto=AnalysisRequestDto.from_dict(
            ({"datasetId": int(dataset_id), "type": "DATASET_DESCRIPTION"})
        )
    )

def get_run_description(row,
                        include_repetition: bool = True,
                        include_initial_threshold: bool = True
                        ) -> str:
    rep = ""
    if include_repetition and "repetition" in row:
        rep = ", i=" + str(row["repetition"])
    thr = ""
    if include_repetition and "rbfInitThreshold" in row:
        thr = ", t=" + str(row["rbfInitThreshold"])
    description = (
            # format_param("t", row["rbfInitThreshold"])
            # + ", "
            format_param("e", row["ppcrErr"])
            + ", "
            + format_param("b", row["ppcrBudget"])
            + thr
            + rep
    )
    # print(description)
    return description


def format_param(short: str, value: float, digits: int = 2):
    return short + "=" + str(round(value, digits))


def add_threshold_and_iteration(run_results: pd.DataFrame,
                                previous_thresholds: list[float]) -> pd.DataFrame:
    assert "#Improved" in run_results
    df = pd.DataFrame({"thr": previous_thresholds})
    df["iteration"] = df.index
    dfEmpty = pd.DataFrame([[np.nan] * len(df.columns)], columns=df.columns)
    df = pd.concat([dfEmpty, df]).sort_index().reset_index(drop=True)

    df_stretched = pd.DataFrame(columns=["thr", "iteration"])
    t = 0
    i = -1
    for r in range(len(run_results)):
        if r == 0:
            df_stretched.loc[r] = [np.nan, np.nan]
            continue
        m = run_results.iloc[r-1]["#Improved"]
        n = run_results.iloc[r]["#Improved"]
        if r + 1 < len(run_results):
            o = run_results.iloc[r + 1]["#Improved"]
            if m != n:
                i = i + 1
            if n != o:
                t = t + 1
        else:
            t = t + 1
        df_stretched.loc[r] = [df.loc[t]["thr"], i]
    out = pd.concat([run_results, df_stretched], axis=1)
    assert np.count_nonzero(np.isnan(out['thr'])) <= 1
    assert np.count_nonzero(np.isnan(out['iteration'])) <= 1
    return out


def add_threshold(run_results: pd.DataFrame,
                                previous_thresholds: list[float]) -> pd.DataFrame:
    assert "#Improved" in run_results
    df_stretched = pd.DataFrame(columns=["thr"])
    t = -1
    for r in range(len(run_results)):
        n = run_results.iloc[r]["#Improved"]
        if n < 0:
            df_stretched.loc[r] = np.nan
            continue
        if r + 1 < len(run_results):
            o = run_results.iloc[r + 1]["#Improved"]
            if n != o:
                t = t + 1
        else:
            t = t + 1
        t = min(t, len(previous_thresholds) - 1)
        df_stretched.loc[r] = previous_thresholds[t]

    out = pd.concat([run_results, df_stretched], axis=1)
    assert np.count_nonzero(np.isnan(out['thr'])) <= 1
    return out


def add_iteration(run_results: pd.DataFrame) -> pd.DataFrame:
    assert "#Improved" in run_results

    df_stretched = pd.DataFrame(columns=["iteration"])
    i = -1
    for r in range(len(run_results)):
        if r == 0:
            df_stretched.loc[r] = [np.nan]
            continue
        m = run_results.iloc[r-1]["#Improved"]
        n = run_results.iloc[r]["#Improved"]
        if r + 1 < len(run_results):
            o = run_results.iloc[r + 1]["#Improved"]
            if m != n:
                i = i + 1
        df_stretched.loc[r] = [i]
    out = pd.concat([run_results, df_stretched], axis=1)
    assert np.count_nonzero(np.isnan(out['iteration'])) <= 1
    return out


def drop_results_before_reclassification(q: pd.DataFrame):
    q2 = q.copy(deep=True)
    for j in range(0, len(q)):
        if j + 1 >= len(q):
            break
        # m = q.iloc[j - 1]["#Improved"]
        # n = q.iloc[j]["#Improved"]
        # o = q.iloc[j + 1]["#Improved"]
        # if n == m and n != o:
        #     q2.drop(j - 1, inplace=True)
        n = q.iloc[j]["#Improved"]
        o = q.iloc[j + 1]["#Improved"]
        if n == o:
            q2.drop(j, inplace=True)
    return q2
