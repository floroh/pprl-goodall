# MatchingDto

Description of a matching scheme

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | [**MatcherIdDto**](MatcherIdDto.md) |  | [optional] 
**validation** | [**RecordRequirementsDto**](RecordRequirementsDto.md) |  | [optional] 
**config** | **str** | Configuration / parameters to build the matcher | [optional] 
**classifier_description** | **str** | Description of the classifier | [optional] 

## Example

```python
from pprl_linkage_unit_service_api_client.models.matching_dto import MatchingDto

# TODO update the JSON string below
json = "{}"
# create an instance of MatchingDto from a JSON string
matching_dto_instance = MatchingDto.from_json(json)
# print the JSON string representation of the object
print(MatchingDto.to_json())

# convert the object into a dict
matching_dto_dict = matching_dto_instance.to_dict()
# create an instance of MatchingDto from a dict
matching_dto_from_dict = MatchingDto.from_dict(matching_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


