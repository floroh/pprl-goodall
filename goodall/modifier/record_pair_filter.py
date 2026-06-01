from typing import List

import pandas as pd


def filter_pairs(
    df_record_pairs: pd.DataFrame,
    pair_filters: List[str] = [],
    pair_remove_filters: List[str] = [],
    match_all: bool = True,
) -> pd.DataFrame:
    # Ensure 'properties' is always a list
    def ensure_list(props):
        return props if isinstance(props, list) else [props]

    # Apply inclusion filters
    if pair_filters:
        if match_all:
            df_record_pairs = df_record_pairs[
                df_record_pairs["properties"].apply(
                    lambda props: all(f in ensure_list(props) for f in pair_filters)
                )
            ]
        else:
            df_record_pairs = df_record_pairs[
                df_record_pairs["properties"].apply(
                    lambda props: any(f in ensure_list(props) for f in pair_filters)
                )
            ]

    # Apply exclusion filters
    if pair_remove_filters:
        if match_all:
            df_record_pairs = df_record_pairs[
                df_record_pairs["properties"].apply(
                    lambda props: all(
                        f not in ensure_list(props) for f in pair_remove_filters
                    )
                )
            ]
        else:
            df_record_pairs = df_record_pairs[
                df_record_pairs["properties"].apply(
                    lambda props: any(
                        f not in ensure_list(props) for f in pair_remove_filters
                    )
                )
            ]

    return df_record_pairs
