# TaggedDatasetDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dataset_id** | **int** |  | [optional] 
**records** | [**List[RecordDto]**](RecordDto.md) |  | [optional] 
**tags** | [**List[Tag]**](Tag.md) |  | [optional] 

## Example

```python
from pprl_data_generator_service_api_client.models.tagged_dataset_dto import TaggedDatasetDto

# TODO update the JSON string below
json = "{}"
# create an instance of TaggedDatasetDto from a JSON string
tagged_dataset_dto_instance = TaggedDatasetDto.from_json(json)
# print the JSON string representation of the object
print(TaggedDatasetDto.to_json())

# convert the object into a dict
tagged_dataset_dto_dict = tagged_dataset_dto_instance.to_dict()
# create an instance of TaggedDatasetDto from a dict
tagged_dataset_dto_from_dict = TaggedDatasetDto.from_dict(tagged_dataset_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


