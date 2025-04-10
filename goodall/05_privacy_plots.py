import argparse
import os

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

from goodall.multi_layer_evaluation.helper import get_run_description


def read_data(directory: str):
    project_type = "ppcrProject"
    q = pd.read_csv(os.path.join(directory, "privacy_results_ppcr.csv"), sep=",")
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
    return q


def filter_data(figure: str, eval_raw_df: pd.DataFrame) -> pd.DataFrame:
    if figure == "fig6_left":
        eval_raw_df = eval_raw_df[eval_raw_df["plaintextDatasetId"] == 2032]
    elif figure == "fig6_right":
        eval_raw_df = eval_raw_df[eval_raw_df["plaintextDatasetId"] == 2042]
    eval_raw_df = eval_raw_df[eval_raw_df["ppcrErr"] == 0.2]
    eval_raw_df = eval_raw_df[eval_raw_df["ppcrBudget"] == 200]
    return eval_raw_df


def render_plot(eval_raw_df: pd.DataFrame, output_path: str):
    eval_2 = eval_raw_df.loc[eval_raw_df["Unnamed: 0"] == 2, :]
    eval_2 = eval_2.reset_index(drop=True)
    eval_no_restrictions = pd.concat(
        [
            eval_2["KAPR"],
            eval_2["FIRSTNAME availability"],
            eval_2["MIDDLENAME availability"],
            eval_2["LASTNAME availability"],
            eval_2["YEAROFBIRTH availability"],
            eval_2["CITY availability"],
            eval_2["PLZ availability"],
            eval_2["PLACEOFBIRTH availability"],
        ]
    )
    eval_1 = eval_raw_df.loc[eval_raw_df["Unnamed: 0"] == 1, :]
    eval_1 = eval_1.reset_index(drop=True)
    eval_no_equal_attributes = pd.concat(
        [
            eval_1["KAPR"],
            eval_1["FIRSTNAME availability"],
            eval_1["MIDDLENAME availability"],
            eval_1["LASTNAME availability"],
            eval_1["YEAROFBIRTH availability"],
            eval_1["CITY availability"],
            eval_1["PLZ availability"],
            eval_1["PLACEOFBIRTH availability"],
        ]
    )
    eval_4 = eval_raw_df.loc[eval_raw_df["Unnamed: 0"] == 4, :]
    eval_4 = eval_4.reset_index(drop=True)
    eval_sim = pd.concat(
        [
            eval_4["KAPR"],
            eval_4["FIRSTNAME availability"],
            eval_4["MIDDLENAME availability"],
            eval_4["LASTNAME availability"],
            eval_4["YEAROFBIRTH availability"],
            eval_4["CITY availability"],
            eval_4["PLZ availability"],
            eval_4["PLACEOFBIRTH availability"],
        ]
    )
    values_df = pd.concat([eval_no_restrictions, eval_no_equal_attributes, eval_sim])

    length = len(eval_2)
    length_all = 3 * length

    metric = (
        ["KAPR"] * length
        + ["FN"] * length
        + ["MN"] * length
        + ["LN"] * length
        + ["YOB"] * length
        + ["CITY"] * length
        + ["ZIP"] * length
        + ["POB"] * length
    )

    metric = metric * 3

    method_names = (
        ["No restrictions"] * 8 * length
        + ["No equal attributes"] * 8 * length
        + ["sim(0.4,1.0)"] * 8 * length
    )

    eval_df = pd.DataFrame({"METHOD": method_names, "SCORE": values_df, " ": metric})

    # Boxplot Figure Workaround: Changed Background Color of Boxplot and Legend and the Position of the Legend
    fig, ax = plt.subplots(1, figsize=(9, 6))
    sns.set_style("whitegrid")

    plt.rcParams.update({'font.size': 16})

    sns.boxplot(x=" ", y="SCORE", hue="METHOD", data=eval_df)
    ax.vlines(x=[0.5], ymin=-0.05, ymax=1.05,
              linestyles=["dashed"], colors=["Gray"])
    ax.text(x=4, y=-0.165, s="Attribute availability", ha="center", va="bottom", fontsize=22)
    ax.set(ylim=(0, 1.02))

    plt.ylabel(ylabel="SCORE", fontsize=20)
    ax.tick_params(axis='both', which='major', labelsize=18)
    ax.tick_params(axis='both', which='minor', labelsize=18)

    plt.grid(axis="y")
    plt.tight_layout()
    legend = ax.legend(loc='best')
    legend.get_frame().set_facecolor('white')

    plt.savefig(output_path, format="pdf", bbox_inches="tight")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("figure",
                        help="Name of the figure (fig6_left, fig6_right)")  # Add arguments here
    args = parser.parse_args()
    figure = args.figure
    result_directory = "results"

    directory = None
    if figure == "fig6_left":
        directory = os.path.join(result_directory, "fig3")
    elif figure == "fig6_right":
        directory = os.path.join(result_directory, "fig4_right")
    output_path = os.path.join(result_directory, f"{figure}.pdf")

    if not os.path.exists(directory):
        raise RuntimeError("Result directory " + directory + " does not exist")
    eval_raw_df = read_data(directory)
    eval_raw_df = filter_data(figure, eval_raw_df)
    render_plot(eval_raw_df, output_path)

if __name__ == '__main__':
    main()
