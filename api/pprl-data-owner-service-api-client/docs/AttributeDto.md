# AttributeDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | [optional] 
**value** | **str** |  | [optional] 

## Example

```python
from pprl_data_owner_service_api_client.models.attribute_dto import AttributeDto

# TODO update the JSON string below
json = "{}"
# create an instance of AttributeDto from a JSON string
attribute_dto_instance = AttributeDto.from_json(json)
# print the JSON string representation of the object
print(AttributeDto.to_json())

# convert the object into a dict
attribute_dto_dict = attribute_dto_instance.to_dict()
# create an instance of AttributeDto from a dict
attribute_dto_from_dict = AttributeDto.from_dict(attribute_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


