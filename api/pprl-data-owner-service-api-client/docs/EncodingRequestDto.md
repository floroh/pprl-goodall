# EncodingRequestDto

Request for encoding a single record that is included in the request.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**encoding_id** | [**EncodingIdDto**](EncodingIdDto.md) |  | 
**record** | [**RecordDto**](RecordDto.md) |  | [optional] 
**record_secret** | **str** |  | [optional] 

## Example

```python
from pprl_data_owner_service_api_client.models.encoding_request_dto import EncodingRequestDto

# TODO update the JSON string below
json = "{}"
# create an instance of EncodingRequestDto from a JSON string
encoding_request_dto_instance = EncodingRequestDto.from_json(json)
# print the JSON string representation of the object
print(EncodingRequestDto.to_json())

# convert the object into a dict
encoding_request_dto_dict = encoding_request_dto_instance.to_dict()
# create an instance of EncodingRequestDto from a dict
encoding_request_dto_from_dict = EncodingRequestDto.from_dict(encoding_request_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


