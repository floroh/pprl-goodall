# ChangeFilter


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**min_changes** | **int** |  | [optional] 
**max_changes** | **int** |  | [optional] 
**changed_attributes** | **List[str]** |  | [optional] 
**unchanged_attributes** | **List[str]** |  | [optional] 
**require_all_listed_attributes** | **bool** |  | [optional] 

## Example

```python
from pprl_data_generator_service_api_client.models.change_filter import ChangeFilter

# TODO update the JSON string below
json = "{}"
# create an instance of ChangeFilter from a JSON string
change_filter_instance = ChangeFilter.from_json(json)
# print the JSON string representation of the object
print(ChangeFilter.to_json())

# convert the object into a dict
change_filter_dict = change_filter_instance.to_dict()
# create an instance of ChangeFilter from a dict
change_filter_from_dict = ChangeFilter.from_dict(change_filter_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


