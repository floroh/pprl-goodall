# pprl_protocol_manager_service_api_client.ServiceConnectionsApi

All URIs are relative to *http://localhost:8185*

Method | HTTP request | Description
------------- | ------------- | -------------
[**test_connections**](ServiceConnectionsApi.md#test_connections) | **GET** /connectivity/test | Test connections


# **test_connections**
> bool test_connections()

Test connections

### Example


```python
import pprl_protocol_manager_service_api_client
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
    api_instance = pprl_protocol_manager_service_api_client.ServiceConnectionsApi(api_client)

    try:
        # Test connections
        api_response = api_instance.test_connections()
        print("The response of ServiceConnectionsApi->test_connections:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ServiceConnectionsApi->test_connections: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

**bool**

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

