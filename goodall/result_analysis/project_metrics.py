import math
import re
from typing import Tuple, Any
from loguru import logger

import numpy as np
import pandas as pd
from pandas import DataFrame
from pprl_linkage_unit_service_api_client import BatchMatchProjectDto
from sklearn.metrics import auc

from goodall.api_helper import lu_api
from goodall.api_helper.parser import get_report_output

METRIC_BLOCKING_BLOCK_COUNT = "blocking.blockcount"
METRIC_BLOCKING_PAIR_COUNT = "blocking.paircount"
METRIC_BLOCKING_RR = "blocking.rr"

METRIC_MAPPING_THIS_TO_MLFLOW = {
    "bestthr": "bestthr",
    "f1-score.bestthr": "f1-score.bestthr",
}


class ProjectMetricsAnalyzer:
    def __init__(self,
                 project_id: str | None = None,
                 project: BatchMatchProjectDto | None = None,
                 lu_logfile: str | None = None):
        self.project_id = project_id
        self.project = project
        self.lu_logfile = lu_logfile

    def get_project(self):
        if not self.project:
            self.project = lu_api.get_project(self.project_id)

    def get_metrics_from_reports(self, dataset_sizes: list[int] | None = None) -> dict[
        str, float]:
        self.get_project()
        df_thresholds = self.get_df_thresholds()
        metrics = self.get_metrics_from_thresholds(df_thresholds)
        metrics.update(self.get_blocking_metrics(dataset_sizes))
        return metrics

    def get_metrics_from_thresholds(self, df_thresholds: DataFrame) -> dict[str, Any]:
        best_thr, best_f1 = determine_best_result(df_thresholds, measure_col="F1-score")
        recall_bestthr = get_result_for_threshold(df_thresholds, best_thr,
                                                   "recall")
        precision_bestthr = get_result_for_threshold(df_thresholds, best_thr,
                                                      "precision")
        best_fstar = best_f1 / (2 - best_f1)
        l_f1_0_01 = compute_local_loss(df_thresholds, "F1-score", 0.01)
        l_f1_0_03 = compute_local_loss(df_thresholds, "F1-score", 0.03)
        l_f1_0_05 = compute_local_loss(df_thresholds, "F1-score", 0.05)
        f1_hand2018, thr_hand2018, _ = get_f1_with_equal_r_p_weights_hand2018(
            df_thresholds)
        recall_hand2018 = get_result_for_threshold(df_thresholds, thr_hand2018,
                                                   "recall")
        precision_hand2018 = get_result_for_threshold(df_thresholds, thr_hand2018,
                                                      "precision")
        metrics = {
            "AUC": compute_pr_auc(df_thresholds),
            "AUC.noYaxisPt": compute_pr_auc(df_thresholds, add_point_at_y_axis=False),
            "bestthr": best_thr,
            "thr.hand2018-p50": thr_hand2018,
            "f1-score.hand2018-p50": f1_hand2018,
            "recall.hand2018-p50": recall_hand2018,
            "precision.hand2018-p50": precision_hand2018,
            "f1-score.bestthr": best_f1,
            "recall.bestthr": recall_bestthr,
            "precision.bestthr": precision_bestthr,
            "fstar.bestthr": best_fstar,
            "f1-score.loss.0_01": l_f1_0_01,
            "f1-score.loss.0_03": l_f1_0_03,
            "f1-score.loss.0_05": l_f1_0_05,
        }
        metrics.update(get_approximate_metrics(df_thresholds))
        return metrics

    def get_blocking_metrics(self, dataset_sizes: list[int] | None = None) -> dict[
        str, float]:
        df_lq_overview = self.get_df_lq_overview()
        df_blocking_result = df_lq_overview[
            df_lq_overview["Description"] == "All pairs / Post blocking"]
        blocking_pc = df_blocking_result["recall"].tolist()[0]
        blocking_pq = df_blocking_result["precision"].tolist()[0]
        # Approximate number of pairs from confusion matrix, but TN are missing
        blocking_pair_count = (df_blocking_result["TP"].tolist()[0]
                               + df_blocking_result["FP"].tolist()[0]
                               + df_blocking_result["FN"].tolist()[0])
        blocking_groups_count = None
        if self.lu_logfile:
            # Parse blocking parameters from the LU log file if available
            blocking_groups_count = extract_value_from_log_text(self.lu_logfile,
                                                                "Number of blocking groups")
            blocking_pair_count = extract_value_from_log_text(self.lu_logfile,
                                                              "Number of pairs after blocking")
        metrics = {
            "blocking.pc": blocking_pc,
            "blocking.pq": blocking_pq,
            METRIC_BLOCKING_PAIR_COUNT: blocking_pair_count,
        }
        if blocking_groups_count:
            metrics[METRIC_BLOCKING_BLOCK_COUNT] = blocking_groups_count

        if dataset_sizes:
            total_candidates = math.prod(dataset_sizes)
            rr = 1 - blocking_pair_count / total_candidates
            metrics["blocking.rr"] = rr
        return metrics

    def get_df_lq_overview(self) -> pd.DataFrame:
        _, df_thresholds = get_report_output(
            self.project.phases["CLASSIFICATION"].report_groups,
            "Overview",
            "Linkage quality evaluation")
        return df_thresholds

    def get_df_thresholds(self) -> pd.DataFrame:
        _, df_thresholds = get_report_output(
            self.project.phases["CLASSIFICATION"].report_groups,
            "Thresholds",
            "Linkage quality evaluation")
        return df_thresholds


