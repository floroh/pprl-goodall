# DateInfo


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**var_date** | **str** |  | [optional] 
**year** | **int** |  | [optional] 
**month** | **int** |  | [optional] 
**day** | **int** |  | [optional] 
**as_date** | **date** |  | [optional] 

## Example

```python
from pprl_data_generator_service_api_client.models.date_info import DateInfo

# TODO update the JSON string below
json = "{}"
# create an instance of DateInfo from a JSON string
date_info_instance = DateInfo.from_json(json)
# print the JSON string representation of the object
print(DateInfo.to_json())

# convert the object into a dict
date_info_dict = date_info_instance.to_dict()
# create an instance of DateInfo from a dict
date_info_from_dict = DateInfo.from_dict(date_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


