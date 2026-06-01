import numpy as np
import pandas as pd
from pprl_protocol_manager_service_api_client import MultiLayerProtocol

from goodall.utils.utils import hash_pydantic


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


def build_df_runs(protocols: list[MultiLayerProtocol],
                  raw_protocols_for_repetition_detection: list[MultiLayerProtocol] | None = None,
                  plaintext_dataset_id_mapping: dict[int, str] | None = None,
                  rbf_dataset_id_mapping: dict[int, str] | None = None,
                  ) -> pd.DataFrame:
    if plaintext_dataset_id_mapping is None:
        plaintext_dataset_id_mapping = {}
    if rbf_dataset_id_mapping is None:
        rbf_dataset_id_mapping = {}

    columns = [
        "RBF",
        "ABF",
        "PPCR",
        "plaintextDatasetId",
        "rbfDatasetId",
        "rbfInitThreshold",
        "ppcrErr",
        "ppcrBudget",
        "repetition",
    ]

    rows = []
    repetition_counter = {}  # tracks how many times each (config) combo appeared

    for idx, protocol in enumerate(protocols):
        error_rate = protocol.layers[2].error_rate
        error_rate = 0.0 if error_rate is None or np.isnan(error_rate) else error_rate
        new_row = {
            "rbfInitThreshold": protocol.layers[0].initial_threshold,
            "ppcrErr": error_rate,
            "ppcrBudget": protocol.layers[2].budget,
        }
        mapped_pt_id = plaintext_dataset_id_mapping.get(protocol.plaintext_dataset_id, None)
        if mapped_pt_id:
            new_row["plaintextDatasetId"] = mapped_pt_id
        else:
            new_row["plaintextDatasetId"] = protocol.plaintext_dataset_id
        mapped_rbf_id = rbf_dataset_id_mapping.get(protocol.plaintext_dataset_id, None)
        if mapped_rbf_id:
            new_row["rbfDatasetId"] = mapped_rbf_id
        else:
            new_row["rbfDatasetId"] = protocol.initial_dataset_id

        # Build a hashable key for repetition tracking (based on all identifying fields)
        if raw_protocols_for_repetition_detection:
            p = raw_protocols_for_repetition_detection[idx]
            key = hash_pydantic(p)
            key = key + str(new_row["plaintextDatasetId"])
        else:
            key = tuple(new_row.items())
        repetition_counter[key] = repetition_counter.get(key, 0) + 1
        new_row["repetition"] = repetition_counter[key]

        new_row["RBF"] = protocol.layers[0].project_id
        new_row["ABF"] = protocol.layers[1].project_id
        new_row["PPCR"] = protocol.layers[2].project_id
        rows.append(new_row)
    df = pd.DataFrame(rows, columns=columns)
    return df


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
