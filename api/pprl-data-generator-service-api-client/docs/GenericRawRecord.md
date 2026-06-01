# GenericRawRecord


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**voter_id** | **str** |  | [optional] 
**snap_shot** | [**DateInfo**](DateInfo.md) |  | [optional] 
**attributes** | **Dict[str, str]** |  | [optional] 

## Example

```python
from pprl_data_generator_service_api_client.models.generic_raw_record import GenericRawRecord

# TODO update the JSON string below
json = "{}"
# create an instance of GenericRawRecord from a JSON string
generic_raw_record_instance = GenericRawRecord.from_json(json)
# print the JSON string representation of the object
print(GenericRawRecord.to_json())

# convert the object into a dict
generic_raw_record_dict = generic_raw_record_instance.to_dict()
# create an instance of GenericRawRecord from a dict
generic_raw_record_from_dict = GenericRawRecord.from_dict(generic_raw_record_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


