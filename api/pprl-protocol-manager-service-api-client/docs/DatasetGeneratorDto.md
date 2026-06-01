# DatasetGeneratorDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dataset_id** | **int** |  | [optional] 
**dataset_name** | **str** |  | [optional] 
**germany_generator_config** | [**GermanyGeneratorConfig**](GermanyGeneratorConfig.md) |  | [optional] 
**usvr_selection_config** | [**UsvrSelectionConfig**](UsvrSelectionConfig.md) |  | [optional] 

## Example

```python
from pprl_protocol_manager_service_api_client.models.dataset_generator_dto import DatasetGeneratorDto

# TODO update the JSON string below
json = "{}"
# create an instance of DatasetGeneratorDto from a JSON string
dataset_generator_dto_instance = DatasetGeneratorDto.from_json(json)
# print the JSON string representation of the object
print(DatasetGeneratorDto.to_json())

# convert the object into a dict
dataset_generator_dto_dict = dataset_generator_dto_instance.to_dict()
# create an instance of DatasetGeneratorDto from a dict
dataset_generator_dto_from_dict = DatasetGeneratorDto.from_dict(dataset_generator_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