def compute_pr_auc(df_thresholds: pd.DataFrame,
                   add_point_at_y_axis: bool = True) -> float:
    """
    Compute the Area Under the Precision–Recall Curve (PR-AUC).

    The PR curve is defined by columns:
        - precision
        - recall

    Returns:
        float: PR-AUC value.
    """
    if df_thresholds.empty:
        return 0.0

    # Sort by recall in ascending order (standard for trapezoidal rule)
    df_thresholds = df_thresholds[["recall", "precision"]]
    if add_point_at_y_axis:
        # Add the point (r=0, p=1) (at hypothetical thr=1.01)
        # to ensure that the PR curve reaches the y-axis
        df_thresholds = pd.concat(
            [pd.DataFrame({"recall": [0.0], "precision": [1.0]}), df_thresholds],
            ignore_index=True
        )
    df_sorted = df_thresholds.sort_values("recall")

    recall = df_sorted["recall"].to_numpy()
    precision = df_sorted["precision"].to_numpy()
    return float(auc(recall, precision))


def determine_best_result(df_thresholds: pd.DataFrame,
                          measure_col: str = "F1-score") -> Tuple[float, float]:
    """
    Determine the best threshold based on a given quality measure (default: F1-score).

    Args:
        df_thresholds: DataFrame that must contain:
                       - "threshold"
                       - measure_col (e.g., "F1-score", "precision", etc.)
        measure_col: Name of the column used to pick the best threshold.

    Returns:
        (best_threshold, best_quality_value)
    """
    if df_thresholds.empty:
        return np.nan, np.nan

    if measure_col not in df_thresholds.columns:
        raise ValueError(f"Column '{measure_col}' not found in df_thresholds.")

    # Find the row with maximum metric
    idx = df_thresholds[measure_col].idxmax()
    best_row = df_thresholds.loc[idx]

    best_thr = float(best_row["threshold"])
    best_measure = float(best_row[measure_col])

    return best_thr, best_measure

def get_result_for_threshold(df_thresholds: pd.DataFrame,
                             threshold: float,
                             measure_col: str = "F1-score") -> float | dict[str, float]:
    closest_idx = (df_thresholds['threshold'] - threshold).abs().idxmin()
    selected_row = df_thresholds.loc[closest_idx]

    if measure_col is not None:
        # Return only the value from the specified column
        return float(selected_row[measure_col])
    else:
        # Return the full row as a dictionary
        return selected_row.to_dict()


def get_f1_with_equal_r_p_weights_hand2018(df_thresholds: pd.DataFrame) -> Tuple[
    float, float, float]:
    """
    Compute F1 score for a threshold which ensures that TP + FP = TP + FN
    See Hand 2018: A note on using the F-measure for evaluating record linkage algorithms
    (10.1007/s11222-017-9746-6)
    :param df_thresholds:
    :return:
    """
    if df_thresholds.empty:
        return np.nan, np.nan, np.nan
    # find the row where abs((TP + FP) - (TP + FN)) is minimal
    df_copy = df_thresholds.copy()
    df_copy['diff'] = abs(
        (df_copy['TP'] + df_copy['FP']) - (df_copy['TP'] + df_copy['FN']))
    min_idx = df_copy['diff'].idxmin()
    best_row = df_copy.loc[min_idx]
    return float(best_row['F1-score']), float(best_row['threshold']), float(
        best_row['diff'])


