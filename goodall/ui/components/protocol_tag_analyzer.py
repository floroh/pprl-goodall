
import pandas as pd
from pandas import DataFrame
from pprl_protocol_manager_service_api_client import (
    MultiLayerProtocol,
)

import streamlit as st
import plotly.express as px

from goodall.result_analysis.pair_evaluation import combine_FP, \
    add_threshold_dependent_type, add_ground_truth_label
from goodall.ui.components.datasets import replace_schema_strings
from goodall.ui.components.tag_analyzer import TagAnalyzer, group_by_tag, \
    filter_dataframe
from goodall.ui.constants import linkTypeColorMap
from goodall.utils.constants import ATTRIBUTES_FOR_DISPLAY


class ProtocolTagAnalyzer(TagAnalyzer):
    def __init__(self, protocol: MultiLayerProtocol | None = None,
                 df_tags: pd.DataFrame | None = None,
                 df_tags_2: pd.DataFrame | None = None,
                 ref_thr: float | None = None,
                 ref_thr_2: float | None = None,
                 ):
        super().__init__(df_tags)
        self.protocol = protocol
        self.ref_thr = ref_thr
        self.df_tags_2 = df_tags_2
        self.ref_thr_2 = ref_thr_2

    def compute_linkage_quality(
        self,
    ):
        pass

    def analyze(self):
        # df_pairs = self.get_record_pairs()
        # st.dataframe(df_pairs)
        save_dataframe_option(self.df_tags, "tags")
        super().analyze()

        if self.simulate_missing_gt:
            type_order = ["MATCH", "NON-MATCH"]
        else:
            type_order = ["TP", "FP", "FN", "TN"]
        df_tags_fp, df_pair_tags = self.add_eval_type_to_tags(self.df_tags)
        if self.df_tags_2 is not None:
            df_tags_fp_2, df_pair_tags_2 = self.add_eval_type_to_tags(self.df_tags_2)

        with st.expander("Diff schema", expanded=True):
            st.subheader("by diff schema tag")
            def prepare_df_schema(df_pair_tags: pd.DataFrame,
                                  df_tags_fp: pd.DataFrame,
                                  ref_thr: float | None):
                df_schema = filter_dataframe(df_pair_tags, {"tag": "PLAIN_DIFF_SCHEMA"})
                df_schema.rename(columns=lambda col: col.replace("tagString", "Schema"), inplace=True)
                replace_schema_strings(df_schema, attributes_to_keep=ATTRIBUTES_FOR_DISPLAY)
                df_schema.rename(columns=lambda col: col.replace("Schema", "tagString"), inplace=True)
                df_schema = add_similarity_column(df_schema, df_tags_fp)
                if ref_thr:
                    st.info(f"Updating eval types using threshold {ref_thr}")
                    df_schema = get_eval_type_based_on_thr(df_schema, ref_thr)
                st.dataframe(df_schema)
                return df_schema

            df_schema = prepare_df_schema(df_pair_tags, df_tags_fp, self.ref_thr)
            if self.df_tags_2 is not None:
                df_schema_2 = prepare_df_schema(df_pair_tags_2, df_tags_fp_2, self.ref_thr_2)

            st.dataframe(group_pair_tags(df_schema, ["Eval-Type"]))
            df_schema = df_schema[df_schema["Eval-Type"] != "TN"]
            df_schema = df_schema[df_schema["Eval-Type"] != "TP"]

            grouped = group_pair_tags(df_schema, ["tagString", "Eval-Type"])
            # grouped = df_schema.groupby(by=["tagString", "Eval-Type"]).size().rename("count")
            grouped = (
                grouped
                .reset_index()
                .sort_values(["count", "tagString", "Eval-Type"],
                             ascending=[False, True, True])
            )
            st.dataframe(grouped)

        with st.expander("Similarity Histogram", expanded=True):
            st.subheader("by modifier tag")

            boxplot_barmode = st.sidebar.selectbox("Boxplot barmode",
                                                   ["group", "stack"], index = 1)
            def prepare_df_schema(df_pair_tags: pd.DataFrame,
                                  df_tags_fp: pd.DataFrame):
                df_modifier = filter_dataframe(df_pair_tags, {"tag": "Modifier"})
                df_tag_with_sim = add_similarity_column(df_modifier, df_tags_fp)
                df_tag_with_sim = df_tag_with_sim[
                    ~df_tag_with_sim["similarity"].isnull()
                ]
                st.dataframe(df_tag_with_sim)
                group_by_tag(df_tag_with_sim, ["tagString"])

                grouped = group_pair_tags(df_tag_with_sim, ["tagString", "Eval-Type"])
                st.dataframe(grouped)
                return df_tag_with_sim

            df_tag_with_sim = prepare_df_schema(df_pair_tags, df_tags_fp)
            save_dataframe_option(df_tag_with_sim, "tag_with_sim")
            if self.df_tags_2 is not None:
                df_tag_with_sim_2 = prepare_df_schema(df_pair_tags_2, df_tags_fp_2)
                df_out = (
                    df_tag_with_sim_2
                    .merge(
                        df_tag_with_sim[["ID0", "ID1", "similarity"]],
                        on=["ID0", "ID1"],
                        how="left",
                        suffixes=("", "_ref")
                    )
                )

                df_out["similarity_diff"] = (
                        df_out["similarity"] - df_out["similarity_ref"]
                )
                st.dataframe(df_out)
                save_dataframe_option(df_out, "tag_with_sim_2")
                fig = px.histogram(
                    df_out, x="similarity_diff", color="tagString",
                    barmode=boxplot_barmode
                )
                fig.update_layout(bargap=0)
                st.plotly_chart(fig)
                fig = px.histogram(
                    df_out, x="similarity", color="tagString",
                    barmode=boxplot_barmode
                )
                fig.update_layout(bargap=0)
                st.plotly_chart(fig)

            fig = px.histogram(
                df_tag_with_sim, x="similarity", color="tagString", barmode=boxplot_barmode
            )
            fig.update_layout(bargap=0)
            st.plotly_chart(fig)

        with st.expander("FILLRATE", expanded=False):
            st.subheader("by FILLRATE")
            # st.dataframe(merged_df[merged_df["tag"] == "FILLRATE"])
            df_fillrate = filter_dataframe(df_pair_tags, {"tag": ["FILLRATE"]})
            st.dataframe(df_fillrate)
            y_col_name = "Bloom Filter fillratio"
            df_fillrate.rename(columns={"tagNumeric": y_col_name}, inplace=True)
            st.plotly_chart(
                px.box(
                    df_fillrate,
                    x="tag",
                    y=y_col_name,
                    color="Eval-Type",
                    color_discrete_map=linkTypeColorMap,
                    category_orders={"Eval-Type": type_order},
                )
            )

        with st.expander("FREQ_POS_REL", expanded=False):
            st.subheader("by FREQ_POS_REL")
            df_freq = filter_dataframe(df_pair_tags, {"tag": ["FREQ_POS_REL"]})
            st.text(
                f"Number of records with type with freq info: "
                f"{len(pd.unique(df_freq['ID0']))}"
            )
            st.dataframe(df_freq)
            group_by_tag(
                df_freq[df_freq["attribute"] == "FIRSTNAME"], ["Eval-Type"]
            )
            df_freq_no_type = filter_dataframe(
                df_tags_fp, {"tag": ["FREQ_POS_REL"]}
            )
            st.text(
                f"Number of records with freq info: "
                f"{len(pd.unique(df_freq_no_type['ID0']))}"
            )
            st.dataframe(df_freq_no_type)
            y_col_name = "Rel. frequency rank (high=rare)"
            df_freq.rename(columns={"tagNumeric": y_col_name}, inplace=True)
            st.plotly_chart(
                px.box(
                    df_freq,
                    x="attribute",
                    y=y_col_name,
                    color="Eval-Type",
                    color_discrete_map=linkTypeColorMap,
                    category_orders={
                        "Eval-Type": type_order,
                        "attribute": ["FIRSTNAME", "LASTNAME", "CITY"],
                    },
                )
            )
            st.plotly_chart(
                px.box(
                    df_freq,
                    x="Eval-Type",
                    y=y_col_name,
                    color="attribute",
                    color_discrete_map=linkTypeColorMap,
                    category_orders={
                        "Eval-Type": type_order,
                        "attribute": ["FIRSTNAME", "LASTNAME", "CITY"],
                    },
                )
            )

        # with st.expander("HOUSEHOLD", expanded=False):
        #     st.subheader("by HOUSEHOLD-TYPE")
        #     df_household = self.filter_dataframe(merged_df, {"tag": ["HOUSEHOLD-TYPE"]})
        #     # st.dataframe(df_household)
        #     # group_by_tag(df_household, ["tagString"])
        #     df_hh_by_type = group_by_tag(df_household, ["tagString", "Eval-Type"])
        #     df_hh_by_type["share"] = df_hh_by_type["count"] / df_hh_by_type.groupby(
        #         "tagString"
        #     )["count"].transform("sum")
        #     # st.dataframe(df_hh_by_type)
        #     # st.dataframe(self.filter_dataframe(df_tags_fp,
        #     #                                    {"tag": ["HOUSEHOLD-TYPE"]}))
        #     x_col_name = "Household type"
        #     df_hh_by_type.rename(columns={"tagString": x_col_name}, inplace=True)
        #     st.plotly_chart(
        #         px.bar(
        #             df_hh_by_type,
        #             x="Eval-Type",
        #             y="share",
        #             color=x_col_name,
        #             color_discrete_map=linkTypeColorMap,
        #             category_orders={"Eval-Type": type_order},
        #             barmode="group",
        #         )
        #     )
        #     st.plotly_chart(
        #         px.bar(
        #             df_hh_by_type,
        #             x=x_col_name,
        #             y="share",
        #             color="Eval-Type",
        #             color_discrete_map=linkTypeColorMap,
        #             category_orders={"Eval-Type": type_order},
        #             barmode="group",
        #         )
        #     )

        st.text("the end...")



    def add_eval_type_to_tags(self, df_tags: pd.DataFrame) -> tuple[DataFrame, DataFrame]:
        df_tags_fp = combine_FP(df_tags, column_names=["tagString"])
        if self.simulate_missing_gt:
            df_tags_fp = self.get_with_missing_gt(df_tags_fp)
        df_gt_types = filter_dataframe(df_tags_fp, {"tag": "type"})[
            ["ID0", "ID1", "tagString"]
        ]
        # st.dataframe(df_gt_types)
        df_gt_types = df_gt_types.rename(columns={"tagString": "Eval-Type"})
        # unique_ids = pd.unique(df_gt_types[["ID0", "ID1"]].values.ravel())
        # st.text(f"#Unique IDs: {len(unique_ids)}")
        # st.dataframe(unique_ids)

        # st.dataframe(df_tags_fp[df_tags_fp["tag"] == "PLAIN_DIFF_SCHEMA"])
        # st.text(len(df_tags_fp[df_tags_fp["tag"] == "PLAIN_DIFF_SCHEMA"]))
        # st.dataframe(df_tags_fp[df_tags_fp["tag"] == "FILLRATE"])

        # merged_df_id0_only = merge_type(df_tags_fp, df_gt_types, unique_ids, "ID0")
        # merged_df_id1_only = merge_type(df_tags_fp, df_gt_types, unique_ids, "ID1")
        merged_pairs = merge_type_both(df_tags_fp, df_gt_types)
        # st.dataframe(merged_pairs[merged_pairs["tag"] == "PLAIN_DIFF_SCHEMA"])

        # st.dataframe(merged_pairs)
        # st.dataframe(merged_df_id1_only[merged_df_id1_only["tag"] == "FILLRATE"])
        # merged_df = pd.concat(
        #     [merged_df_id0_only, merged_df_id1_only, merged_pairs], axis=0
        # )
        # st.text(f"length: id0_only={len(merged_df_id0_only)}"
        #         f" id1_only={len(merged_df_id1_only)}"
        #         f" both={len(merged_pairs)}"
        #         f" merged={len(merged_df)}")
        merged_df = merged_pairs
        st.dataframe(merged_df)
        return df_tags_fp, merged_df


