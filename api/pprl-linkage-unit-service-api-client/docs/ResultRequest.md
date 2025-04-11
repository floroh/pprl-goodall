# ResultRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**project_id** | **str** |  | [optional] 
**pair_properties** | **List[str]** |  | [optional] 

## Example

```python
from pprl_linkage_unit_service_api_client.models.result_request import ResultRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ResultRequest from a JSON string
result_request_instance = ResultRequest.from_json(json)
# print the JSON string representation of the object
print(ResultRequest.to_json())

# convert the object into a dict
result_request_dict = result_request_instance.to_dict()
# create an instance of ResultRequest from a dict
result_request_from_dict = ResultRequest.from_dict(result_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