def get_approximate_metrics(df_thresholds: pd.DataFrame,
                            pos_gt_prob: float = 1.0,
                            neg_gt_prob: float = 0.0) -> dict[str, float]:
    """
    Approximate Brier score using aggregated TP/FP/FN per threshold table.

    Args:
      df_thresholds: DataFrame with columns ['threshold','TP','FP','FN'].
      pos_gt_prob: ground-truth probability for positive class (default 1.0).
      neg_gt_prob: ground-truth probability for negative class (default 0.0).

    Returns:
      brier_est: approximate Brier score (float)
    """
    df = df_thresholds.copy()
    for c in ['threshold', 'TP', 'FP', 'FN']:
        if c not in df.columns:
            raise ValueError(f"DataFrame must contain column '{c}'")
    # Sort descending
    df = df.sort_values('threshold', ascending=False).reset_index(drop=True)
    df['P'] = df['TP'] + df['FP']  # predicted positives at each threshold
    df['total_pos'] = df['TP'] + df['FN']  # actual positives (should be constant)
    total_pos = int(df['total_pos'].iloc[0])
    # Best estimate of N from the provided aggregates
    N_est = int(df['P'].max())
    if N_est < total_pos:  # defensive fix if numbers weird
        N_est = total_pos

    # Add virtual endpoints at threshold 1.0 (predict none positive) and 0.0 (predict all positive)
    dfs = []
    if df['threshold'].iloc[0] < 1.0:
        dfs.append(pd.DataFrame(
            [{'threshold': 1.0, 'TP': 0, 'FP': 0, 'FN': total_pos, 'P': 0,
              'total_pos': total_pos}]))
    dfs.append(df[['threshold', 'TP', 'FP', 'FN', 'P', 'total_pos']])
    if df['threshold'].iloc[-1] > 0.0:
        fp_at_0 = max(0, N_est - total_pos)
        dfs.append(pd.DataFrame(
            [{'threshold': 0.0, 'TP': total_pos, 'FP': fp_at_0, 'FN': 0, 'P': N_est,
              'total_pos': total_pos}]))

    df_ext = pd.concat(dfs, ignore_index=True).sort_values('threshold',
                                                           ascending=False).reset_index(
        drop=True)

    # Build intervals by differencing
    intervals = []
    for i in range(len(df_ext) - 1):
        t_hi = df_ext.at[i, 'threshold']
        t_lo = df_ext.at[i + 1, 'threshold']
        p_rep = (t_hi + t_lo) / 2.0
        tp_interval = max(0, int(df_ext.at[i + 1, 'TP']) - int(
            df_ext.at[i, 'TP']))  # positives in interval
        fp_interval = max(0, int(df_ext.at[i + 1, 'FP']) - int(
            df_ext.at[i, 'FP']))  # negatives in interval
        interval_count = tp_interval + fp_interval
        intervals.append({
            't_hi': t_hi, 't_lo': t_lo, 'p_rep': p_rep,
            'tp_count': tp_interval, 'fp_count': fp_interval,
            'interval_count': interval_count
        })

    intervals_df = pd.DataFrame(intervals)
    intervals_df['tp_contrib'] = intervals_df['tp_count'] * (
                (intervals_df['p_rep'] - pos_gt_prob) ** 2)
    intervals_df['fp_contrib'] = intervals_df['fp_count'] * (
                (intervals_df['p_rep'] - neg_gt_prob) ** 2)
    intervals_df['total_contrib'] = intervals_df['tp_contrib'] + intervals_df[
        'fp_contrib']

    total_contrib = intervals_df['total_contrib'].sum()
    tp_contrib = intervals_df['tp_contrib'].sum()
    fp_contrib = intervals_df['fp_contrib'].sum()
    logger.info(f"brier score contribs: total={total_contrib},"
                f" tp%={tp_contrib / total_contrib},"
                f" fp%={fp_contrib / total_contrib}")
    total_pairs = max(1, N_est)
    brier_est = total_contrib / total_pairs  # normalize by estimated N
    brier_tm = tp_contrib / total_pos
    brier_tnm = fp_contrib / (total_pairs - total_pos)
    return {
        "brier_score_approx": float(brier_est),
        "brier_score_tm_approx": float(brier_tm),
        "brier_score_tnm_approx": float(brier_tnm),
        "log_loss_approx": get_logloss_from_intervals(intervals_df),
        "ece_approx": approx_ece_from_intervals(intervals_df)
    }


def get_logloss_from_intervals(intervals_df: pd.DataFrame, eps: float = 1e-12) -> float:
    # positives contribute -log(p); negatives contribute -log(1-p)
    pos_term = (intervals_df['tp_count'] * -np.log(
        np.clip(intervals_df['p_rep'], eps, 1 - eps))).sum()
    neg_term = (intervals_df['fp_count'] * -np.log(
        np.clip(1.0 - intervals_df['p_rep'], eps, 1 - eps))).sum()
    total_samples = intervals_df['interval_count'].sum()
    return float((pos_term + neg_term) / max(1, total_samples))


