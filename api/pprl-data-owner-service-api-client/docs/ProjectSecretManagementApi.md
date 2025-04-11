# pprl_data_owner_service_api_client.ProjectSecretManagementApi

All URIs are relative to *http://localhost:8081*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add**](ProjectSecretManagementApi.md#add) | **POST** /secret/ | Add a secret for a project
[**get_projects**](ProjectSecretManagementApi.md#get_projects) | **GET** /secret/findAll | Get a list of all projects that are registered with a secret
[**remove**](ProjectSecretManagementApi.md#remove) | **DELETE** /secret/ | Remove a secret of a project
[**update**](ProjectSecretManagementApi.md#update) | **PUT** /secret/ | Override a secret of a project


# **add**
> add(secret_dto)

Add a secret for a project

### Example


```python
import pprl_data_owner_service_api_client
from pprl_data_owner_service_api_client.models.secret_dto import SecretDto
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
    api_instance = pprl_data_owner_service_api_client.ProjectSecretManagementApi(api_client)
    secret_dto = pprl_data_owner_service_api_client.SecretDto() # SecretDto | 

    try:
        # Add a secret for a project
        api_instance.add(secret_dto)
    except Exception as e:
        print("Exception when calling ProjectSecretManagementApi->add: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **secret_dto** | [**SecretDto**](SecretDto.md)|  | 

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

# **get_projects**
> List[str] get_projects()

Get a list of all projects that are registered with a secret

### Example


```python
import pprl_data_owner_service_api_client
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
    api_instance = pprl_data_owner_service_api_client.ProjectSecretManagementApi(api_client)

    try:
        # Get a list of all projects that are registered with a secret
        api_response = api_instance.get_projects()
        print("The response of ProjectSecretManagementApi->get_projects:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectSecretManagementApi->get_projects: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

**List[str]**

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

# **remove**
> remove(body)

Remove a secret of a project

### Example


```python
import pprl_data_owner_service_api_client
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
    api_instance = pprl_data_owner_service_api_client.ProjectSecretManagementApi(api_client)
    body = 'body_example' # str | 

    try:
        # Remove a secret of a project
        api_instance.remove(body)
    except Exception as e:
        print("Exception when calling ProjectSecretManagementApi->remove: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | **str**|  | 

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

# **update**
> update(secret_dto)

Override a secret of a project

### Example


```python
import pprl_data_owner_service_api_client
from pprl_data_owner_service_api_client.models.secret_dto import SecretDto
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
    api_instance = pprl_data_owner_service_api_client.ProjectSecretManagementApi(api_client)
    secret_dto = pprl_data_owner_service_api_client.SecretDto() # SecretDto | 

    try:
        # Override a secret of a project
        api_instance.update(secret_dto)
    except Exception as e:
        print("Exception when calling ProjectSecretManagementApi->update: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **secret_dto** | [**SecretDto**](SecretDto.md)|  | 

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

