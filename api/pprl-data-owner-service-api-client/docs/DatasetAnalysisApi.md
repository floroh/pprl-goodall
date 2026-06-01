# pprl_data_owner_service_api_client.DatasetAnalysisApi

All URIs are relative to *http://localhost:8181*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_tags**](DatasetAnalysisApi.md#delete_tags) | **DELETE** /analysis/tag/{datasetId} | Delete all tags of a dataset from database
[**get_analysis_types**](DatasetAnalysisApi.md#get_analysis_types) | **GET** /analysis/findAll | Get a list of all supported analysis types
[**get_tags**](DatasetAnalysisApi.md#get_tags) | **GET** /analysis/tag/{datasetId} | Get tags from database
[**get_tags_by_origin**](DatasetAnalysisApi.md#get_tags_by_origin) | **GET** /analysis/tag/{datasetId}/{origin} | Get tags from database
[**run_analysis**](DatasetAnalysisApi.md#run_analysis) | **POST** /analysis/run | Run a specific analysis type
[**run_pair_analysis**](DatasetAnalysisApi.md#run_pair_analysis) | **POST** /analysis/pair-tags/{datasetId} | Get tags for pairs
[**run_validation_analysis**](DatasetAnalysisApi.md#run_validation_analysis) | **POST** /analysis/runValidation | Run a specific analysis type
[**save_tags**](DatasetAnalysisApi.md#save_tags) | **POST** /analysis/tag/{datasetId} | Add tags to database


# **delete_tags**
> delete_tags(dataset_id)

Delete all tags of a dataset from database

### Example


```python
import pprl_data_owner_service_api_client
from pprl_data_owner_service_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8181
# See configuration.py for a list of all supported configuration parameters.
configuration = pprl_data_owner_service_api_client.Configuration(
    host = "http://localhost:8181"
)


# Enter a context with an instance of the API client
with pprl_data_owner_service_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pprl_data_owner_service_api_client.DatasetAnalysisApi(api_client)
    dataset_id = 56 # int | 

    try:
        # Delete all tags of a dataset from database
        api_instance.delete_tags(dataset_id)
    except Exception as e:
        print("Exception when calling DatasetAnalysisApi->delete_tags: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dataset_id** | **int**|  | 

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

# **get_analysis_types**
> List[str] get_analysis_types()

Get a list of all supported analysis types

### Example


```python
import pprl_data_owner_service_api_client
from pprl_data_owner_service_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8181
# See configuration.py for a list of all supported configuration parameters.
configuration = pprl_data_owner_service_api_client.Configuration(
    host = "http://localhost:8181"
)


# Enter a context with an instance of the API client
with pprl_data_owner_service_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pprl_data_owner_service_api_client.DatasetAnalysisApi(api_client)

    try:
        # Get a list of all supported analysis types
        api_response = api_instance.get_analysis_types()
        print("The response of DatasetAnalysisApi->get_analysis_types:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatasetAnalysisApi->get_analysis_types: %s\n" % e)
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

# **get_tags**
> List[Tag] get_tags(dataset_id)

Get tags from database

### Example


```python
import pprl_data_owner_service_api_client
from pprl_data_owner_service_api_client.models.tag import Tag
from pprl_data_owner_service_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8181
# See configuration.py for a list of all supported configuration parameters.
configuration = pprl_data_owner_service_api_client.Configuration(
    host = "http://localhost:8181"
)


# Enter a context with an instance of the API client
with pprl_data_owner_service_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pprl_data_owner_service_api_client.DatasetAnalysisApi(api_client)
    dataset_id = 56 # int | 

    try:
        # Get tags from database
        api_response = api_instance.get_tags(dataset_id)
        print("The response of DatasetAnalysisApi->get_tags:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatasetAnalysisApi->get_tags: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dataset_id** | **int**|  | 

### Return type

[**List[Tag]**](Tag.md)

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

# **get_tags_by_origin**
> List[Tag] get_tags_by_origin(dataset_id, origin)

Get tags from database

### Example


```python
import pprl_data_owner_service_api_client
from pprl_data_owner_service_api_client.models.tag import Tag
from pprl_data_owner_service_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8181
# See configuration.py for a list of all supported configuration parameters.
configuration = pprl_data_owner_service_api_client.Configuration(
    host = "http://localhost:8181"
)


# Enter a context with an instance of the API client
with pprl_data_owner_service_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pprl_data_owner_service_api_client.DatasetAnalysisApi(api_client)
    dataset_id = 56 # int | 
    origin = 'origin_example' # str | 

    try:
        # Get tags from database
        api_response = api_instance.get_tags_by_origin(dataset_id, origin)
        print("The response of DatasetAnalysisApi->get_tags_by_origin:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatasetAnalysisApi->get_tags_by_origin: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dataset_id** | **int**|  | 
 **origin** | **str**|  | 

### Return type

[**List[Tag]**](Tag.md)

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

# **run_analysis**
> AnalysisResultDto run_analysis(analysis_request_dto)

Run a specific analysis type

### Example


```python
import pprl_data_owner_service_api_client
from pprl_data_owner_service_api_client.models.analysis_request_dto import AnalysisRequestDto
from pprl_data_owner_service_api_client.models.analysis_result_dto import AnalysisResultDto
from pprl_data_owner_service_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8181
# See configuration.py for a list of all supported configuration parameters.
configuration = pprl_data_owner_service_api_client.Configuration(
    host = "http://localhost:8181"
)


# Enter a context with an instance of the API client
with pprl_data_owner_service_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pprl_data_owner_service_api_client.DatasetAnalysisApi(api_client)
    analysis_request_dto = pprl_data_owner_service_api_client.AnalysisRequestDto() # AnalysisRequestDto | 

    try:
        # Run a specific analysis type
        api_response = api_instance.run_analysis(analysis_request_dto)
        print("The response of DatasetAnalysisApi->run_analysis:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatasetAnalysisApi->run_analysis: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **analysis_request_dto** | [**AnalysisRequestDto**](AnalysisRequestDto.md)|  | 

### Return type

[**AnalysisResultDto**](AnalysisResultDto.md)

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

# **run_pair_analysis**
> List[Tag] run_pair_analysis(dataset_id, record_id_pair_dto)

Get tags for pairs

### Example


```python
import pprl_data_owner_service_api_client
from pprl_data_owner_service_api_client.models.record_id_pair_dto import RecordIdPairDto
from pprl_data_owner_service_api_client.models.tag import Tag
from pprl_data_owner_service_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8181
# See configuration.py for a list of all supported configuration parameters.
configuration = pprl_data_owner_service_api_client.Configuration(
    host = "http://localhost:8181"
)


# Enter a context with an instance of the API client
with pprl_data_owner_service_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pprl_data_owner_service_api_client.DatasetAnalysisApi(api_client)
    dataset_id = 56 # int | 
    record_id_pair_dto = [pprl_data_owner_service_api_client.RecordIdPairDto()] # List[RecordIdPairDto] | 

    try:
        # Get tags for pairs
        api_response = api_instance.run_pair_analysis(dataset_id, record_id_pair_dto)
        print("The response of DatasetAnalysisApi->run_pair_analysis:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatasetAnalysisApi->run_pair_analysis: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dataset_id** | **int**|  | 
 **record_id_pair_dto** | [**List[RecordIdPairDto]**](RecordIdPairDto.md)|  | 

### Return type

[**List[Tag]**](Tag.md)

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

# **run_validation_analysis**
> AnalysisResultDto run_validation_analysis(analysis_request_dto)

Run a specific analysis type

### Example


```python
import pprl_data_owner_service_api_client
from pprl_data_owner_service_api_client.models.analysis_request_dto import AnalysisRequestDto
from pprl_data_owner_service_api_client.models.analysis_result_dto import AnalysisResultDto
from pprl_data_owner_service_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8181
# See configuration.py for a list of all supported configuration parameters.
configuration = pprl_data_owner_service_api_client.Configuration(
    host = "http://localhost:8181"
)


# Enter a context with an instance of the API client
with pprl_data_owner_service_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pprl_data_owner_service_api_client.DatasetAnalysisApi(api_client)
    analysis_request_dto = pprl_data_owner_service_api_client.AnalysisRequestDto() # AnalysisRequestDto | 

    try:
        # Run a specific analysis type
        api_response = api_instance.run_validation_analysis(analysis_request_dto)
        print("The response of DatasetAnalysisApi->run_validation_analysis:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatasetAnalysisApi->run_validation_analysis: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **analysis_request_dto** | [**AnalysisRequestDto**](AnalysisRequestDto.md)|  | 

### Return type

[**AnalysisResultDto**](AnalysisResultDto.md)

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

# **save_tags**
> save_tags(dataset_id, tag)

Add tags to database

### Example


```python
import pprl_data_owner_service_api_client
from pprl_data_owner_service_api_client.models.tag import Tag
from pprl_data_owner_service_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8181
# See configuration.py for a list of all supported configuration parameters.
configuration = pprl_data_owner_service_api_client.Configuration(
    host = "http://localhost:8181"
)


# Enter a context with an instance of the API client
with pprl_data_owner_service_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pprl_data_owner_service_api_client.DatasetAnalysisApi(api_client)
    dataset_id = 56 # int | 
    tag = [pprl_data_owner_service_api_client.Tag()] # List[Tag] | 

    try:
        # Add tags to database
        api_instance.save_tags(dataset_id, tag)
    except Exception as e:
        print("Exception when calling DatasetAnalysisApi->save_tags: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dataset_id** | **int**|  | 
 **tag** | [**List[Tag]**](Tag.md)|  | 

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

