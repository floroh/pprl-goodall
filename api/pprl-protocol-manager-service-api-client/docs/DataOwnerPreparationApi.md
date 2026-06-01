# pprl_protocol_manager_service_api_client.DataOwnerPreparationApi

All URIs are relative to *http://localhost:8185*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_generated_dataset**](DataOwnerPreparationApi.md#add_generated_dataset) | **POST** /data-owner/record/generate | Insert dataset from generator
[**insert_from_csv**](DataOwnerPreparationApi.md#insert_from_csv) | **POST** /data-owner/record | Insert dataset from csv file


# **add_generated_dataset**
> int add_generated_dataset(dataset_generator_dto)

Insert dataset from generator

### Example


```python
import pprl_protocol_manager_service_api_client
from pprl_protocol_manager_service_api_client.models.dataset_generator_dto import DatasetGeneratorDto
from pprl_protocol_manager_service_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8185
# See configuration.py for a list of all supported configuration parameters.
configuration = pprl_protocol_manager_service_api_client.Configuration(
    host = "http://localhost:8185"
)


# Enter a context with an instance of the API client
with pprl_protocol_manager_service_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pprl_protocol_manager_service_api_client.DataOwnerPreparationApi(api_client)
    dataset_generator_dto = pprl_protocol_manager_service_api_client.DatasetGeneratorDto() # DatasetGeneratorDto | 

    try:
        # Insert dataset from generator
        api_response = api_instance.add_generated_dataset(dataset_generator_dto)
        print("The response of DataOwnerPreparationApi->add_generated_dataset:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataOwnerPreparationApi->add_generated_dataset: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dataset_generator_dto** | [**DatasetGeneratorDto**](DatasetGeneratorDto.md)|  | 

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

# **insert_from_csv**
> int insert_from_csv(dataset_csv_dto)

Insert dataset from csv file

### Example


```python
import pprl_protocol_manager_service_api_client
from pprl_protocol_manager_service_api_client.models.dataset_csv_dto import DatasetCsvDto
from pprl_protocol_manager_service_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8185
# See configuration.py for a list of all supported configuration parameters.
configuration = pprl_protocol_manager_service_api_client.Configuration(
    host = "http://localhost:8185"
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

