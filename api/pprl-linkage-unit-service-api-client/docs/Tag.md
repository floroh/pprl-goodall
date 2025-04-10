# Tag


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id0** | **str** |  | [optional] 
**id1** | **str** |  | [optional] 
**attribute** | **str** |  | [optional] 
**tag** | **str** |  | [optional] 
**string_value** | **str** |  | [optional] 
**numeric_value** | **float** |  | [optional] 

## Example

```python
from pprl_linkage_unit_service_api_client.models.tag import Tag

# TODO update the JSON string below
json = "{}"
# create an instance of Tag from a JSON string
tag_instance = Tag.from_json(json)
# print the JSON string representation of the object
print(Tag.to_json())

# convert the object into a dict
tag_dict = tag_instance.to_dict()
# create an instance of Tag from a dict
tag_from_dict = Tag.from_dict(tag_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


