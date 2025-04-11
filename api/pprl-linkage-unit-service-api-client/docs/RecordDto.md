# RecordDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | [**RecordIdDto**](RecordIdDto.md) |  | [optional] 
**dataset_id** | **int** |  | [optional] 
**encoding_id** | [**EncodingIdDto**](EncodingIdDto.md) |  | [optional] 
**attributes** | [**Dict[str, AttributeDto]**](AttributeDto.md) |  | [optional] 

## Example

```python
from pprl_linkage_unit_service_api_client.models.record_dto import RecordDto

# TODO update the JSON string below
json = "{}"
# create an instance of RecordDto from a JSON string
record_dto_instance = RecordDto.from_json(json)
# print the JSON string representation of the object
print(RecordDto.to_json())

# convert the object into a dict
record_dto_dict = record_dto_instance.to_dict()
# create an instance of RecordDto from a dict
record_dto_from_dict = RecordDto.from_dict(record_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


