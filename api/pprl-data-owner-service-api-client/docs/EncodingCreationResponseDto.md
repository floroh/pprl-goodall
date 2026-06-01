# EncodingCreationResponseDto

Response of creating an encoding definition.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**request** | [**EncodingCreationRequestDto**](EncodingCreationRequestDto.md) | Request description with auto-generated dataset-based properties | [optional] 
**encoding** | [**EncodingDto**](EncodingDto.md) |  | [optional] 

## Example

```python
from pprl_data_owner_service_api_client.models.encoding_creation_response_dto import EncodingCreationResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of EncodingCreationResponseDto from a JSON string
encoding_creation_response_dto_instance = EncodingCreationResponseDto.from_json(json)
# print the JSON string representation of the object
print(EncodingCreationResponseDto.to_json())

# convert the object into a dict
encoding_creation_response_dto_dict = encoding_creation_response_dto_instance.to_dict()
# create an instance of EncodingCreationResponseDto from a dict
encoding_creation_response_dto_from_dict = EncodingCreationResponseDto.from_dict(encoding_creation_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


