# pprl_linkage_unit_service_api_client.LinkageResultAnalysisApi

All URIs are relative to *http://localhost:8082*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_pairs**](LinkageResultAnalysisApi.md#get_pairs) | **POST** /analysis/pairs | Get record pairs
[**run_linkage_result_analysis**](LinkageResultAnalysisApi.md#run_linkage_result_analysis) | **POST** /analysis/eval | Run a specific linkage result analysis type
[**run_validation_analysis**](LinkageResultAnalysisApi.md#run_validation_analysis) | **POST** /analysis/runValidation | Run a specific dataset analysis type


# **get_pairs**
> List[RecordPairDto] get_pairs(result_request)

Get record pairs

### Example


```python
import pprl_linkage_unit_service_api_client
from pprl_linkage_unit_service_api_client.models.record_pair_dto import RecordPairDto
from pprl_linkage_unit_service_api_client.models.result_request import ResultRequest
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
    api_instance = pprl_linkage_unit_service_api_client.LinkageResultAnalysisApi(api_client)
    result_request = pprl_linkage_unit_service_api_client.ResultRequest() # ResultRequest | 

    try:
        # Get record pairs
        api_response = api_instance.get_pairs(result_request)
        print("The response of LinkageResultAnalysisApi->get_pairs:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LinkageResultAnalysisApi->get_pairs: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **result_request** | [**ResultRequest**](ResultRequest.md)|  | 

### Return type

[**List[RecordPairDto]**](RecordPairDto.md)

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

# **run_linkage_result_analysis**
> AnalysisResultDto run_linkage_result_analysis(match_result_analysis_request_dto)

Run a specific linkage result analysis type

### Example


```python
import pprl_linkage_unit_service_api_client
from pprl_linkage_unit_service_api_client.models.analysis_result_dto import AnalysisResultDto
from pprl_linkage_unit_service_api_client.models.match_result_analysis_request_dto import MatchResultAnalysisRequestDto
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
    api_instance = pprl_linkage_unit_service_api_client.LinkageResultAnalysisApi(api_client)
    match_result_analysis_request_dto = pprl_linkage_unit_service_api_client.MatchResultAnalysisRequestDto() # MatchResultAnalysisRequestDto | 

    try:
        # Run a specific linkage result analysis type
        api_response = api_instance.run_linkage_result_analysis(match_result_analysis_request_dto)
        print("The response of LinkageResultAnalysisApi->run_linkage_result_analysis:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LinkageResultAnalysisApi->run_linkage_result_analysis: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **match_result_analysis_request_dto** | [**MatchResultAnalysisRequestDto**](MatchResultAnalysisRequestDto.md)|  | 

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

Run a specific dataset analysis type

### Example


```python
import pprl_linkage_unit_service_api_client
from pprl_linkage_unit_service_api_client.models.analysis_request_dto import AnalysisRequestDto
from pprl_linkage_unit_service_api_client.models.analysis_result_dto import AnalysisResultDto
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
    api_instance = pprl_linkage_unit_service_api_client.LinkageResultAnalysisApi(api_client)
    analysis_request_dto = pprl_linkage_unit_service_api_client.AnalysisRequestDto() # AnalysisRequestDto | 

    try:
        # Run a specific dataset analysis type
        api_response = api_instance.run_validation_analysis(analysis_request_dto)
        print("The response of LinkageResultAnalysisApi->run_validation_analysis:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LinkageResultAnalysisApi->run_validation_analysis: %s\n" % e)
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

