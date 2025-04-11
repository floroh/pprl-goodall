# RecordIdPairDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**left_record_id** | [**RecordIdDto**](RecordIdDto.md) |  | [optional] 
**right_record_id** | [**RecordIdDto**](RecordIdDto.md) |  | [optional] 
**label** | **str** |  | [optional] 

## Example

```python
from pprl_linkage_unit_service_api_client.models.record_id_pair_dto import RecordIdPairDto

# TODO update the JSON string below
json = "{}"
# create an instance of RecordIdPairDto from a JSON string
record_id_pair_dto_instance = RecordIdPairDto.from_json(json)
# print the JSON string representation of the object
print(RecordIdPairDto.to_json())

# convert the object into a dict
record_id_pair_dto_dict = record_id_pair_dto_instance.to_dict()
# create an instance of RecordIdPairDto from a dict
record_id_pair_dto_from_dict = RecordIdPairDto.from_dict(record_id_pair_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


