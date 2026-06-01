# MatchingCreationRequestDto

Request for creating a matching definition.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**weight_selection_method** | **str** |  | [optional] 
**matching_creation_method** | **str** |  | [optional] 
**base_matcher_id** | [**MatcherIdDto**](MatcherIdDto.md) |  | [optional] 
**output_matcher_id** | [**MatcherIdDto**](MatcherIdDto.md) |  | [optional] 
**attribute_weights** | **Dict[str, float]** |  | [optional] 
**attribute_m_weights** | **Dict[str, float]** |  | [optional] 
**attribute_u_weights** | **Dict[str, float]** |  | [optional] 
**dataset_id** | **int** |  | [optional] 
**persist** | **bool** |  | [optional] 

## Example

```python
from pprl_linkage_unit_service_api_client.models.matching_creation_request_dto import MatchingCreationRequestDto

# TODO update the JSON string below
json = "{}"
# create an instance of MatchingCreationRequestDto from a JSON string
matching_creation_request_dto_instance = MatchingCreationRequestDto.from_json(json)
# print the JSON string representation of the object
print(MatchingCreationRequestDto.to_json())

# convert the object into a dict
matching_creation_request_dto_dict = matching_creation_request_dto_instance.to_dict()
# create an instance of MatchingCreationRequestDto from a dict
matching_creation_request_dto_from_dict = MatchingCreationRequestDto.from_dict(matching_creation_request_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


