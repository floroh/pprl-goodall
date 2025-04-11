# pprl_linkage_unit_service_api_client.ProjectBasedBatchMatchingApi

All URIs are relative to *http://localhost:8082*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create**](ProjectBasedBatchMatchingApi.md#create) | **POST** /project/ | Create new linkage project
[**delete**](ProjectBasedBatchMatchingApi.md#delete) | **DELETE** /project/{projectId} | Delete a project
[**delete_all1**](ProjectBasedBatchMatchingApi.md#delete_all1) | **DELETE** /project/all | Delete all projects
[**find_all**](ProjectBasedBatchMatchingApi.md#find_all) | **GET** /project/findAll | Get existing linkage projects
[**get**](ProjectBasedBatchMatchingApi.md#get) | **GET** /project/{projectId} | Get an existing linkage project
[**reset**](ProjectBasedBatchMatchingApi.md#reset) | **POST** /project/reset | Reset a linkage project
[**run_for_new**](ProjectBasedBatchMatchingApi.md#run_for_new) | **POST** /project/runForNew/{projectId} | Run a linkage project for new records
[**run_next**](ProjectBasedBatchMatchingApi.md#run_next) | **POST** /project/run/{projectId} | Run (the next phase of) a linkage project
[**run_parts**](ProjectBasedBatchMatchingApi.md#run_parts) | **POST** /project/run | Execute (parts of) a linkage project


# **create**
> BatchMatchProjectDto create(batch_match_project_dto)

Create new linkage project

### Example


```python
import pprl_linkage_unit_service_api_client
from pprl_linkage_unit_service_api_client.models.batch_match_project_dto import BatchMatchProjectDto
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
    api_instance = pprl_linkage_unit_service_api_client.ProjectBasedBatchMatchingApi(api_client)
    batch_match_project_dto = pprl_linkage_unit_service_api_client.BatchMatchProjectDto() # BatchMatchProjectDto | 

    try:
        # Create new linkage project
        api_response = api_instance.create(batch_match_project_dto)
        print("The response of ProjectBasedBatchMatchingApi->create:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectBasedBatchMatchingApi->create: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **batch_match_project_dto** | [**BatchMatchProjectDto**](BatchMatchProjectDto.md)|  | 

### Return type

[**BatchMatchProjectDto**](BatchMatchProjectDto.md)

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

# **delete**
> delete(project_id, delete_parents=delete_parents)

Delete a project

### Example


```python
import pprl_linkage_unit_service_api_client
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
    api_instance = pprl_linkage_unit_service_api_client.ProjectBasedBatchMatchingApi(api_client)
    project_id = 'project_id_example' # str | 
    delete_parents = True # bool |  (optional)

    try:
        # Delete a project
        api_instance.delete(project_id, delete_parents=delete_parents)
    except Exception as e:
        print("Exception when calling ProjectBasedBatchMatchingApi->delete: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **delete_parents** | **bool**|  | [optional] 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_all1**
> delete_all1()

Delete all projects

### Example


```python
import pprl_linkage_unit_service_api_client
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
    api_instance = pprl_linkage_unit_service_api_client.ProjectBasedBatchMatchingApi(api_client)

    try:
        # Delete all projects
        api_instance.delete_all1()
    except Exception as e:
        print("Exception when calling ProjectBasedBatchMatchingApi->delete_all1: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_all**
> List[BatchMatchProjectDto] find_all(update=update)

Get existing linkage projects

### Example


```python
import pprl_linkage_unit_service_api_client
from pprl_linkage_unit_service_api_client.models.batch_match_project_dto import BatchMatchProjectDto
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
    api_instance = pprl_linkage_unit_service_api_client.ProjectBasedBatchMatchingApi(api_client)
    update = 'update_example' # str |  (optional)

    try:
        # Get existing linkage projects
        api_response = api_instance.find_all(update=update)
        print("The response of ProjectBasedBatchMatchingApi->find_all:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectBasedBatchMatchingApi->find_all: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **update** | **str**|  | [optional] 

### Return type

[**List[BatchMatchProjectDto]**](BatchMatchProjectDto.md)

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

# **get**
> BatchMatchProjectDto get(project_id, update=update)

Get an existing linkage project

### Example


```python
import pprl_linkage_unit_service_api_client
from pprl_linkage_unit_service_api_client.models.batch_match_project_dto import BatchMatchProjectDto
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
    api_instance = pprl_linkage_unit_service_api_client.ProjectBasedBatchMatchingApi(api_client)
    project_id = 'project_id_example' # str | 
    update = 'update_example' # str |  (optional)

    try:
        # Get an existing linkage project
        api_response = api_instance.get(project_id, update=update)
        print("The response of ProjectBasedBatchMatchingApi->get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectBasedBatchMatchingApi->get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **update** | **str**|  | [optional] 

### Return type

[**BatchMatchProjectDto**](BatchMatchProjectDto.md)

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

# **reset**
> BatchMatchProjectDto reset(batch_match_project_execution_dto)

Reset a linkage project

### Example


```python
import pprl_linkage_unit_service_api_client
from pprl_linkage_unit_service_api_client.models.batch_match_project_dto import BatchMatchProjectDto
from pprl_linkage_unit_service_api_client.models.batch_match_project_execution_dto import BatchMatchProjectExecutionDto
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
    api_instance = pprl_linkage_unit_service_api_client.ProjectBasedBatchMatchingApi(api_client)
    batch_match_project_execution_dto = pprl_linkage_unit_service_api_client.BatchMatchProjectExecutionDto() # BatchMatchProjectExecutionDto | 

    try:
        # Reset a linkage project
        api_response = api_instance.reset(batch_match_project_execution_dto)
        print("The response of ProjectBasedBatchMatchingApi->reset:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectBasedBatchMatchingApi->reset: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **batch_match_project_execution_dto** | [**BatchMatchProjectExecutionDto**](BatchMatchProjectExecutionDto.md)|  | 

### Return type

[**BatchMatchProjectDto**](BatchMatchProjectDto.md)

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

# **run_for_new**
> BatchMatchProjectDto run_for_new(project_id)

Run a linkage project for new records

### Example


```python
import pprl_linkage_unit_service_api_client
from pprl_linkage_unit_service_api_client.models.batch_match_project_dto import BatchMatchProjectDto
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
    api_instance = pprl_linkage_unit_service_api_client.ProjectBasedBatchMatchingApi(api_client)
    project_id = 'project_id_example' # str | 

    try:
        # Run a linkage project for new records
        api_response = api_instance.run_for_new(project_id)
        print("The response of ProjectBasedBatchMatchingApi->run_for_new:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectBasedBatchMatchingApi->run_for_new: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 

### Return type

[**BatchMatchProjectDto**](BatchMatchProjectDto.md)

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

# **run_next**
> BatchMatchProjectDto run_next(project_id)

Run (the next phase of) a linkage project

### Example


```python
import pprl_linkage_unit_service_api_client
from pprl_linkage_unit_service_api_client.models.batch_match_project_dto import BatchMatchProjectDto
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
    api_instance = pprl_linkage_unit_service_api_client.ProjectBasedBatchMatchingApi(api_client)
    project_id = 'project_id_example' # str | 

    try:
        # Run (the next phase of) a linkage project
        api_response = api_instance.run_next(project_id)
        print("The response of ProjectBasedBatchMatchingApi->run_next:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectBasedBatchMatchingApi->run_next: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 

### Return type

[**BatchMatchProjectDto**](BatchMatchProjectDto.md)

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

# **run_parts**
> BatchMatchProjectDto run_parts(batch_match_project_execution_dto)

Execute (parts of) a linkage project

### Example


```python
import pprl_linkage_unit_service_api_client
from pprl_linkage_unit_service_api_client.models.batch_match_project_dto import BatchMatchProjectDto
from pprl_linkage_unit_service_api_client.models.batch_match_project_execution_dto import BatchMatchProjectExecutionDto
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
    api_instance = pprl_linkage_unit_service_api_client.ProjectBasedBatchMatchingApi(api_client)
    batch_match_project_execution_dto = pprl_linkage_unit_service_api_client.BatchMatchProjectExecutionDto() # BatchMatchProjectExecutionDto | 

    try:
        # Execute (parts of) a linkage project
        api_response = api_instance.run_parts(batch_match_project_execution_dto)
        print("The response of ProjectBasedBatchMatchingApi->run_parts:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectBasedBatchMatchingApi->run_parts: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **batch_match_project_execution_dto** | [**BatchMatchProjectExecutionDto**](BatchMatchProjectExecutionDto.md)|  | 

### Return type

[**BatchMatchProjectDto**](BatchMatchProjectDto.md)

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

