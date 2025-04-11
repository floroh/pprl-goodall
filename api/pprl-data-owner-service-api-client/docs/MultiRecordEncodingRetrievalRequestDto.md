# MultiRecordEncodingRetrievalRequestDto

Request description for encoding multiple records from the same dataset with the same encoding. No record-specific secret is required or possible.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**encoding_id** | [**EncodingIdDto**](EncodingIdDto.md) |  | [optional] 
**record_ids** | [**List[RecordIdDto]**](RecordIdDto.md) | List of record ids to encode. If empty, all records of the dataset are encoded. | [optional] 
**dataset_id** | **int** |  | [optional] 

## Example

```python
from pprl_data_owner_service_api_client.models.multi_record_encoding_retrieval_request_dto import MultiRecordEncodingRetrievalRequestDto

# TODO update the JSON string below
json = "{}"
# create an instance of MultiRecordEncodingRetrievalRequestDto from a JSON string
multi_record_encoding_retrieval_request_dto_instance = MultiRecordEncodingRetrievalRequestDto.from_json(json)
# print the JSON string representation of the object
print(MultiRecordEncodingRetrievalRequestDto.to_json())

# convert the object into a dict
multi_record_encoding_retrieval_request_dto_dict = multi_record_encoding_retrieval_request_dto_instance.to_dict()
# create an instance of MultiRecordEncodingRetrievalRequestDto from a dict
multi_record_encoding_retrieval_request_dto_from_dict = MultiRecordEncodingRetrievalRequestDto.from_dict(multi_record_encoding_retrieval_request_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


