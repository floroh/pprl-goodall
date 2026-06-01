# DataSetModifierConfig


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**tag** | **str** |  | [optional] 
**original_source_name** | **str** |  | [optional] 
**modified_source_name** | **str** |  | [optional] 
**filter_records_to_modify** | [**SelectorRecord**](SelectorRecord.md) |  | [optional] 
**record_modifiers** | [**List[SelectiveRecordModifier]**](SelectiveRecordModifier.md) |  | [optional] 
**attribute_modifiers** | **Dict[str, List[SelectiveAttributeModifier]]** |  | [optional] 
**true_duplicate** | **bool** |  | [optional] 
**var_class** | **str** |  | 

## Example

```python
from pprl_data_owner_service_api_client.models.data_set_modifier_config import DataSetModifierConfig

# TODO update the JSON string below
json = "{}"
# create an instance of DataSetModifierConfig from a JSON string
data_set_modifier_config_instance = DataSetModifierConfig.from_json(json)
# print the JSON string representation of the object
print(DataSetModifierConfig.to_json())

# convert the object into a dict
data_set_modifier_config_dict = data_set_modifier_config_instance.to_dict()
# create an instance of DataSetModifierConfig from a dict
data_set_modifier_config_from_dict = DataSetModifierConfig.from_dict(data_set_modifier_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


