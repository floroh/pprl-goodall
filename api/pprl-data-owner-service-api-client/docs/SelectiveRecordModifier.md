# SelectiveRecordModifier


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**modifier** | [**RecordModifier**](RecordModifier.md) |  | [optional] 
**selector** | [**SelectorRecord**](SelectorRecord.md) |  | [optional] 
**var_class** | **str** |  | 

## Example

```python
from pprl_data_owner_service_api_client.models.selective_record_modifier import SelectiveRecordModifier

# TODO update the JSON string below
json = "{}"
# create an instance of SelectiveRecordModifier from a JSON string
selective_record_modifier_instance = SelectiveRecordModifier.from_json(json)
# print the JSON string representation of the object
print(SelectiveRecordModifier.to_json())

# convert the object into a dict
selective_record_modifier_dict = selective_record_modifier_instance.to_dict()
# create an instance of SelectiveRecordModifier from a dict
selective_record_modifier_from_dict = SelectiveRecordModifier.from_dict(selective_record_modifier_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


