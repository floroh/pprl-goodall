from typing import Tuple
from loguru import logger

import pandas as pd
from pprl_data_owner_service_api_client import AnalysisResultDto, ReportGroup

from goodall.api_helper.parser import get_report_output
from goodall.utils.constants import ATTRIBUTE_REPLACEMENTS


def get_analysis_report(analysis_result: AnalysisResultDto,
                        report_name: str,
                        report_group_name: str = "all") -> None | Tuple[
    str, pd.DataFrame | None]:
    return get_report_output(analysis_result.report_groups, report_name, report_group_name)



def get_dataset_metrics(dataset_analysis: AnalysisResultDto) -> dict[str, float]:
    metrics: dict[str, float] = {}

    def add_metrics_from_report(report_name: str, key_col: str, value_col: str,
                                prefix: str,
                                skip_values: set[str] = set()):
        """Fetches a report, checks nulls, and adds metrics to the dict."""
        result = get_analysis_report(dataset_analysis, report_name)
        if result is None:
            return
        _, df = result
        if df is None or key_col not in df.columns or value_col not in df.columns:
            return
        for key, value in zip(df[key_col], df[value_col]):
            if pd.notna(key) and pd.notna(value) and str(
                    key).lower() not in skip_values:
                metrics[f"{prefix}.{key}"] = float(value)

    # RecordCounter
    add_metrics_from_report("RecordCounter", "source", "count", "size")

    # RecordOverlap
    add_metrics_from_report("RecordOverlap", "source pair", "overlap", "overlap",
                            skip_values={"total"})

    # RecordOverlap relative
    total_size = metrics.get("size.total")
    if total_size:
        for metric, value in list(metrics.items()):
            if metric.startswith("overlap."):
                rel_metric = metric.replace("overlap.", "overlap-relative.")
                metrics[rel_metric] = value / (total_size / 2)

    # RecordLength
    add_metrics_from_report("RecordLength", "source", "mean", "record_length_mean")

    # ClusterPairwiseEqualCount
    add_metrics_from_report("ClusterPairwiseEqualCount", "#errors", "share",
                            "attributes_diff_share")

    # AttributeAvailability
    add_metrics_from_report("AttributeAvailability", "attribute", "missing",
                            "attribute_missingness")

    # AttributeLength (mean + median)
    add_metrics_from_report("AttributeLength", "attribute", "mean",
                            "attribute_length_mean")
    add_metrics_from_report("AttributeLength", "attribute", "median",
                            "attribute_length_median")

    return metrics

def get_report_names(report_groups: dict[str, ReportGroup],
                      report_group_name: str = "all") -> list[str] | None:
    try:
        return list(report_groups[report_group_name].reports.keys())
    except:
        logger.warning(f"Failed to parse TAG_BASED_DATASET_ANALYSIS result "
                       f"in group {report_group_name}.")
    return None

def get_report_groups_names(analysis_result: AnalysisResultDto) -> list[str] | None:
    try:
        return list(analysis_result.report_groups.keys())
    except:
        logger.warning("Failed to parse TAG_BASED_DATASET_ANALYSIS result.")
    return None

def parse_sub_reports(df_sub_reports: pd.DataFrame,
                      result: AnalysisResultDto,
                      selected_report: str,
                      report_group_name: str,
                      dataset_name: str):
    if selected_report in ["AttributeLength", "AttributeMostFrequent"]:
        report_names = get_report_names(result.report_groups)
        matching_report_names = [rn for rn in report_names if
                                 rn.startswith(selected_report)]
        for matching_report_name in matching_report_names:
            _, df_sub_report = get_analysis_report(result,
                                                   matching_report_name)
            parts = matching_report_name.split(">>>")
            if len(parts) > 1:
                # Only use exact report matches, not "AttributeMostFrequentBigram" etc
                if selected_report != parts[0]:
                    continue
                attribute_name = parts[1]
                logger.info(f"Found report for attribute {attribute_name}")
                df_sub_report: pd.DataFrame = df_sub_report
                # if selected_report in ["AttributeMostFrequent"]:
                #     df_sub_report = df_sub_report.head(top_n_values)
                df_sub_report["dataset_name"] = dataset_name
                df_sub_report["attribute_name"] = attribute_name
                df_sub_report["group"] = report_group_name
                if df_sub_reports is None:
                    df_sub_reports = df_sub_report
                else:
                    df_sub_reports = pd.concat([df_sub_reports, df_sub_report],
                                               ignore_index=True, axis="rows")
    if df_sub_reports is not None:
        df_sub_reports["attribute_name"] = df_sub_reports["attribute_name"].replace(ATTRIBUTE_REPLACEMENTS)
    return df_sub_reports