# MatcherUpdateRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**project_id** | **str** |  | [optional] 
**type** | **str** |  | [optional] 

## Example

```python
from pprl_linkage_unit_service_api_client.models.matcher_update_request import MatcherUpdateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of MatcherUpdateRequest from a JSON string
matcher_update_request_instance = MatcherUpdateRequest.from_json(json)
# print the JSON string representation of the object
print(MatcherUpdateRequest.to_json())

# convert the object into a dict
matcher_update_request_dict = matcher_update_request_instance.to_dict()
# create an instance of MatcherUpdateRequest from a dict
matcher_update_request_from_dict = MatcherUpdateRequest.from_dict(matcher_update_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


