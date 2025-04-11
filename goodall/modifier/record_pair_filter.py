from typing import List

import pandas as pd


def filter_pairs(df_record_pairs: pd.DataFrame,
                 pair_filters: List[str] = [],
                 pair_remove_filters: List[str] = []) -> pd.DataFrame:
    if len(pair_filters) != 0:
        for pairFilter in pair_filters:
            df_record_pairs = df_record_pairs[
                df_record_pairs["properties"].apply(
                    lambda props: pairFilter in props
                    if isinstance(props, list)
                    else [props == pairFilter]
                )
            ]
    if len(pair_remove_filters) != 0:
        for pairRemoveFilter in pair_remove_filters:
            df_record_pairs = df_record_pairs[
                df_record_pairs["properties"].apply(
                    lambda props: pairRemoveFilter not in props
                    if isinstance(props, list)
                    else [props != pairRemoveFilter]
                )
            ]
    return df_record_pairs