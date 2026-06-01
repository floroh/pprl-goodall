# pprl_protocol_manager_service_api_client.ProtocolAnalyzerApi

All URIs are relative to *http://localhost:8185*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_tags_from_protocol**](ProtocolAnalyzerApi.md#get_tags_from_protocol) | **POST** /analyzer/tag-collection | Get all tags for an executed protocol
[**get_tags_from_protocol_as_table**](ProtocolAnalyzerApi.md#get_tags_from_protocol_as_table) | **POST** /analyzer/tag-table | Get all tags for an executed protocol in table format


# **get_tags_from_protocol**
> List[Tag] get_tags_from_protocol(protocol_analysis_request_dto)

Get all tags for an executed protocol

### Example


```python
import pprl_protocol_manager_service_api_client
from pprl_protocol_manager_service_api_client.models.protocol_analysis_request_dto import ProtocolAnalysisRequestDto
from pprl_protocol_manager_service_api_client.models.tag import Tag
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
    api_instance = pprl_protocol_manager_service_api_client.ProtocolAnalyzerApi(api_client)
    protocol_analysis_request_dto = pprl_protocol_manager_service_api_client.ProtocolAnalysisRequestDto() # ProtocolAnalysisRequestDto | 

    try:
        # Get all tags for an executed protocol
        api_response = api_instance.get_tags_from_protocol(protocol_analysis_request_dto)
        print("The response of ProtocolAnalyzerApi->get_tags_from_protocol:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProtocolAnalyzerApi->get_tags_from_protocol: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **protocol_analysis_request_dto** | [**ProtocolAnalysisRequestDto**](ProtocolAnalysisRequestDto.md)|  | 

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

# **get_tags_from_protocol_as_table**
> SerializableTable get_tags_from_protocol_as_table(protocol_analysis_request_dto)

Get all tags for an executed protocol in table format

### Example


```python
import pprl_protocol_manager_service_api_client
from pprl_protocol_manager_service_api_client.models.protocol_analysis_request_dto import ProtocolAnalysisRequestDto
from pprl_protocol_manager_service_api_client.models.serializable_table import SerializableTable
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
    api_instance = pprl_protocol_manager_service_api_client.ProtocolAnalyzerApi(api_client)
    protocol_analysis_request_dto = pprl_protocol_manager_service_api_client.ProtocolAnalysisRequestDto() # ProtocolAnalysisRequestDto | 

    try:
        # Get all tags for an executed protocol in table format
        api_response = api_instance.get_tags_from_protocol_as_table(protocol_analysis_request_dto)
        print("The response of ProtocolAnalyzerApi->get_tags_from_protocol_as_table:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProtocolAnalyzerApi->get_tags_from_protocol_as_table: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **protocol_analysis_request_dto** | [**ProtocolAnalysisRequestDto**](ProtocolAnalysisRequestDto.md)|  | 

### Return type

[**SerializableTable**](SerializableTable.md)

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

