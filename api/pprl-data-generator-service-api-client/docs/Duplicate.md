# Duplicate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**record** | [**GenericRawRecord**](GenericRawRecord.md) |  | [optional] 
**occurs_in** | [**List[DateInfo]**](DateInfo.md) |  | [optional] 
**changes** | **Dict[str, bool]** |  | [optional] 
**timespan_in_days** | **List[int]** |  | [optional] 

## Example

```python
from pprl_data_generator_service_api_client.models.duplicate import Duplicate

# TODO update the JSON string below
json = "{}"
# create an instance of Duplicate from a JSON string
duplicate_instance = Duplicate.from_json(json)
# print the JSON string representation of the object
print(Duplicate.to_json())

# convert the object into a dict
duplicate_dict = duplicate_instance.to_dict()
# create an instance of Duplicate from a dict
duplicate_from_dict = Duplicate.from_dict(duplicate_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


