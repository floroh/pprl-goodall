# pprl_data_owner_service_api_client.EncoderApi

All URIs are relative to *http://localhost:8081*

Method | HTTP request | Description
------------- | ------------- | -------------
[**encode**](EncoderApi.md#encode) | **POST** /record/{uniqueId}/encode | Encode a persisted record
[**encode_multiple**](EncoderApi.md#encode_multiple) | **POST** /record/encode-multiple | Bundled encoding requests for multiple persisted records
[**encode_multiple_same**](EncoderApi.md#encode_multiple_same) | **POST** /record/encode-multiple-same | Encode multiple persisted records with the same encoding


# **encode**
> RecordDto encode(unique_id, encoding_request_dto)

Encode a persisted record

### Example


```python
import pprl_data_owner_service_api_client
from pprl_data_owner_service_api_client.models.encoding_request_dto import EncodingRequestDto
from pprl_data_owner_service_api_client.models.record_dto import RecordDto
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
    api_instance = pprl_data_owner_service_api_client.EncoderApi(api_client)
    unique_id = 'unique_id_example' # str | 
    encoding_request_dto = pprl_data_owner_service_api_client.EncodingRequestDto() # EncodingRequestDto | 

    try:
        # Encode a persisted record
        api_response = api_instance.encode(unique_id, encoding_request_dto)
        print("The response of EncoderApi->encode:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling EncoderApi->encode: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **unique_id** | **str**|  | 
 **encoding_request_dto** | [**EncodingRequestDto**](EncodingRequestDto.md)|  | 

### Return type

[**RecordDto**](RecordDto.md)

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

# **encode_multiple**
> List[RecordDto] encode_multiple(encoding_retrieval_request_dto)

Bundled encoding requests for multiple persisted records

### Example


```python
import pprl_data_owner_service_api_client
from pprl_data_owner_service_api_client.models.encoding_retrieval_request_dto import EncodingRetrievalRequestDto
from pprl_data_owner_service_api_client.models.record_dto import RecordDto
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
    api_instance = pprl_data_owner_service_api_client.EncoderApi(api_client)
    encoding_retrieval_request_dto = [pprl_data_owner_service_api_client.EncodingRetrievalRequestDto()] # List[EncodingRetrievalRequestDto] | 

    try:
        # Bundled encoding requests for multiple persisted records
        api_response = api_instance.encode_multiple(encoding_retrieval_request_dto)
        print("The response of EncoderApi->encode_multiple:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling EncoderApi->encode_multiple: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **encoding_retrieval_request_dto** | [**List[EncodingRetrievalRequestDto]**](EncodingRetrievalRequestDto.md)|  | 

### Return type

[**List[RecordDto]**](RecordDto.md)

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

# **encode_multiple_same**
> List[RecordDto] encode_multiple_same(multi_record_encoding_retrieval_request_dto)

Encode multiple persisted records with the same encoding

### Example


```python
import pprl_data_owner_service_api_client
from pprl_data_owner_service_api_client.models.multi_record_encoding_retrieval_request_dto import MultiRecordEncodingRetrievalRequestDto
from pprl_data_owner_service_api_client.models.record_dto import RecordDto
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
    api_instance = pprl_data_owner_service_api_client.EncoderApi(api_client)
    multi_record_encoding_retrieval_request_dto = pprl_data_owner_service_api_client.MultiRecordEncodingRetrievalRequestDto() # MultiRecordEncodingRetrievalRequestDto | 

    try:
        # Encode multiple persisted records with the same encoding
        api_response = api_instance.encode_multiple_same(multi_record_encoding_retrieval_request_dto)
        print("The response of EncoderApi->encode_multiple_same:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling EncoderApi->encode_multiple_same: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **multi_record_encoding_retrieval_request_dto** | [**MultiRecordEncodingRetrievalRequestDto**](MultiRecordEncodingRetrievalRequestDto.md)|  | 

### Return type

[**List[RecordDto]**](RecordDto.md)

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

