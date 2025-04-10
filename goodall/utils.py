from typing import Dict, Any


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
