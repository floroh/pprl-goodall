# pprl_linkage_unit_service_api_client.TransientBatchMatchingApi

All URIs are relative to *http://localhost:8082*

Method | HTTP request | Description
------------- | ------------- | -------------
[**cluster**](TransientBatchMatchingApi.md#cluster) | **POST** /batch/cluster | Cluster and assign global IDs based on precomputed links
[**match**](TransientBatchMatchingApi.md#match) | **POST** /batch/match | Batch matcher


# **cluster**
> MatchResultDto cluster(clustering_request_dto)

Cluster and assign global IDs based on precomputed links

### Example


```python
import pprl_linkage_unit_service_api_client
from pprl_linkage_unit_service_api_client.models.clustering_request_dto import ClusteringRequestDto
from pprl_linkage_unit_service_api_client.models.match_result_dto import MatchResultDto
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
    api_instance = pprl_linkage_unit_service_api_client.TransientBatchMatchingApi(api_client)
    clustering_request_dto = pprl_linkage_unit_service_api_client.ClusteringRequestDto() # ClusteringRequestDto | 

    try:
        # Cluster and assign global IDs based on precomputed links
        api_response = api_instance.cluster(clustering_request_dto)
        print("The response of TransientBatchMatchingApi->cluster:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TransientBatchMatchingApi->cluster: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **clustering_request_dto** | [**ClusteringRequestDto**](ClusteringRequestDto.md)|  | 

### Return type

[**MatchResultDto**](MatchResultDto.md)

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

# **match**
> MatchResultDto match(batch_match_request_dto)

Batch matcher

### Example


```python
import pprl_linkage_unit_service_api_client
from pprl_linkage_unit_service_api_client.models.batch_match_request_dto import BatchMatchRequestDto
from pprl_linkage_unit_service_api_client.models.match_result_dto import MatchResultDto
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
    api_instance = pprl_linkage_unit_service_api_client.TransientBatchMatchingApi(api_client)
    batch_match_request_dto = pprl_linkage_unit_service_api_client.BatchMatchRequestDto() # BatchMatchRequestDto | 

    try:
        # Batch matcher
        api_response = api_instance.match(batch_match_request_dto)
        print("The response of TransientBatchMatchingApi->match:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TransientBatchMatchingApi->match: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **batch_match_request_dto** | [**BatchMatchRequestDto**](BatchMatchRequestDto.md)|  | 

### Return type

[**MatchResultDto**](MatchResultDto.md)

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

