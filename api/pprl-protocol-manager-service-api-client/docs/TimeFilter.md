# TimeFilter


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ignore_order** | **bool** |  | [optional] 
**require_all_timestamps_passing** | **bool** |  | [optional] 
**min_days** | **int** |  | [optional] 
**max_days** | **int** |  | [optional] 

## Example

```python
from pprl_protocol_manager_service_api_client.models.time_filter import TimeFilter

# TODO update the JSON string below
json = "{}"
# create an instance of TimeFilter from a JSON string
time_filter_instance = TimeFilter.from_json(json)
# print the JSON string representation of the object
print(TimeFilter.to_json())

# convert the object into a dict
time_filter_dict = time_filter_instance.to_dict()
# create an instance of TimeFilter from a dict
time_filter_from_dict = TimeFilter.from_dict(time_filter_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


