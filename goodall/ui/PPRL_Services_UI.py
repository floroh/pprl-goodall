matchGradeColorMap = {
    "CERTAIN_MATCH": "green",
    "PROBABLE": "blue",
    "POSSIBLE_MATCH": "orange",
    "NON_MATCH": "red",
}

gtLabelColorMap = {"TRUE_MATCH": "green", "TRUE_NON_MATCH": "red"}

linkTypeColorMap = {
    "TP": "green",
    "TN": "blue",
    "FN": "red",
    "FP": "orange",
    "FPd": "orange",
    "Fpd": "yellow",
}

linkTypeOrder = {"TP": 0, "TN": 1, "FP": 2, "FN": 3}

# Session state keys
SELECTED_PROJECT_ID = "selected_project_id"
SELECTED_PROTOCOL_ID = "selected_protocol_id"
SELECTED_METHOD = "selected_method"
SELECTED_METHOD_DISPLAY = "selected_method_display"
COMBINE_FP = "combine_FP"
COMBINE_MATCHGRADES = "combine_match_grades"
FETCH_RECORD_PAIRS = "fetch_record_pairs"
MSAL_HISTORY_DATA = "msal_history_data"
NUMBER_OF_SHOW_PROJECTS = "number_of_show_projects"


def get_tag_value(tags, tag_name: str, numeric: bool = False):
    if tags is not None:
        for tag in tags:
            if tag["tag"] == tag_name:
                if numeric:
                    return tag["numericValue"]
                else:
                    return tag["stringValue"]
    return None


ATTRIBUTE_ORDER = ["FIRSTNAME", "MIDDLENAME", "LASTNAME", "CITY", "ZIP",
                 "YEAROFBIRTH", "PLACEOFBIRTH", "COUNTRY", "GENDER", "STREET"]

ATTRIBUTES_FOR_DISPLAY = ["FIRSTNAME", "MIDDLENAME", "LASTNAME", "CITY", "ZIP",
                 "YEAROFBIRTH", "PLACEOFBIRTH"]
