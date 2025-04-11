# BatchMatchRequestDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**records** | [**List[RecordDto]**](RecordDto.md) |  | [optional] 
**method** | **str** |  | [optional] 

## Example

```python
from pprl_linkage_unit_service_api_client.models.batch_match_request_dto import BatchMatchRequestDto

# TODO update the JSON string below
json = "{}"
# create an instance of BatchMatchRequestDto from a JSON string
batch_match_request_dto_instance = BatchMatchRequestDto.from_json(json)
# print the JSON string representation of the object
print(BatchMatchRequestDto.to_json())

# convert the object into a dict
batch_match_request_dto_dict = batch_match_request_dto_instance.to_dict()
# create an instance of BatchMatchRequestDto from a dict
batch_match_request_dto_from_dict = BatchMatchRequestDto.from_dict(batch_match_request_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


