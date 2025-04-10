# RecordEncodingWishDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**encoding_id** | [**EncodingIdDto**](EncodingIdDto.md) |  | [optional] 
**record_secret** | **str** |  | [optional] 
**order_id** | **int** |  | [optional] 

## Example

```python
from pprl_linkage_unit_service_api_client.models.record_encoding_wish_dto import RecordEncodingWishDto

# TODO update the JSON string below
json = "{}"
# create an instance of RecordEncodingWishDto from a JSON string
record_encoding_wish_dto_instance = RecordEncodingWishDto.from_json(json)
# print the JSON string representation of the object
print(RecordEncodingWishDto.to_json())

# convert the object into a dict
record_encoding_wish_dto_dict = record_encoding_wish_dto_instance.to_dict()
# create an instance of RecordEncodingWishDto from a dict
record_encoding_wish_dto_from_dict = RecordEncodingWishDto.from_dict(record_encoding_wish_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


