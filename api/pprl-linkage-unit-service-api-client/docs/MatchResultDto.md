# MatchResultDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**records** | [**List[RecordDto]**](RecordDto.md) |  | [optional] 
**record_ids** | [**List[RecordIdDto]**](RecordIdDto.md) |  | [optional] 
**record_pairs** | [**List[RecordPairDto]**](RecordPairDto.md) |  | [optional] 

## Example

```python
from pprl_linkage_unit_service_api_client.models.match_result_dto import MatchResultDto

# TODO update the JSON string below
json = "{}"
# create an instance of MatchResultDto from a JSON string
match_result_dto_instance = MatchResultDto.from_json(json)
# print the JSON string representation of the object
print(MatchResultDto.to_json())

# convert the object into a dict
match_result_dto_dict = match_result_dto_instance.to_dict()
# create an instance of MatchResultDto from a dict
match_result_dto_from_dict = MatchResultDto.from_dict(match_result_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


