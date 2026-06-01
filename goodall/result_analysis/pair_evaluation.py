import pandas as pd
import numpy as np

from pandas import DataFrame
from scipy.interpolate import UnivariateSpline

list_of_expected_types = ["TP", "FP", "FN", "TN"]


def combine_FP(df: DataFrame, column_names: list[str] | None = None) -> DataFrame:
    if column_names is None:
        column_names = ["type", "type_x", "type_y"]
    for column_name in column_names:
        df = df.replace({column_name: {"FPs": "FP", "FPd": "FP"}})
    return df


def combine_MatchGrade(df: DataFrame) -> DataFrame:
    mapping = {
        "POSSIBLE_MATCH": "NON_MATCH",
        "PROBABLE_MATCH": "CERTAIN_MATCH",
    }
    return df.replace(
        {
            "matchGrade": mapping,
            "matchGrade_x": mapping,
            "matchGrade_y": mapping,
        }
    )


def add_missing_link_types(df: DataFrame) -> DataFrame:
    for type in list_of_expected_types:
        if type not in df:
            df[type] = 0
    return df


def add_relative_share(df: DataFrame, columnName: str, method: str = "max"):
    if columnName in df:
        if method == "max":
            ref = df[columnName].max()
            df[columnName + "/all"] = df[columnName].div(ref)
        else:
            ref = df[columnName].count()
            df[columnName + "/all"] = df[columnName].div(ref)


def get_type_stats_by_probability(df: DataFrame) -> DataFrame:
    grouped = pd.crosstab(
        df["type"],
        pd.cut(
            df["probability"],
            np.arange(0.5, 1.01, 0.05).tolist(),
        ),
    )
    cum = grouped.cumsum(axis=1)
    cum = cum.transpose()
    cum = cum.reset_index()
    cum.insert(1, "max-probability", pd.IntervalIndex(cum["probability"]).right)
    cum["probability"] = cum["probability"].astype(str)
    cum = cum.replace(to_replace="(0.\d+,", value="(0.5,", regex=True)
    add_relative_share(cum, "FN")
    add_relative_share(cum, "FP")
    add_relative_share(cum, "TP")
    add_relative_share(cum, "TN")
    return cum


def get_type(similarity: float, threshold: float, ground_truth_label: str) -> str:
    if similarity >= threshold:
        if ground_truth_label == "TRUE_MATCH":
            return "TP"
        elif ground_truth_label == "TRUE_NON_MATCH":
            return "FP"
        else:
            raise ValueError
    else:
        if ground_truth_label == "TRUE_NON_MATCH":
            return "TN"
        elif ground_truth_label == "TRUE_MATCH":
            return "FN"
        else:
            raise ValueError

def get_gt_label(eval_type: str) -> str:
    if eval_type == "TP" or eval_type == "FN":
        return "TRUE_MATCH"
    elif "FP" in eval_type or eval_type == "TN":
        return "TRUE_NON_MATCH"

def add_ground_truth_label(df: pd.DataFrame, col_eval_type: str = "Eval-Type") -> pd.DataFrame:
    cur_out = df.copy(deep=True)
    cur_out["gtLabel"] = cur_out.apply(
        lambda row: get_gt_label(row[col_eval_type]), axis=1
    )
    return cur_out

def get_real_probability(
    similarity_upper_bound: float,
    threshold: float,
    TP: float,
    FP: float,
    FN: float,
    TN: float,
) -> float:
    if similarity_upper_bound <= threshold:
        if (TN + FN) == 0:
            return 0
        return TN / (TN + FN)
    else:
        if (TP + FP) == 0:
            return 0
        return TP / (TP + FP)


def get_real_probabilities_by_thresholds(
    input: DataFrame, thresholds: list
) -> DataFrame:
    df = input.copy()
    out = None
    for threshold in thresholds:
        cur_out = get_real_probabilities_by_threshold(df, threshold)
        cur_out["threshold"] = threshold
        if out is None:
            out = cur_out
        else:
            out = pd.concat([out, cur_out])
    return out


def get_real_probabilities_by_threshold(
    input: DataFrame, threshold: float, bin_size: float = 0.01
) -> DataFrame:
    df = add_threshold_dependent_type(input, threshold)
    grouped = pd.crosstab(
        df["type_thr"],
        pd.cut(df["similarity"], np.arange(0.5, 1.0, bin_size).tolist(), right=False),
    )
    grouped = grouped.transpose()
    grouped = grouped.reset_index()
    grouped.insert(
        1, "similarity-upper-bound", pd.IntervalIndex(grouped["similarity"]).right
    )
    grouped["similarity"] = grouped["similarity"].astype(str)
    grouped = add_missing_link_types(grouped)
    grouped["real-probability"] = grouped.apply(
        lambda row: get_real_probability(
            row["similarity-upper-bound"],
            threshold,
            row["TP"],
            row["FP"],
            row["FN"],
            row["TN"],
        ),
        axis=1,
    )
    return grouped


