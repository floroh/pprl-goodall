# RecordRequirementsDto

Description of requirements for this scheme

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**method** | **str** |  | [optional] 
**supported_encoding_methods** | **List[str]** | List of encoding methods that can be matched with this scheme | [optional] 
**attributes** | [**List[AttributeDescriptionDto]**](AttributeDescriptionDto.md) |  | [optional] 

## Example

```python
from pprl_linkage_unit_service_api_client.models.record_requirements_dto import RecordRequirementsDto

# TODO update the JSON string below
json = "{}"
# create an instance of RecordRequirementsDto from a JSON string
record_requirements_dto_instance = RecordRequirementsDto.from_json(json)
# print the JSON string representation of the object
print(RecordRequirementsDto.to_json())

# convert the object into a dict
record_requirements_dto_dict = record_requirements_dto_instance.to_dict()
# create an instance of RecordRequirementsDto from a dict
record_requirements_dto_from_dict = RecordRequirementsDto.from_dict(record_requirements_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