def save_dataframe_option(df: pd.DataFrame, name: str):
    # if st.button(f"Save dataframe {name}", key=str(uuid.uuid4())):
    if st.button(f"Save dataframe {name}"):
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"df_{name}_{timestamp}.csv"
        df.to_csv(filename, index=False)
        st.success(f"Saved to {filename}")

def add_similarity_column( df_modifier: DataFrame, df_tags: DataFrame) -> DataFrame:
    df_sim = df_tags[df_tags["tag"] == "SIMILARITY"][
        ["ID0", "ID1", "tagNumeric"]
    ]
    df_sim.rename(columns={"tagNumeric": "similarity"}, inplace=True)
    # st.dataframe(df_sim)
    df_tag_with_sim = df_modifier.merge(df_sim, on=["ID0", "ID1"], how="left")
    return df_tag_with_sim


def group_pair_tags(df: pd.DataFrame, by: list) -> pd.DataFrame:
    grouped = (
        df
        .groupby(by)
        .agg(
            count=("similarity", "size"),
            mean=("similarity", "mean"),
            min=("similarity", "min"),
            max=("similarity", "max"),
        )
    )
    return grouped
    # return df.groupby(by=by).size().rename("count")


def get_eval_type_based_on_thr(df_tags_with_sim: pd.DataFrame, thr: float) -> pd.DataFrame:
    df_eval_type_gt = add_ground_truth_label(df_tags_with_sim[["similarity", "Eval-Type"]])

    col_eval_type = "Eval-Type"
    df_out = add_threshold_dependent_type(df_eval_type_gt, thr, col_type=col_eval_type)
    df_tags_with_sim[col_eval_type] = df_out[col_eval_type]
    # st.dataframe(df_tags_with_sim)
    return df_tags_with_sim

