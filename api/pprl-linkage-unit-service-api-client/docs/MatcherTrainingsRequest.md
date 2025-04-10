# MatcherTrainingsRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**matcher_id** | [**MatcherIdDto**](MatcherIdDto.md) |  | [optional] 
**dataset_id** | **int** |  | [optional] 
**min_similarity** | **float** |  | [optional] 
**max_similarity** | **float** |  | [optional] 

## Example

```python
from pprl_linkage_unit_service_api_client.models.matcher_trainings_request import MatcherTrainingsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of MatcherTrainingsRequest from a JSON string
matcher_trainings_request_instance = MatcherTrainingsRequest.from_json(json)
# print the JSON string representation of the object
print(MatcherTrainingsRequest.to_json())

# convert the object into a dict
matcher_trainings_request_dict = matcher_trainings_request_instance.to_dict()
# create an instance of MatcherTrainingsRequest from a dict
matcher_trainings_request_from_dict = MatcherTrainingsRequest.from_dict(matcher_trainings_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


