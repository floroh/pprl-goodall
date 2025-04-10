# pprl_data_owner_service_api_client.DatasetAnalysisApi

All URIs are relative to *http://localhost:8081*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_analysis_types**](DatasetAnalysisApi.md#get_analysis_types) | **GET** /analysis/findAll | Get a list of all supported analysis types
[**run_analysis**](DatasetAnalysisApi.md#run_analysis) | **POST** /analysis/run | Run a specific analysis type
[**run_validation_analysis**](DatasetAnalysisApi.md#run_validation_analysis) | **POST** /analysis/runValidation | Run a specific analysis type


# **get_analysis_types**
> List[str] get_analysis_types()

Get a list of all supported analysis types

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

# Defining the host is optional and defaults to http://localhost:8081
# See configuration.py for a list of all supported configuration parameters.
configuration = pprl_data_owner_service_api_client.Configuration(
    host = "http://localhost:8081"
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

# Defining the host is optional and defaults to http://localhost:8081
# See configuration.py for a list of all supported configuration parameters.
configuration = pprl_data_owner_service_api_client.Configuration(
    host = "http://localhost:8081"
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

