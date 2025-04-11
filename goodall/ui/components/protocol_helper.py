import json

from goodall.api_helper import lu_api


def get_current_classifier_threshold(layer):
    classifier_config = lu_api.get_config(
        lu_api.get_project(layer.project_id).method).config
    classifier = json.loads(classifier_config)["linker"][
        "classifier"]
    current_threshold = classifier['threshold']
    return current_threshold

def update_classifier_threshold(layer, new_threshold: float):
    matching_dto = lu_api.get_config(lu_api.get_project(layer.project_id).method)
    classifier = json.loads(matching_dto.config)
    classifier["linker"]["classifier"]['threshold'] = new_threshold
    matching_dto.config = json.dumps(classifier)
    lu_api.update_config(matching_dto)
