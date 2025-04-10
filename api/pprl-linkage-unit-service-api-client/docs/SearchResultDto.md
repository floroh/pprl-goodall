# SearchResultDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**query_id** | [**RecordIdDto**](RecordIdDto.md) |  | [optional] 
**matches** | [**List[SearchResultEntryDto]**](SearchResultEntryDto.md) |  | [optional] 

## Example

```python
from pprl_linkage_unit_service_api_client.models.search_result_dto import SearchResultDto

# TODO update the JSON string below
json = "{}"
# create an instance of SearchResultDto from a JSON string
search_result_dto_instance = SearchResultDto.from_json(json)
# print the JSON string representation of the object
print(SearchResultDto.to_json())

# convert the object into a dict
search_result_dto_dict = search_result_dto_instance.to_dict()
# create an instance of SearchResultDto from a dict
search_result_dto_from_dict = SearchResultDto.from_dict(search_result_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


