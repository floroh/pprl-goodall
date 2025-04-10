# DatasetDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dataset_id** | **int** |  | [optional] 
**plaintext_dataset_id** | **int** |  | [optional] 
**dataset_name** | **str** |  | [optional] 

## Example

```python
from pprl_linkage_unit_service_api_client.models.dataset_dto import DatasetDto

# TODO update the JSON string below
json = "{}"
# create an instance of DatasetDto from a JSON string
dataset_dto_instance = DatasetDto.from_json(json)
# print the JSON string representation of the object
print(DatasetDto.to_json())

# convert the object into a dict
dataset_dto_dict = dataset_dto_instance.to_dict()
# create an instance of DatasetDto from a dict
dataset_dto_from_dict = DatasetDto.from_dict(dataset_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