def get_quality_for_thresholds(df: pd.DataFrame, thresholds: list[float],
                               df_base: pd.DataFrame | None = None) -> pd.DataFrame:
    """
    Computes quality metrics per threshold.
    Returns one row per threshold with:
    threshold, recall, precision, F1-score, accuracy, TP, FP, FN, TN
    """
    rows = []

    # Compute minimum FN from base run if provided
    min_fn_base = df_base["FN"].min() if df_base is not None else 0

    for thr in thresholds:
        cur = df.copy(deep=False)

        # Prediction based on threshold
        pred_match = cur["similarity"] >= thr
        gt_match = cur["gtLabel"] == "TRUE_MATCH"

        TP = ((pred_match) & (gt_match)).sum()
        FP = ((pred_match) & (~gt_match)).sum()
        FN = ((~pred_match) & (gt_match)).sum()
        TN = ((~pred_match) & (~gt_match)).sum()

        # Adjust FN count to include the missed pairs form the base run
        FN = FN + min_fn_base

        precision = TP / (TP + FP) if (TP + FP) > 0 else 0.0
        recall    = TP / (TP + FN) if (TP + FN) > 0 else 0.0
        f1        = (
            2 * precision * recall / (precision + recall)
            if (precision + recall) > 0
            else 0.0
        )
        accuracy  = (TP + TN) / (TP + FP + FN + TN) if (TP + FP + FN + TN) > 0 else 0.0
        rows.append(
            {
                "threshold": thr,
                "recall": recall,
                "precision": precision,
                "F1-score": f1,
                "Accuracy": accuracy,
                "TP": TP,
                "FP": FP,
                "FN": FN,
                "TN": TN,
            }
        )
    return pd.DataFrame(rows)


def get_quality_metrics(df: pd.DataFrame,
                        df_base: pd.DataFrame | None = None) -> dict[str, float]:
    # Compute minimum FN from base run if provided
    min_fn_base = df_base["FN"].min() if df_base is not None else 0

    type_counts = df["type"].value_counts()
    TP = type_counts.get("TP", 0)
    FP = type_counts.get("FP", 0)
    FN = type_counts.get("FN", 0)
    TN = type_counts.get("TN", 0)

    # Adjust FN count to include the missed pairs form the base run
    FN = FN + min_fn_base

    precision = TP / (TP + FP) if (TP + FP) > 0 else 0.0
    recall    = TP / (TP + FN) if (TP + FN) > 0 else 0.0
    f1        = (
        2 * precision * recall / (precision + recall)
        if (precision + recall) > 0
        else 0.0
    )
    accuracy  = (TP + TN) / (TP + FP + FN + TN) if (TP + FP + FN + TN) > 0 else 0.0
    return {
            "recall": recall,
            "precision": precision,
            "f1-score": f1,
            "accuracy": accuracy
        }


def add_threshold_dependent_types(df: DataFrame, thresholds: list) -> DataFrame:
    out = None
    for thr in thresholds:
        cur_out = add_threshold_dependent_type(df, thr)
        if out is None:
            out = cur_out
        else:
            out = pd.concat([out, cur_out])
    return out


def add_threshold_dependent_type(df: DataFrame, thr: float,
                                 col_type: str = "type_thr") -> DataFrame:
    cur_out = df.copy(deep=True)
    cur_out[col_type] = cur_out.apply(
        lambda row: get_type(row["similarity"], thr, row["gtLabel"]), axis=1
    )
    # cur_out[] = df[df['similarity' >= thr] & df['gtLabel' == 'TRUE_MATCH']]
    # add_relative_share(cur_out, 'type_thr', 'count')
    cur_out["threshold"] = thr
    return cur_out


def find_threshold_used(df: DataFrame) -> float:
    min_FP_sim = df[df["type"] == "FP"]["similarity"].min()
    if np.isnan(min_FP_sim):
        min_TP_sim = df[df["type"] == "TP"]["similarity"].min()
        if np.isnan(min_TP_sim):
            return df[df["type"] == "FN"]["similarity"].max()
        return min_TP_sim
    return min_FP_sim


def fit_spline_function(
    df: DataFrame, x_col: str, y_col: str, x_min: float = 0, x_max: float = 1
):
    selection = df[(df[x_col] >= x_min) & (df[x_col] < x_max)]
    x = selection[x_col]
    y = selection[y_col]
    spl = UnivariateSpline(x, y)
    return spl


def fit_two_spline_functions(
    df: DataFrame, x_col: str, y_col: str, threshold: float
) -> list:
    spline_left = fit_spline_function(df, x_col, y_col, 0, threshold)
    spline_right = fit_spline_function(df, x_col, y_col, threshold, 1)
    spline_left.set_smoothing_factor(0.05)
    spline_right.set_smoothing_factor(0.05)
    return [spline_left, spline_right]


def two_spline_interpolation(
    similarity: float, threshold: float, spline_left, spline_right
):
    if similarity >= threshold:
        return min(1, spline_right(similarity))
    else:
        return min(1, spline_left(similarity))


def linear_interpolation(
    similarity: float,
    threshold: float,
    left_distance: float = 0.05,
    right_distance: float = 0.1,
):
    left_distance = min(threshold, left_distance)
    right_distance = min(1 - threshold, right_distance)
    if similarity >= threshold:
        return 0.5 * (1 + min(1.0, (similarity - threshold) / right_distance))
    else:
        return 0.5 * (1 + min(1.0, (threshold - similarity) / left_distance))


def get_probability(
    df: DataFrame,
    method: str,
    threshold: float,
    left_distance: float = 0.05,
    right_distance: float = 0.1,
):
    if method == "default":
        return df["probability"]
    elif method == "linear":
        return df["similarity"].apply(
            lambda sim: linear_interpolation(
                sim, threshold, left_distance, right_distance
            )
        )
    elif method == "real-spline":
        df_real_probabilities = get_real_probabilities_by_threshold(df, threshold)
        [spline_left, spline_right] = fit_two_spline_functions(
            df_real_probabilities,
            "similarity-upper-bound",
            "real-probability",
            threshold,
        )
        return df["similarity"].apply(
            lambda sim: two_spline_interpolation(
                sim, threshold, spline_left, spline_right
            )
        )
    else:
        raise ValueError("method not supported")
