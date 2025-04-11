# EncodedTransferRequestDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data_owner_dataset_id** | **int** |  | [optional] 
**encoding** | [**EncodingIdDto**](EncodingIdDto.md) |  | 

## Example

```python
from pprl_protocol_manager_service_api_client.models.encoded_transfer_request_dto import EncodedTransferRequestDto

# TODO update the JSON string below
json = "{}"
# create an instance of EncodedTransferRequestDto from a JSON string
encoded_transfer_request_dto_instance = EncodedTransferRequestDto.from_json(json)
# print the JSON string representation of the object
print(EncodedTransferRequestDto.to_json())

# convert the object into a dict
encoded_transfer_request_dto_dict = encoded_transfer_request_dto_instance.to_dict()
# create an instance of EncodedTransferRequestDto from a dict
encoded_transfer_request_dto_from_dict = EncodedTransferRequestDto.from_dict(encoded_transfer_request_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


