# MatcherIdDto

ID of an matching scheme

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**method** | **str** | Name of the matching scheme | [optional] 
**project** | **str** | (Optional) Project name where this scheme is used | [optional] 

## Example

```python
from pprl_linkage_unit_service_api_client.models.matcher_id_dto import MatcherIdDto

# TODO update the JSON string below
json = "{}"
# create an instance of MatcherIdDto from a JSON string
matcher_id_dto_instance = MatcherIdDto.from_json(json)
# print the JSON string representation of the object
print(MatcherIdDto.to_json())

# convert the object into a dict
matcher_id_dto_dict = matcher_id_dto_instance.to_dict()
# create an instance of MatcherIdDto from a dict
matcher_id_dto_from_dict = MatcherIdDto.from_dict(matcher_id_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


