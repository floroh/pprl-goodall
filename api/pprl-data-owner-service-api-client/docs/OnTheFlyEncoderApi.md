# pprl_data_owner_service_api_client.OnTheFlyEncoderApi

All URIs are relative to *http://localhost:8081*

Method | HTTP request | Description
------------- | ------------- | -------------
[**encode1**](OnTheFlyEncoderApi.md#encode1) | **POST** /encode | Encode a single record
[**encode_multiple_same1**](OnTheFlyEncoderApi.md#encode_multiple_same1) | **POST** /encode-multiple-same | Encode multiple records with the same encoding


# **encode1**
> RecordDto encode1(encoding_request_dto)

Encode a single record

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
    api_instance = pprl_data_owner_service_api_client.OnTheFlyEncoderApi(api_client)
    encoding_request_dto = pprl_data_owner_service_api_client.EncodingRequestDto() # EncodingRequestDto | 

    try:
        # Encode a single record
        api_response = api_instance.encode1(encoding_request_dto)
        print("The response of OnTheFlyEncoderApi->encode1:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OnTheFlyEncoderApi->encode1: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
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

# **encode_multiple_same1**
> List[RecordDto] encode_multiple_same1(multi_record_encoding_request_dto)

Encode multiple records with the same encoding

### Example


```python
import pprl_data_owner_service_api_client
from pprl_data_owner_service_api_client.models.multi_record_encoding_request_dto import MultiRecordEncodingRequestDto
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
    api_instance = pprl_data_owner_service_api_client.OnTheFlyEncoderApi(api_client)
    multi_record_encoding_request_dto = pprl_data_owner_service_api_client.MultiRecordEncodingRequestDto() # MultiRecordEncodingRequestDto | 

    try:
        # Encode multiple records with the same encoding
        api_response = api_instance.encode_multiple_same1(multi_record_encoding_request_dto)
        print("The response of OnTheFlyEncoderApi->encode_multiple_same1:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OnTheFlyEncoderApi->encode_multiple_same1: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **multi_record_encoding_request_dto** | [**MultiRecordEncodingRequestDto**](MultiRecordEncodingRequestDto.md)|  | 

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

