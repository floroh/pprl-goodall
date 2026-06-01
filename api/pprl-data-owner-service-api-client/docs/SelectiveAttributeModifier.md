# SelectiveAttributeModifier


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**modifier** | [**AttributeModifierObject**](AttributeModifierObject.md) |  | [optional] 
**selector** | [**SelectorString**](SelectorString.md) |  | [optional] 
**var_class** | **str** |  | 

## Example

```python
from pprl_data_owner_service_api_client.models.selective_attribute_modifier import SelectiveAttributeModifier

# TODO update the JSON string below
json = "{}"
# create an instance of SelectiveAttributeModifier from a JSON string
selective_attribute_modifier_instance = SelectiveAttributeModifier.from_json(json)
# print the JSON string representation of the object
print(SelectiveAttributeModifier.to_json())

# convert the object into a dict
selective_attribute_modifier_dict = selective_attribute_modifier_instance.to_dict()
# create an instance of SelectiveAttributeModifier from a dict
selective_attribute_modifier_from_dict = SelectiveAttributeModifier.from_dict(selective_attribute_modifier_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


