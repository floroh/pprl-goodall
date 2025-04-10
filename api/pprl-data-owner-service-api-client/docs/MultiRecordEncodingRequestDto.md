# MultiRecordEncodingRequestDto

Request for encoding multiple records using the same method. The records are included in the request.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**encoding_id** | [**EncodingIdDto**](EncodingIdDto.md) |  | [optional] 
**records** | [**List[RecordDto]**](RecordDto.md) |  | [optional] 

## Example

```python
from pprl_data_owner_service_api_client.models.multi_record_encoding_request_dto import MultiRecordEncodingRequestDto

# TODO update the JSON string below
json = "{}"
# create an instance of MultiRecordEncodingRequestDto from a JSON string
multi_record_encoding_request_dto_instance = MultiRecordEncodingRequestDto.from_json(json)
# print the JSON string representation of the object
print(MultiRecordEncodingRequestDto.to_json())

# convert the object into a dict
multi_record_encoding_request_dto_dict = multi_record_encoding_request_dto_instance.to_dict()
# create an instance of MultiRecordEncodingRequestDto from a dict
multi_record_encoding_request_dto_from_dict = MultiRecordEncodingRequestDto.from_dict(multi_record_encoding_request_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