# Optional: approximate ECE using intervals (absolute difference between mean p and observed fraction)
def approx_ece_from_intervals(intervals_df: pd.DataFrame) -> float:
    # observed fraction in interval = tp_count / interval_count
    df = intervals_df.copy()
    df['obs_frac'] = df['tp_count'] / df['interval_count'].replace(0, np.nan)
    df['abs_err'] = (df['p_rep'] - df['obs_frac']).abs() * df['interval_count']
    total = df['abs_err'].sum()
    return float(total / max(1, df['interval_count'].sum()))


def compute_local_loss(
        df_thresholds: pd.DataFrame,
        measure_col: str = "F1-score",
        distance: float = 0.05
) -> float:
    """
    Compute the local loss L_M^d for measure M within a threshold window
    [t_opt - d, t_opt + d].

    Parameters
    ----------
    df_thresholds : pd.DataFrame
        Must contain columns:
            - "threshold"
            - measure_col (e.g. "F1-score")
    measure_col : str
        Name of the quality measure column.
    distance : float
        The threshold window half-width d.

    Returns
    -------
    float
        The maximal loss of the measure M within the threshold window.
        (best_measure - worst_measure_in_window)
    """
    if df_thresholds.empty:
        return np.nan

    if measure_col not in df_thresholds.columns:
        raise ValueError(f"Column '{measure_col}' not found in df_thresholds.")

    idx_best = df_thresholds[measure_col].idxmax()
    best_row = df_thresholds.loc[idx_best]

    t_opt = float(best_row["threshold"])
    best_measure = float(best_row[measure_col])

    lo = t_opt - distance
    hi = t_opt + distance

    window_df = df_thresholds[
        (df_thresholds["threshold"] >= lo) &
        (df_thresholds["threshold"] <= hi)
        ]

    if window_df.empty:
        # No points in window → define loss as zero
        return 0.0

    worst_measure = float(window_df[measure_col].min())
    loss = best_measure - worst_measure

    return loss


def check_metrics_identity(local_metrics: dict,
                           run_metrics: dict,
                           keys=None,
                           precision: int = 6):
    """
    Compare locally computed metrics with those stored in run.data.metrics.

    Raises:
        ValueError if metrics differ beyond the allowed precision.
    """
    if keys is None:
        keys = METRIC_MAPPING_THIS_TO_MLFLOW

    tol = 10 ** (-precision)

    for local_key, mlflow_run_key in keys.items():

        if local_key not in local_metrics:
            raise KeyError(f"Local metric '{local_key}' is missing.")
        if mlflow_run_key not in run_metrics:
            logger.debug("New metrics key which is not tracked in mlflow metrics.")
            raise KeyError(
                f"Run metric '{mlflow_run_key}' is missing in run.data.metrics.")

        local_val = local_metrics[local_key]
        run_val = run_metrics[mlflow_run_key]

        # Compare with tolerance
        if not math.isclose(local_val, run_val, rel_tol=0, abs_tol=tol):
            raise ValueError(
                f"Metric mismatch for '{local_key}': "
                f"local={local_val:.12f}, run={run_val:.12f}, "
                f"allowed tolerance={tol}"
            )


def filter_metrics(metrics: dict, patterns: list[str]) -> dict:
    """
    Filters a dictionary of metrics to only include keys that match any of the given patterns.
    """
    regexes = [re.compile(p) for p in patterns]

    def matches(key):
        return any(r.match(key) for r in regexes)

    return {k: v for k, v in metrics.items() if matches(k)}


def get_differing_metrics(
        local_metrics: dict[str, float],
        run_metrics: dict[str, float],
        keys: list[str] | None = None,
        precision: int = 6
) -> dict[str, float]:
    """
    Return a dict of metrics that are missing or differ from run_metrics.

    Parameters
    ----------
    local_metrics : dict
        Locally computed metrics.
    run_metrics : dict
        Metrics from run.data.metrics.
    keys : list or None
        If provided, restrict comparison to these keys.
    precision : int
        Number of decimal digits allowed for value comparison (default 6).
    """
    tol = 10 ** (-precision)
    diff = {}

    check_keys = keys if keys is not None else local_metrics.keys()

    for key in check_keys:
        local_val = local_metrics.get(key, None)
        run_val = run_metrics.get(key, None)

        # New metric
        if key not in run_metrics:
            diff[key] = local_val
            continue

        # Missing in local
        if local_val is None:
            continue

        # Value changed beyond tolerance
        if not math.isclose(local_val, run_val, rel_tol=0, abs_tol=tol):
            diff[key] = local_val

    return diff


def extract_value_from_log_text(log_text, label):
    """
    Extract the integer following the first occurrence of a label.
    Example label: 'Number of blocking groups'
    Returns int or None.
    """
    pattern = rf"{re.escape(label)}:\s*(\d+)"
    match = re.search(pattern, log_text)
    return int(match.group(1)) if match else None
