# EncodingIdDto

ID of an encoding scheme

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**method** | **str** | Name of the encoding scheme | [optional] 
**project** | **str** | Unique name of the record-linkage project | [optional] 

## Example

```python
from pprl_linkage_unit_service_api_client.models.encoding_id_dto import EncodingIdDto

# TODO update the JSON string below
json = "{}"
# create an instance of EncodingIdDto from a JSON string
encoding_id_dto_instance = EncodingIdDto.from_json(json)
# print the JSON string representation of the object
print(EncodingIdDto.to_json())

# convert the object into a dict
encoding_id_dto_dict = encoding_id_dto_instance.to_dict()
# create an instance of EncodingIdDto from a dict
encoding_id_dto_from_dict = EncodingIdDto.from_dict(encoding_id_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


