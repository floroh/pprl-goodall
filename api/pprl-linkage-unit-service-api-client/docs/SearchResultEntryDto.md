# SearchResultEntryDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**found_id** | [**RecordIdDto**](RecordIdDto.md) |  | [optional] 
**similarity** | **float** |  | [optional] 

## Example

```python
from pprl_linkage_unit_service_api_client.models.search_result_entry_dto import SearchResultEntryDto

# TODO update the JSON string below
json = "{}"
# create an instance of SearchResultEntryDto from a JSON string
search_result_entry_dto_instance = SearchResultEntryDto.from_json(json)
# print the JSON string representation of the object
print(SearchResultEntryDto.to_json())

# convert the object into a dict
search_result_entry_dto_dict = search_result_entry_dto_instance.to_dict()
# create an instance of SearchResultEntryDto from a dict
search_result_entry_dto_from_dict = SearchResultEntryDto.from_dict(search_result_entry_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


