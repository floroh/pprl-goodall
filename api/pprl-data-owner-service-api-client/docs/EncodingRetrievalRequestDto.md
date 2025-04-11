# EncodingRetrievalRequestDto

Request description for encoding a single record. The record itself is not part of the request, but retrieved from the database using its id.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**encoding_id** | [**EncodingIdDto**](EncodingIdDto.md) |  | 
**dataset_id** | **int** |  | [optional] 
**record_secret** | **str** |  | [optional] 

## Example

```python
from pprl_data_owner_service_api_client.models.encoding_retrieval_request_dto import EncodingRetrievalRequestDto

# TODO update the JSON string below
json = "{}"
# create an instance of EncodingRetrievalRequestDto from a JSON string
encoding_retrieval_request_dto_instance = EncodingRetrievalRequestDto.from_json(json)
# print the JSON string representation of the object
print(EncodingRetrievalRequestDto.to_json())

# convert the object into a dict
encoding_retrieval_request_dto_dict = encoding_retrieval_request_dto_instance.to_dict()
# create an instance of EncodingRetrievalRequestDto from a dict
encoding_retrieval_request_dto_from_dict = EncodingRetrievalRequestDto.from_dict(encoding_retrieval_request_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


