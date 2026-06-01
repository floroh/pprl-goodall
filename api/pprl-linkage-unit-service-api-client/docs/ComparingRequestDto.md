# ComparingRequestDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**record_pairs** | [**List[RecordPairWithRecordsDto]**](RecordPairWithRecordsDto.md) |  | [optional] 
**method** | **str** |  | [optional] 

## Example

```python
from pprl_linkage_unit_service_api_client.models.comparing_request_dto import ComparingRequestDto

# TODO update the JSON string below
json = "{}"
# create an instance of ComparingRequestDto from a JSON string
comparing_request_dto_instance = ComparingRequestDto.from_json(json)
# print the JSON string representation of the object
print(ComparingRequestDto.to_json())

# convert the object into a dict
comparing_request_dto_dict = comparing_request_dto_instance.to_dict()
# create an instance of ComparingRequestDto from a dict
comparing_request_dto_from_dict = ComparingRequestDto.from_dict(comparing_request_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


