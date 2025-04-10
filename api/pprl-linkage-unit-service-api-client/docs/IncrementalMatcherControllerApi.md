# pprl_linkage_unit_service_api_client.IncrementalMatcherControllerApi

All URIs are relative to *http://localhost:8082*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create1**](IncrementalMatcherControllerApi.md#create1) | **POST** /insert | 
[**search**](IncrementalMatcherControllerApi.md#search) | **POST** /search | 


# **create1**
> RecordIdDto create1(record_dto)



### Example


```python
import pprl_linkage_unit_service_api_client
from pprl_linkage_unit_service_api_client.models.record_dto import RecordDto
from pprl_linkage_unit_service_api_client.models.record_id_dto import RecordIdDto
from pprl_linkage_unit_service_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8082
# See configuration.py for a list of all supported configuration parameters.
configuration = pprl_linkage_unit_service_api_client.Configuration(
    host = "http://localhost:8082"
)


# Enter a context with an instance of the API client
with pprl_linkage_unit_service_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pprl_linkage_unit_service_api_client.IncrementalMatcherControllerApi(api_client)
    record_dto = pprl_linkage_unit_service_api_client.RecordDto() # RecordDto | 

    try:
        api_response = api_instance.create1(record_dto)
        print("The response of IncrementalMatcherControllerApi->create1:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling IncrementalMatcherControllerApi->create1: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **record_dto** | [**RecordDto**](RecordDto.md)|  | 

### Return type

[**RecordIdDto**](RecordIdDto.md)

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

# **search**
> SearchResultDto search(record_dto)



### Example


```python
import pprl_linkage_unit_service_api_client
from pprl_linkage_unit_service_api_client.models.record_dto import RecordDto
from pprl_linkage_unit_service_api_client.models.search_result_dto import SearchResultDto
from pprl_linkage_unit_service_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8082
# See configuration.py for a list of all supported configuration parameters.
configuration = pprl_linkage_unit_service_api_client.Configuration(
    host = "http://localhost:8082"
)


# Enter a context with an instance of the API client
with pprl_linkage_unit_service_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pprl_linkage_unit_service_api_client.IncrementalMatcherControllerApi(api_client)
    record_dto = pprl_linkage_unit_service_api_client.RecordDto() # RecordDto | 

    try:
        api_response = api_instance.search(record_dto)
        print("The response of IncrementalMatcherControllerApi->search:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling IncrementalMatcherControllerApi->search: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **record_dto** | [**RecordDto**](RecordDto.md)|  | 

### Return type

[**SearchResultDto**](SearchResultDto.md)

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

