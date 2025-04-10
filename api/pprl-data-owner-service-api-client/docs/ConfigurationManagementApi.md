# pprl_data_owner_service_api_client.ConfigurationManagementApi

All URIs are relative to *http://localhost:8081*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add1**](ConfigurationManagementApi.md#add1) | **POST** /config/ | Add a configuration
[**get_configs**](ConfigurationManagementApi.md#get_configs) | **GET** /config/findAll | Get a list of all configuration IDs
[**get_encoding**](ConfigurationManagementApi.md#get_encoding) | **POST** /config/findById | Get the configuration by its ID
[**get_encoding_method_requirements**](ConfigurationManagementApi.md#get_encoding_method_requirements) | **GET** /config/findAllRequirements | Get descriptions of the requirements of all encoding methods
[**remove1**](ConfigurationManagementApi.md#remove1) | **DELETE** /config/ | Remove a configuration
[**update2**](ConfigurationManagementApi.md#update2) | **PUT** /config/ | Override an existing configuration


# **add1**
> add1(encoding_dto)

Add a configuration

### Example


```python
import pprl_data_owner_service_api_client
from pprl_data_owner_service_api_client.models.encoding_dto import EncodingDto
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
    api_instance = pprl_data_owner_service_api_client.ConfigurationManagementApi(api_client)
    encoding_dto = pprl_data_owner_service_api_client.EncodingDto() # EncodingDto | 

    try:
        # Add a configuration
        api_instance.add1(encoding_dto)
    except Exception as e:
        print("Exception when calling ConfigurationManagementApi->add1: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **encoding_dto** | [**EncodingDto**](EncodingDto.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_configs**
> List[EncodingIdDto] get_configs()

Get a list of all configuration IDs

### Example


```python
import pprl_data_owner_service_api_client
from pprl_data_owner_service_api_client.models.encoding_id_dto import EncodingIdDto
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
    api_instance = pprl_data_owner_service_api_client.ConfigurationManagementApi(api_client)

    try:
        # Get a list of all configuration IDs
        api_response = api_instance.get_configs()
        print("The response of ConfigurationManagementApi->get_configs:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ConfigurationManagementApi->get_configs: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[EncodingIdDto]**](EncodingIdDto.md)

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

# **get_encoding**
> EncodingDto get_encoding(encoding_id_dto)

Get the configuration by its ID

### Example


```python
import pprl_data_owner_service_api_client
from pprl_data_owner_service_api_client.models.encoding_dto import EncodingDto
from pprl_data_owner_service_api_client.models.encoding_id_dto import EncodingIdDto
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
    api_instance = pprl_data_owner_service_api_client.ConfigurationManagementApi(api_client)
    encoding_id_dto = pprl_data_owner_service_api_client.EncodingIdDto() # EncodingIdDto | 

    try:
        # Get the configuration by its ID
        api_response = api_instance.get_encoding(encoding_id_dto)
        print("The response of ConfigurationManagementApi->get_encoding:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ConfigurationManagementApi->get_encoding: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **encoding_id_dto** | [**EncodingIdDto**](EncodingIdDto.md)|  | 

### Return type

[**EncodingDto**](EncodingDto.md)

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

# **get_encoding_method_requirements**
> List[RecordRequirementsDto] get_encoding_method_requirements()

Get descriptions of the requirements of all encoding methods

### Example


```python
import pprl_data_owner_service_api_client
from pprl_data_owner_service_api_client.models.record_requirements_dto import RecordRequirementsDto
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
    api_instance = pprl_data_owner_service_api_client.ConfigurationManagementApi(api_client)

    try:
        # Get descriptions of the requirements of all encoding methods
        api_response = api_instance.get_encoding_method_requirements()
        print("The response of ConfigurationManagementApi->get_encoding_method_requirements:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ConfigurationManagementApi->get_encoding_method_requirements: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[RecordRequirementsDto]**](RecordRequirementsDto.md)

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

# **remove1**
> remove1(encoding_id_dto)

Remove a configuration

### Example


```python
import pprl_data_owner_service_api_client
from pprl_data_owner_service_api_client.models.encoding_id_dto import EncodingIdDto
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
    api_instance = pprl_data_owner_service_api_client.ConfigurationManagementApi(api_client)
    encoding_id_dto = pprl_data_owner_service_api_client.EncodingIdDto() # EncodingIdDto | 

    try:
        # Remove a configuration
        api_instance.remove1(encoding_id_dto)
    except Exception as e:
        print("Exception when calling ConfigurationManagementApi->remove1: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **encoding_id_dto** | [**EncodingIdDto**](EncodingIdDto.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update2**
> update2(encoding_dto)

Override an existing configuration

### Example


```python
import pprl_data_owner_service_api_client
from pprl_data_owner_service_api_client.models.encoding_dto import EncodingDto
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
    api_instance = pprl_data_owner_service_api_client.ConfigurationManagementApi(api_client)
    encoding_dto = pprl_data_owner_service_api_client.EncodingDto() # EncodingDto | 

    try:
        # Override an existing configuration
        api_instance.update2(encoding_dto)
    except Exception as e:
        print("Exception when calling ConfigurationManagementApi->update2: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **encoding_dto** | [**EncodingDto**](EncodingDto.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

