import json
from pathlib import Path
from typing import Any

import numpy as np


def _load_json_file(path: str | Path) -> Any:
    p = Path(path)
    with p.open("r", encoding="utf-8") as f:
        return json.loads(f.read())


def _handle_ranges(values):
    """
    If `values` is a list/tuple that represents range arguments (start, stop[, step]),
    return a list of values from range(...).
    Ensures float precision is at least .2f, or higher if input precision is higher.
    """
    if isinstance(values, (list, tuple)):
        try:
            # Compute precision: max number of decimal places in the inputs
            precisions = []
            for v in values:
                if isinstance(v, float):
                    s = str(v)
                    if "." in s:
                        precisions.append(len(s.split(".")[-1]))
            precision = max(max(precisions, default=2), 2)  # at least 2 decimals

            # Create the range
            arr = np.arange(*values)

            # Round to the detected precision
            arr = np.round(arr, decimals=precision)

            return arr.tolist()

        except TypeError:
            # Not valid args for np.arange -> just return as-is
            return list(values)
    return [values]