def merge_type(df_tags_fp: pd.DataFrame, df_gt_types: pd.DataFrame, unique_ids, id_column: str):
    other_id_column = "ID0" if id_column == "ID1" else "ID1"
    # filtered_df = df_tags_fp[
    #     df_tags_fp["ID0"].isin(unique_ids) & (df_tags_fp["ID1"] == "")
    # ]
    # if id_column == 'ID0':
    #     filtered_df = df_tags_fp[df_tags_fp[id_column].isin(unique_ids)
    #                              & (df_tags_fp[other_id_column].isna())]
    # else:
        # filtered_df = df_tags_fp[df_tags_fp[id_column].isin(unique_ids)
        #                      & ~df_tags_fp[other_id_column].isin(unique_ids)]
    #     filtered_df = df_tags_fp[df_tags_fp['ID0'].isin(unique_ids)]
    # filtered_df = df_tags_fp[df_tags_fp[id_column].isin(unique_ids)
    #                          | df_tags_fp[other_id_column].isin(unique_ids)]
    filtered_df = df_tags_fp[df_tags_fp[id_column].isin(unique_ids)
                             & df_tags_fp[other_id_column].isna()]
    st.text(f"#filtered_df by id column: {len(filtered_df)}")
    filtered_df = filtered_df[~(filtered_df["tag"] == "type")]
    # st.text(f"#filtered_df by {id_column}: {len(filtered_df)}")
    # st.dataframe(filtered_df)
    merged_df = filtered_df.merge(
        df_gt_types[[id_column, "Eval-Type"]],
        left_on="ID0",
        right_on=id_column,
        how="right",
        suffixes=(
            "",
            "_drop",
        ),  # Avoid _x and _y, mark right-side column for deletion
    )
    merged_df = merged_df.drop(columns=[f"{id_column}_drop"], errors="ignore")
    merged_df["Eval-Type"] = merged_df["Eval-Type"].fillna("TN")
    st.text(f"#merged_df by {id_column}: {len(merged_df)}")
    # st.dataframe(merged_df)
    return merged_df

