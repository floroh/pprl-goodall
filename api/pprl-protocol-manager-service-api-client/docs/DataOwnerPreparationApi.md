# pprl_protocol_manager_service_api_client.DataOwnerPreparationApi

All URIs are relative to *http://localhost:8085*

Method | HTTP request | Description
------------- | ------------- | -------------
[**insert_from_csv**](DataOwnerPreparationApi.md#insert_from_csv) | **POST** /data-owner/record | Insert dataset from csv file


# **insert_from_csv**
> int insert_from_csv(dataset_csv_dto)

Insert dataset from csv file

### Example


```python
import pprl_protocol_manager_service_api_client
from pprl_protocol_manager_service_api_client.models.dataset_csv_dto import DatasetCsvDto
from pprl_protocol_manager_service_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8085
# See configuration.py for a list of all supported configuration parameters.
configuration = pprl_protocol_manager_service_api_client.Configuration(
    host = "http://localhost:8085"
)


# Enter a context with an instance of the API client
with pprl_protocol_manager_service_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pprl_protocol_manager_service_api_client.DataOwnerPreparationApi(api_client)
    dataset_csv_dto = pprl_protocol_manager_service_api_client.DatasetCsvDto() # DatasetCsvDto | 

    try:
        # Insert dataset from csv file
        api_response = api_instance.insert_from_csv(dataset_csv_dto)
        print("The response of DataOwnerPreparationApi->insert_from_csv:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataOwnerPreparationApi->insert_from_csv: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dataset_csv_dto** | [**DatasetCsvDto**](DatasetCsvDto.md)|  | 

### Return type

**int**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

