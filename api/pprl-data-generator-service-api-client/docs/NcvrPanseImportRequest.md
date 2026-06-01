# NcvrPanseImportRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**max_clusters** | **int** |  | [optional] 
**force_import_even_when_not_empty** | **bool** |  | [optional] 

## Example

```python
from pprl_data_generator_service_api_client.models.ncvr_panse_import_request import NcvrPanseImportRequest

# TODO update the JSON string below
json = "{}"
# create an instance of NcvrPanseImportRequest from a JSON string
ncvr_panse_import_request_instance = NcvrPanseImportRequest.from_json(json)
# print the JSON string representation of the object
print(NcvrPanseImportRequest.to_json())

# convert the object into a dict
ncvr_panse_import_request_dict = ncvr_panse_import_request_instance.to_dict()
# create an instance of NcvrPanseImportRequest from a dict
ncvr_panse_import_request_from_dict = NcvrPanseImportRequest.from_dict(ncvr_panse_import_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


