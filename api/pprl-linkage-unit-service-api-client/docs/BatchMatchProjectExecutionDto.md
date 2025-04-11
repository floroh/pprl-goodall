# BatchMatchProjectExecutionDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**project_id** | **str** |  | [optional] 
**from_state** | **str** |  | [optional] 
**to_state** | **str** |  | [optional] 

## Example

```python
from pprl_linkage_unit_service_api_client.models.batch_match_project_execution_dto import BatchMatchProjectExecutionDto

# TODO update the JSON string below
json = "{}"
# create an instance of BatchMatchProjectExecutionDto from a JSON string
batch_match_project_execution_dto_instance = BatchMatchProjectExecutionDto.from_json(json)
# print the JSON string representation of the object
print(BatchMatchProjectExecutionDto.to_json())

# convert the object into a dict
batch_match_project_execution_dto_dict = batch_match_project_execution_dto_instance.to_dict()
# create an instance of BatchMatchProjectExecutionDto from a dict
batch_match_project_execution_dto_from_dict = BatchMatchProjectExecutionDto.from_dict(batch_match_project_execution_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


