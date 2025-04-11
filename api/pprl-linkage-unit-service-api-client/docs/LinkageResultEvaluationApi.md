# pprl_linkage_unit_service_api_client.LinkageResultEvaluationApi

All URIs are relative to *http://localhost:8082*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_ground_truth**](LinkageResultEvaluationApi.md#add_ground_truth) | **POST** /evaluation/ground-truth | Add ground truth for a dataset
[**add_ground_truth_from_global_ids**](LinkageResultEvaluationApi.md#add_ground_truth_from_global_ids) | **POST** /evaluation/ground-truth/{datasetId} | Add ground truth for a dataset based on record global ids
[**fetch**](LinkageResultEvaluationApi.md#fetch) | **GET** /evaluation/ground-truth/{datasetId} | Get ground truth for a dataset
[**fit**](LinkageResultEvaluationApi.md#fit) | **POST** /evaluation/matcher/fit | Fit a matcher for a dataset with ground truth


# **add_ground_truth**
> add_ground_truth(ground_truth_dto)

Add ground truth for a dataset

### Example


```python
import pprl_linkage_unit_service_api_client
from pprl_linkage_unit_service_api_client.models.ground_truth_dto import GroundTruthDto
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
    api_instance = pprl_linkage_unit_service_api_client.LinkageResultEvaluationApi(api_client)
    ground_truth_dto = pprl_linkage_unit_service_api_client.GroundTruthDto() # GroundTruthDto | 

    try:
        # Add ground truth for a dataset
        api_instance.add_ground_truth(ground_truth_dto)
    except Exception as e:
        print("Exception when calling LinkageResultEvaluationApi->add_ground_truth: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ground_truth_dto** | [**GroundTruthDto**](GroundTruthDto.md)|  | 

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

# **add_ground_truth_from_global_ids**
> add_ground_truth_from_global_ids(dataset_id, record_id_dto)

Add ground truth for a dataset based on record global ids

### Example


```python
import pprl_linkage_unit_service_api_client
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
    api_instance = pprl_linkage_unit_service_api_client.LinkageResultEvaluationApi(api_client)
    dataset_id = 56 # int | 
    record_id_dto = [pprl_linkage_unit_service_api_client.RecordIdDto()] # List[RecordIdDto] | 

    try:
        # Add ground truth for a dataset based on record global ids
        api_instance.add_ground_truth_from_global_ids(dataset_id, record_id_dto)
    except Exception as e:
        print("Exception when calling LinkageResultEvaluationApi->add_ground_truth_from_global_ids: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dataset_id** | **int**|  | 
 **record_id_dto** | [**List[RecordIdDto]**](RecordIdDto.md)|  | 

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

# **fetch**
> GroundTruthDto fetch(dataset_id)

Get ground truth for a dataset

### Example


```python
import pprl_linkage_unit_service_api_client
from pprl_linkage_unit_service_api_client.models.ground_truth_dto import GroundTruthDto
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
    api_instance = pprl_linkage_unit_service_api_client.LinkageResultEvaluationApi(api_client)
    dataset_id = 56 # int | 

    try:
        # Get ground truth for a dataset
        api_response = api_instance.fetch(dataset_id)
        print("The response of LinkageResultEvaluationApi->fetch:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LinkageResultEvaluationApi->fetch: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dataset_id** | **int**|  | 

### Return type

[**GroundTruthDto**](GroundTruthDto.md)

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

# **fit**
> MatchingDto fit(matcher_trainings_request)

Fit a matcher for a dataset with ground truth

### Example


```python
import pprl_linkage_unit_service_api_client
from pprl_linkage_unit_service_api_client.models.matcher_trainings_request import MatcherTrainingsRequest
from pprl_linkage_unit_service_api_client.models.matching_dto import MatchingDto
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
    api_instance = pprl_linkage_unit_service_api_client.LinkageResultEvaluationApi(api_client)
    matcher_trainings_request = pprl_linkage_unit_service_api_client.MatcherTrainingsRequest() # MatcherTrainingsRequest | 

    try:
        # Fit a matcher for a dataset with ground truth
        api_response = api_instance.fit(matcher_trainings_request)
        print("The response of LinkageResultEvaluationApi->fit:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LinkageResultEvaluationApi->fit: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **matcher_trainings_request** | [**MatcherTrainingsRequest**](MatcherTrainingsRequest.md)|  | 

### Return type

[**MatchingDto**](MatchingDto.md)

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

