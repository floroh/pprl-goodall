# pprl_linkage_unit_service_api_client.ActuatorApi

All URIs are relative to *http://localhost:8182*

Method | HTTP request | Description
------------- | ------------- | -------------
[**health**](ActuatorApi.md#health) | **GET** /actuator/health | Actuator web endpoint &#39;health&#39;
[**info**](ActuatorApi.md#info) | **GET** /actuator/info | Actuator web endpoint &#39;info&#39;
[**links**](ActuatorApi.md#links) | **GET** /actuator | Actuator root web endpoint
[**list_names**](ActuatorApi.md#list_names) | **GET** /actuator/metrics | Actuator web endpoint &#39;metrics&#39;
[**mappings**](ActuatorApi.md#mappings) | **GET** /actuator/mappings | Actuator web endpoint &#39;mappings&#39;
[**metric**](ActuatorApi.md#metric) | **GET** /actuator/metrics/{requiredMetricName} | Actuator web endpoint &#39;metrics-requiredMetricName&#39;


# **health**
> object health()

Actuator web endpoint 'health'

### Example


```python
import pprl_linkage_unit_service_api_client
from pprl_linkage_unit_service_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8182
# See configuration.py for a list of all supported configuration parameters.
configuration = pprl_linkage_unit_service_api_client.Configuration(
    host = "http://localhost:8182"
)


# Enter a context with an instance of the API client
with pprl_linkage_unit_service_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pprl_linkage_unit_service_api_client.ActuatorApi(api_client)

    try:
        # Actuator web endpoint 'health'
        api_response = api_instance.health()
        print("The response of ActuatorApi->health:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActuatorApi->health: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.spring-boot.actuator.v3+json, application/vnd.spring-boot.actuator.v2+json, application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **info**
> object info()

Actuator web endpoint 'info'

### Example


```python
import pprl_linkage_unit_service_api_client
from pprl_linkage_unit_service_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8182
# See configuration.py for a list of all supported configuration parameters.
configuration = pprl_linkage_unit_service_api_client.Configuration(
    host = "http://localhost:8182"
)


# Enter a context with an instance of the API client
with pprl_linkage_unit_service_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pprl_linkage_unit_service_api_client.ActuatorApi(api_client)

    try:
        # Actuator web endpoint 'info'
        api_response = api_instance.info()
        print("The response of ActuatorApi->info:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActuatorApi->info: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.spring-boot.actuator.v3+json, application/vnd.spring-boot.actuator.v2+json, application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **links**
> Dict[str, Dict[str, Link]] links()

Actuator root web endpoint

### Example


```python
import pprl_linkage_unit_service_api_client
from pprl_linkage_unit_service_api_client.models.link import Link
from pprl_linkage_unit_service_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8182
# See configuration.py for a list of all supported configuration parameters.
configuration = pprl_linkage_unit_service_api_client.Configuration(
    host = "http://localhost:8182"
)


# Enter a context with an instance of the API client
with pprl_linkage_unit_service_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pprl_linkage_unit_service_api_client.ActuatorApi(api_client)

    try:
        # Actuator root web endpoint
        api_response = api_instance.links()
        print("The response of ActuatorApi->links:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActuatorApi->links: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

**Dict[str, Dict[str, Link]]**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.spring-boot.actuator.v3+json, application/vnd.spring-boot.actuator.v2+json, application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_names**
> object list_names()

Actuator web endpoint 'metrics'

### Example


```python
import pprl_linkage_unit_service_api_client
from pprl_linkage_unit_service_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8182
# See configuration.py for a list of all supported configuration parameters.
configuration = pprl_linkage_unit_service_api_client.Configuration(
    host = "http://localhost:8182"
)


# Enter a context with an instance of the API client
with pprl_linkage_unit_service_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pprl_linkage_unit_service_api_client.ActuatorApi(api_client)

    try:
        # Actuator web endpoint 'metrics'
        api_response = api_instance.list_names()
        print("The response of ActuatorApi->list_names:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActuatorApi->list_names: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.spring-boot.actuator.v3+json, application/vnd.spring-boot.actuator.v2+json, application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **mappings**
> object mappings()

Actuator web endpoint 'mappings'

### Example


```python
import pprl_linkage_unit_service_api_client
from pprl_linkage_unit_service_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8182
# See configuration.py for a list of all supported configuration parameters.
configuration = pprl_linkage_unit_service_api_client.Configuration(
    host = "http://localhost:8182"
)


# Enter a context with an instance of the API client
with pprl_linkage_unit_service_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pprl_linkage_unit_service_api_client.ActuatorApi(api_client)

    try:
        # Actuator web endpoint 'mappings'
        api_response = api_instance.mappings()
        print("The response of ActuatorApi->mappings:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActuatorApi->mappings: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.spring-boot.actuator.v3+json, application/vnd.spring-boot.actuator.v2+json, application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **metric**
> object metric(required_metric_name, tag=tag)

Actuator web endpoint 'metrics-requiredMetricName'

### Example


```python
import pprl_linkage_unit_service_api_client
from pprl_linkage_unit_service_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8182
# See configuration.py for a list of all supported configuration parameters.
configuration = pprl_linkage_unit_service_api_client.Configuration(
    host = "http://localhost:8182"
)


# Enter a context with an instance of the API client
with pprl_linkage_unit_service_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pprl_linkage_unit_service_api_client.ActuatorApi(api_client)
    required_metric_name = 'required_metric_name_example' # str | 
    tag = 'tag_example' # str |  (optional)

    try:
        # Actuator web endpoint 'metrics-requiredMetricName'
        api_response = api_instance.metric(required_metric_name, tag=tag)
        print("The response of ActuatorApi->metric:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActuatorApi->metric: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **required_metric_name** | **str**|  | 
 **tag** | **str**|  | [optional] 

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.spring-boot.actuator.v3+json, application/vnd.spring-boot.actuator.v2+json, application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**404** | Not Found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

