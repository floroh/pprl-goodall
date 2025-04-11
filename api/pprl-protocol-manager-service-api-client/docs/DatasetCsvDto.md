# DatasetCsvDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** |  | [optional] 
**dataset_id** | **int** |  | [optional] 

## Example

```python
from pprl_protocol_manager_service_api_client.models.dataset_csv_dto import DatasetCsvDto

# TODO update the JSON string below
json = "{}"
# create an instance of DatasetCsvDto from a JSON string
dataset_csv_dto_instance = DatasetCsvDto.from_json(json)
# print the JSON string representation of the object
print(DatasetCsvDto.to_json())

# convert the object into a dict
dataset_csv_dto_dict = dataset_csv_dto_instance.to_dict()
# create an instance of DatasetCsvDto from a dict
dataset_csv_dto_from_dict = DatasetCsvDto.from_dict(dataset_csv_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


