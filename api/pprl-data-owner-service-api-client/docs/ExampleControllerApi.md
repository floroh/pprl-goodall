# pprl_data_owner_service_api_client.ExampleControllerApi

All URIs are relative to *http://localhost:8081*

Method | HTTP request | Description
------------- | ------------- | -------------
[**example**](ExampleControllerApi.md#example) | **GET** /example | 


# **example**
> RecordDto example()



### Example


```python
import pprl_data_owner_service_api_client
from pprl_data_owner_service_api_client.models.record_dto import RecordDto
from pprl_data_owner_service_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8081
# See configuration.py for a list of all supported configuration parameters.
configuration = pprl_data_owner_service_api_client.Configuration(
    host = "http://localhost:8081"
)


# Enter a context with an instance of the API client
with pprl_data_owner_service_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pprl_data_owner_service_api_client.ExampleControllerApi(api_client)

    try:
        api_response = api_instance.example()
        print("The response of ExampleControllerApi->example:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExampleControllerApi->example: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**RecordDto**](RecordDto.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

