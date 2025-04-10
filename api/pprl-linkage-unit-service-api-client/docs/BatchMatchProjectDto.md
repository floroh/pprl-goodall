# BatchMatchProjectDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**project_id** | **str** |  | [optional] 
**last_update** | **str** |  | [optional] 
**method** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**dataset_id** | **int** |  | [optional] 
**interactive** | **bool** |  | [optional] 
**configs** | **Dict[str, str]** |  | [optional] 
**current_state** | **str** |  | [optional] 
**phases** | [**Dict[str, BatchMatchProjectPhase]**](BatchMatchProjectPhase.md) |  | [optional] 

## Example

```python
from pprl_linkage_unit_service_api_client.models.batch_match_project_dto import BatchMatchProjectDto

# TODO update the JSON string below
json = "{}"
# create an instance of BatchMatchProjectDto from a JSON string
batch_match_project_dto_instance = BatchMatchProjectDto.from_json(json)
# print the JSON string representation of the object
print(BatchMatchProjectDto.to_json())

# convert the object into a dict
batch_match_project_dto_dict = batch_match_project_dto_instance.to_dict()
# create an instance of BatchMatchProjectDto from a dict
batch_match_project_dto_from_dict = BatchMatchProjectDto.from_dict(batch_match_project_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


