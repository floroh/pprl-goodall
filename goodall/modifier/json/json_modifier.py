import json

from jsonpath_ng import parse


def full_class_selector(parent: str, full_class_name) -> str:
    return parent + "[?(@.@class=='" + full_class_name + "')]"


def class_selector(parent: str, class_name) -> str:
    return full_class_selector(parent, "." + class_name)


def update(json_string: str, json_path: str, new_value) -> str:
    obj = json.loads(json_string)
    jsonpath_expr = parse(json_path)
    # jsonpath_expr.find(obj)
    jsonpath_expr.update(obj, new_value)
    return json.dumps(obj)
