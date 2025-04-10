# RecordIdDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**unique** | **str** |  | [optional] 
**source** | **str** |  | [optional] 
**local** | **str** |  | [optional] 
**var_global** | **str** |  | [optional] 
**blocks** | **List[str]** |  | [optional] 

## Example

```python
from pprl_linkage_unit_service_api_client.models.record_id_dto import RecordIdDto

# TODO update the JSON string below
json = "{}"
# create an instance of RecordIdDto from a JSON string
record_id_dto_instance = RecordIdDto.from_json(json)
# print the JSON string representation of the object
print(RecordIdDto.to_json())

# convert the object into a dict
record_id_dto_dict = record_id_dto_instance.to_dict()
# create an instance of RecordIdDto from a dict
record_id_dto_from_dict = RecordIdDto.from_dict(record_id_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


