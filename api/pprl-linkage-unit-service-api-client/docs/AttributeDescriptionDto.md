# AttributeDescriptionDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**display_name** | **str** |  | [optional] 
**required** | **bool** |  | [optional] 
**validations** | **List[str]** |  | [optional] 

## Example

```python
from pprl_linkage_unit_service_api_client.models.attribute_description_dto import AttributeDescriptionDto

# TODO update the JSON string below
json = "{}"
# create an instance of AttributeDescriptionDto from a JSON string
attribute_description_dto_instance = AttributeDescriptionDto.from_json(json)
# print the JSON string representation of the object
print(AttributeDescriptionDto.to_json())

# convert the object into a dict
attribute_description_dto_dict = attribute_description_dto_instance.to_dict()
# create an instance of AttributeDescriptionDto from a dict
attribute_description_dto_from_dict = AttributeDescriptionDto.from_dict(attribute_description_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


