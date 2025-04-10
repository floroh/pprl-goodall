# RecordPairDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id0** | [**RecordIdDto**](RecordIdDto.md) |  | [optional] 
**id1** | [**RecordIdDto**](RecordIdDto.md) |  | [optional] 
**project_id** | **str** |  | [optional] 
**match_grade** | **str** |  | [optional] 
**similarity** | **float** |  | [optional] 
**properties** | **List[str]** |  | [optional] 
**attribute_similarities** | **Dict[str, float]** |  | [optional] 
**tags** | [**List[Tag]**](Tag.md) |  | [optional] 

## Example

```python
from pprl_linkage_unit_service_api_client.models.record_pair_dto import RecordPairDto

# TODO update the JSON string below
json = "{}"
# create an instance of RecordPairDto from a JSON string
record_pair_dto_instance = RecordPairDto.from_json(json)
# print the JSON string representation of the object
print(RecordPairDto.to_json())

# convert the object into a dict
record_pair_dto_dict = record_pair_dto_instance.to_dict()
# create an instance of RecordPairDto from a dict
record_pair_dto_from_dict = RecordPairDto.from_dict(record_pair_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


