import os

import pandas as pd

from goodall.multi_layer_evaluation.helper import get_run_description


def prepare_data(directory: str):
    project_type = "abfProject"
    q = pd.read_csv(os.path.join(directory, "privacy_results_abf.csv"), sep=",")
    r = pd.read_csv(os.path.join(directory, "projectTable.csv"))
    r["type"] = r.apply(
        lambda row: get_run_description(row, include_repetition=False), axis=1
    )
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
    q = q[q["plaintextDatasetId"] == 2032]
    return q


def compute_kabf_privacy_measures(eval_raw_df: pd.DataFrame):
    values_df = pd.concat([eval_raw_df['Count'], eval_raw_df['Gini'], eval_raw_df['JSD']])
    values_df = values_df.reset_index(drop=True)

    metric = pd.concat([eval_raw_df['attribute'], eval_raw_df['attribute'], eval_raw_df['attribute']])
    metric = metric.reset_index(drop=True)

    length = len(eval_raw_df)
    method_names = (
            ["Count"] * length
            + ["Gini"] * length
            + ["JSD"] * length
    )

    y_axis = "Distance to uniform dist."
    eval_df = pd.DataFrame({"METHOD": method_names, y_axis: values_df, "Attribute": metric})

    agg_df = eval_df.groupby(['METHOD', 'Attribute']).aggregate(
                {
                    y_axis: ["mean"],
                }
            ).reset_index()
    print(agg_df.round(3))

def main():
    result_directory = "results"

    directory = os.path.join(result_directory, "fig3")
    if not os.path.exists(directory):
        raise RuntimeError("Result directory " + directory + " does not exist")

    eval_raw_df = prepare_data(directory)
    print("KABF privacy measures for Table 4:")
    compute_kabf_privacy_measures(eval_raw_df)

if __name__ == '__main__':
    main()
