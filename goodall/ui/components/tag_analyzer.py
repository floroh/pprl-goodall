from typing import List, Dict, Any

import pandas as pd

import streamlit as st

from goodall.result_analysis.pair_evaluation import combine_FP


class TagAnalyzer:
    def __init__(
        self, df_tags: pd.DataFrame | None = None
    ):
        self.df_tags = df_tags
        self.simulate_missing_gt = False

    def render_tags(self):
        df_tags = self.get_tag_dataframe()
        st.dataframe(df_tags)

    def get_tag_dataframe(self) -> pd.DataFrame:
        pass

    @staticmethod
    def get_with_missing_gt(df: pd.DataFrame) -> pd.DataFrame:
        replace_map = {
            "TP": "MATCH",
            "FP": "MATCH",
            "TN": "NON-MATCH",
            "FN": "NON-MATCH",
        }
        condition = df["tag"] == "type"
        df_copy = df.copy()
        df_copy.loc[condition, "tagString"] = (
            df_copy.loc[condition, "tagString"]
            .map(replace_map)
            .fillna(df_copy.loc[condition, "tagString"])
        )
        return df_copy

    @staticmethod
    def sort_id_columns(df: pd.DataFrame):
        # mask = df['ID1'].str.endswith('-A') & ~df['ID0'].str.endswith('-A')
        # # Swap ID0 and ID1 where the condition is True
        # df.loc[mask, ['ID0', 'ID1']] = df.loc[mask, ['ID1', 'ID0']].values
        def get_suffix(val):
            return val.rsplit("-", 1)[-1] if isinstance(val, str) and "-" in val else ""

        suffix_id0 = df["ID0"].apply(get_suffix)
        suffix_id1 = df["ID1"].apply(get_suffix)
        mask = (suffix_id1 < suffix_id0) & (df["ID1"] != "")
        df.loc[mask, ["ID0", "ID1"]] = df.loc[mask, ["ID1", "ID0"]].values
        return df

    def analyze(self):
        # df_pairs = self.get_record_pairs()
        # st.dataframe(df_pairs)
        st.text(f"Number of tags: {len(self.df_tags)}")
        # st.dataframe(self.df_tags)
        self.sort_id_columns(self.df_tags)
        st.dataframe(self.df_tags)
        st.text(f"Number of tags: {len(self.df_tags)}")

        with st.expander("Group counts", expanded=False):
            st.subheader("by representation and origin")
            group_by_tag(self.df_tags, ["Type", "Origin"])

            st.subheader("by tag")
            group_by_tag(self.df_tags, ["tag"])

            st.subheader("by Corrupter Modifier")
            group_by_tag(
                filter_dataframe(self.df_tags, {"tag": "Modifier"}), ["tagString"]
            )
            #
            st.subheader("by Corrupter Attribute Modifier")
            group_by_tag(
                filter_dataframe(self.df_tags, {"tag": "Attribute-Modifier"}),
                ["tagString"],
            )
            #
            st.subheader("by confusion matrix type")
            group_by_tag(
                filter_dataframe(self.df_tags, {"tag": "type"}), ["tagString"]
            )

            st.subheader("by confusion matrix type (fp combined)")
            df_tags_fp = combine_FP(self.df_tags, column_names=["tagString"])
            df_type_groups = group_by_tag(
                filter_dataframe(df_tags_fp, {"tag": "type"}), ["tagString"]
            )
            st.text(f"{df_type_groups['count'].sum()} evaluated pairs")
            # df_types = self.filter_dataframe(df_tags_fp,
            #                                  {"tagString": ["TP", "FP", "FN", "TN"]})
            # group_by_tag(df_types, ["tagString"])
            # st.text(len(df_types))
            # st.dataframe(df_types)


def filter_dataframe(
        df: pd.DataFrame, filters: Dict[str, Any]
) -> pd.DataFrame:
    """
    Filters the DataFrame based on multiple column values.

    :param df: The input DataFrame to be filtered.
    :param filters: A dictionary where keys are column names and
                    values are filter values (single or list).
    :return: A filtered DataFrame.
    """
    filtered_df = df.copy()
    for col, value in filters.items():
        if isinstance(value, list):
            filtered_df = filtered_df[filtered_df[col].isin(value)]
        # elif isinstance(value, float):
        #     filtered_df = filtered_df[filtered_df[col].is(value)]
        else:
            filtered_df = filtered_df[filtered_df[col] == value]

    return filtered_df


def group_by_tag(
        df_tags: pd.DataFrame, group_by_columns: List[str]
) -> pd.DataFrame:
    grouped_df = df_tags.groupby(group_by_columns).size().reset_index(name="count")
    st.dataframe(grouped_df)
    return grouped_df