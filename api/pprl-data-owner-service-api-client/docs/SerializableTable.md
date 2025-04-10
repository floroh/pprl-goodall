# SerializableTable


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**header** | **List[str]** |  | [optional] 
**types** | **List[str]** |  | [optional] 
**data** | **List[List[str]]** |  | [optional] 

## Example

```python
from pprl_data_owner_service_api_client.models.serializable_table import SerializableTable

# TODO update the JSON string below
json = "{}"
# create an instance of SerializableTable from a JSON string
serializable_table_instance = SerializableTable.from_json(json)
# print the JSON string representation of the object
print(SerializableTable.to_json())

# convert the object into a dict
serializable_table_dict = serializable_table_instance.to_dict()
# create an instance of SerializableTable from a dict
serializable_table_from_dict = SerializableTable.from_dict(serializable_table_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


