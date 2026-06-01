# RecordPairWithRecordsDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**record0** | [**RecordDto**](RecordDto.md) |  | [optional] 
**record1** | [**RecordDto**](RecordDto.md) |  | [optional] 
**project_id** | **str** |  | [optional] 
**match_grade** | **str** |  | [optional] 
**similarity** | **float** |  | [optional] 
**properties** | **List[str]** |  | [optional] 
**attribute_similarities** | **Dict[str, float]** |  | [optional] 
**tags** | [**List[Tag]**](Tag.md) |  | [optional] 

## Example

```python
from pprl_linkage_unit_service_api_client.models.record_pair_with_records_dto import RecordPairWithRecordsDto

# TODO update the JSON string below
json = "{}"
# create an instance of RecordPairWithRecordsDto from a JSON string
record_pair_with_records_dto_instance = RecordPairWithRecordsDto.from_json(json)
# print the JSON string representation of the object
print(RecordPairWithRecordsDto.to_json())

# convert the object into a dict
record_pair_with_records_dto_dict = record_pair_with_records_dto_instance.to_dict()
# create an instance of RecordPairWithRecordsDto from a dict
record_pair_with_records_dto_from_dict = RecordPairWithRecordsDto.from_dict(record_pair_with_records_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


