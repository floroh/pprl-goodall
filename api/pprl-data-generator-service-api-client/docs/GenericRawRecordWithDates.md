# GenericRawRecordWithDates


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**record** | [**GenericRawRecord**](GenericRawRecord.md) |  | [optional] 
**occurs_in** | [**List[DateInfo]**](DateInfo.md) |  | [optional] 

## Example

```python
from pprl_data_generator_service_api_client.models.generic_raw_record_with_dates import GenericRawRecordWithDates

# TODO update the JSON string below
json = "{}"
# create an instance of GenericRawRecordWithDates from a JSON string
generic_raw_record_with_dates_instance = GenericRawRecordWithDates.from_json(json)
# print the JSON string representation of the object
print(GenericRawRecordWithDates.to_json())

# convert the object into a dict
generic_raw_record_with_dates_dict = generic_raw_record_with_dates_instance.to_dict()
# create an instance of GenericRawRecordWithDates from a dict
generic_raw_record_with_dates_from_dict = GenericRawRecordWithDates.from_dict(generic_raw_record_with_dates_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


