# DatasetGenerationConfigCreatorDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**reference_dataset_id** | **int** | ID of the dataset whose records and attribute value (frequencies) are used as the source for generated records. If empty or 0, the input dataset will be used instead | [optional] 
**name** | **str** | Name of the dataset modification config | 
**override** | [**DataSetGeneratorConfig**](DataSetGeneratorConfig.md) | Configuration settings which override the generated config parameters | [optional] 

## Example

```python
from pprl_data_owner_service_api_client.models.dataset_generation_config_creator_dto import DatasetGenerationConfigCreatorDto

# TODO update the JSON string below
json = "{}"
# create an instance of DatasetGenerationConfigCreatorDto from a JSON string
dataset_generation_config_creator_dto_instance = DatasetGenerationConfigCreatorDto.from_json(json)
# print the JSON string representation of the object
print(DatasetGenerationConfigCreatorDto.to_json())

# convert the object into a dict
dataset_generation_config_creator_dto_dict = dataset_generation_config_creator_dto_instance.to_dict()
# create an instance of DatasetGenerationConfigCreatorDto from a dict
dataset_generation_config_creator_dto_from_dict = DatasetGenerationConfigCreatorDto.from_dict(dataset_generation_config_creator_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


