# AnalysisRequestDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dataset_id** | **int** |  | [optional] 
**project_id** | **str** |  | [optional] 
**type** | **str** |  | [optional] 
**parameters** | **Dict[str, str]** |  | [optional] 

## Example

```python
from pprl_data_owner_service_api_client.models.analysis_request_dto import AnalysisRequestDto

# TODO update the JSON string below
json = "{}"
# create an instance of AnalysisRequestDto from a JSON string
analysis_request_dto_instance = AnalysisRequestDto.from_json(json)
# print the JSON string representation of the object
print(AnalysisRequestDto.to_json())

# convert the object into a dict
analysis_request_dto_dict = analysis_request_dto_instance.to_dict()
# create an instance of AnalysisRequestDto from a dict
analysis_request_dto_from_dict = AnalysisRequestDto.from_dict(analysis_request_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


