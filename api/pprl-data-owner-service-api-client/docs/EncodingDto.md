# EncodingDto

Description of an encoding scheme

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | [**EncodingIdDto**](EncodingIdDto.md) |  | [optional] 
**validation** | [**RecordRequirementsDto**](RecordRequirementsDto.md) |  | [optional] 
**config** | **str** | Configuration / parameters to build the encoder | [optional] 

## Example

```python
from pprl_data_owner_service_api_client.models.encoding_dto import EncodingDto

# TODO update the JSON string below
json = "{}"
# create an instance of EncodingDto from a JSON string
encoding_dto_instance = EncodingDto.from_json(json)
# print the JSON string representation of the object
print(EncodingDto.to_json())

# convert the object into a dict
encoding_dto_dict = encoding_dto_instance.to_dict()
# create an instance of EncodingDto from a dict
encoding_dto_from_dict = EncodingDto.from_dict(encoding_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