def merge_type_both(df_tags_fp: pd.DataFrame, df_gt_types:pd.DataFrame):
    # st.text(f"#df_tags_fp {len(df_tags_fp)}")
    # st.text(f"#df_gt_types {len(df_gt_types)}")
    # filtered_df = df_tags_fp[
    #     ~(df_tags_fp["ID0"] == "") & ~(df_tags_fp["ID1"] == "")
    # ]
    filtered_df = df_tags_fp[
        df_tags_fp["ID0"].notna() & df_tags_fp["ID1"].notna() &
        (df_tags_fp["ID0"] != "") & (df_tags_fp["ID1"] != "")
        ]
    # filtered_df = filtered_df[filtered_df["tag"] == "PLAIN_DIFF_SCHEMA"]

    # st.text(len(filtered_df[filtered_df["tag"] == "PLAIN_DIFF_SCHEMA"]))
    # st.text(f"#filtered_df by both id columns: {len(filtered_df)}")
    filtered_df = filtered_df[~(filtered_df["tag"] == "type")]
    # st.text(len(filtered_df[filtered_df["tag"] == "PLAIN_DIFF_SCHEMA"]))
    # st.text(f"#filtered_df by both id columns: {len(filtered_df)}")
    # st.dataframe(filtered_df.sort_values(by=["ID0", "ID1"]))
    # st.dataframe(df_gt_types.sort_values(by=["ID0", "ID1"]))

    # st.text(filtered_df[["ID0", "ID1"]].dtypes)
    # st.text(df_gt_types[["ID0", "ID1"]].dtypes)
    # for df in (filtered_df, df_gt_types):
    #     df["ID0"] = df["ID0"].astype(str).str.strip()
    #     df["ID1"] = df["ID1"].astype(str).str.strip()

    merged_df = filtered_df.merge(
        df_gt_types[["ID0", "ID1", "Eval-Type"]], on=["ID0", "ID1"], how="left"
    )
    # st.dataframe(merged_df.sort_values(by=["ID0", "ID1"]))
    merged_df["Eval-Type"] = merged_df["Eval-Type"].fillna("TN")
    # st.text(f"#merged_df by both id columns: {len(merged_df)}")
    # st.dataframe(merged_df)
    return merged_df