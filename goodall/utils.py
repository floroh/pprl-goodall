from typing import Dict, Any

import numpy as np


def range_include_right(
    first: float, last: float, step: float, digits: int = 2
) -> list:
    values = list(np.arange(first, last + step / 2, step))
    values = [round(values, digits) for values in values]
    return values


def downsampling_if_possible(df, max_size: int = 10000):
    if df.shape[0] > max_size:
        return df.sample(n=max_size)
    return df


def flatten_dict(d: Dict[str, Any], parent_key: str = '', sep: str = '.') -> Dict[
    str, Any]:
    """
    Recursively flattens a nested dictionary.

    Args:
        d (Dict[str, Any]): The dictionary to flatten.
        parent_key (str): The base key to prepend to flattened keys.
        sep (str): The separator to use between parent and child keys.

    Returns:
        Dict[str, Any]: The flattened dictionary.
    """
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep).items())
        else:
            items.append((new_key, v))
    return dict(items)