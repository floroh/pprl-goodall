# pprl_protocol_manager_service_api_client.PPRLProtocolManagerApi

All URIs are relative to *http://localhost:8085*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_multi_layer_protocol**](PPRLProtocolManagerApi.md#create_multi_layer_protocol) | **POST** /protocol/multi-layer | Create a new multilayer protocol definition
[**delete_all**](PPRLProtocolManagerApi.md#delete_all) | **DELETE** /protocol/multi-layer/all | Delete all protocols
[**delete_multi_layer_protocol**](PPRLProtocolManagerApi.md#delete_multi_layer_protocol) | **DELETE** /protocol/multi-layer/{protocolId} | Delete a new multilayer protocol
[**find_all**](PPRLProtocolManagerApi.md#find_all) | **GET** /protocol/multi-layer/findAll | Get all multilayer protocol definitions
[**get_example_multi_layer_protocol**](PPRLProtocolManagerApi.md#get_example_multi_layer_protocol) | **GET** /protocol/multi-layer/example/{protocolType} | Get an example multilayer protocol definition
[**get_multi_layer_protocol**](PPRLProtocolManagerApi.md#get_multi_layer_protocol) | **GET** /protocol/multi-layer/{protocolId} | Get a multilayer protocol definition
[**run_multi_layer_protocol**](PPRLProtocolManagerApi.md#run_multi_layer_protocol) | **POST** /protocol/multi-layer/run | Run a multilayer protocol
[**skip_step_of_multi_layer_protocol**](PPRLProtocolManagerApi.md#skip_step_of_multi_layer_protocol) | **POST** /protocol/multi-layer/skip/{protocolId} | Skip next step of a multilayer protocol
[**transfer_encoded**](PPRLProtocolManagerApi.md#transfer_encoded) | **POST** /protocol/transfer/dataset | Transfer an encoded dataset
[**update_multi_layer_protocol**](PPRLProtocolManagerApi.md#update_multi_layer_protocol) | **PUT** /protocol/multi-layer | Update a new multilayer protocol definition


# **create_multi_layer_protocol**
> MultiLayerProtocol create_multi_layer_protocol(multi_layer_protocol)

Create a new multilayer protocol definition

### Example


```python
import pprl_protocol_manager_service_api_client
from pprl_protocol_manager_service_api_client.models.multi_layer_protocol import MultiLayerProtocol
from pprl_protocol_manager_service_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8085
# See configuration.py for a list of all supported configuration parameters.
configuration = pprl_protocol_manager_service_api_client.Configuration(
    host = "http://localhost:8085"
)


# Enter a context with an instance of the API client
with pprl_protocol_manager_service_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pprl_protocol_manager_service_api_client.PPRLProtocolManagerApi(api_client)
    multi_layer_protocol = pprl_protocol_manager_service_api_client.MultiLayerProtocol() # MultiLayerProtocol | 

    try:
        # Create a new multilayer protocol definition
        api_response = api_instance.create_multi_layer_protocol(multi_layer_protocol)
        print("The response of PPRLProtocolManagerApi->create_multi_layer_protocol:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PPRLProtocolManagerApi->create_multi_layer_protocol: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **multi_layer_protocol** | [**MultiLayerProtocol**](MultiLayerProtocol.md)|  | 

### Return type

[**MultiLayerProtocol**](MultiLayerProtocol.md)

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

# **delete_all**
> delete_all()

Delete all protocols

### Example


```python
import pprl_protocol_manager_service_api_client
from pprl_protocol_manager_service_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8085
# See configuration.py for a list of all supported configuration parameters.
configuration = pprl_protocol_manager_service_api_client.Configuration(
    host = "http://localhost:8085"
)


# Enter a context with an instance of the API client
with pprl_protocol_manager_service_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pprl_protocol_manager_service_api_client.PPRLProtocolManagerApi(api_client)

    try:
        # Delete all protocols
        api_instance.delete_all()
    except Exception as e:
        print("Exception when calling PPRLProtocolManagerApi->delete_all: %s\n" % e)
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

# **delete_multi_layer_protocol**
> delete_multi_layer_protocol(protocol_id)

Delete a new multilayer protocol

### Example


```python
import pprl_protocol_manager_service_api_client
from pprl_protocol_manager_service_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8085
# See configuration.py for a list of all supported configuration parameters.
configuration = pprl_protocol_manager_service_api_client.Configuration(
    host = "http://localhost:8085"
)


# Enter a context with an instance of the API client
with pprl_protocol_manager_service_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pprl_protocol_manager_service_api_client.PPRLProtocolManagerApi(api_client)
    protocol_id = 'protocol_id_example' # str | 

    try:
        # Delete a new multilayer protocol
        api_instance.delete_multi_layer_protocol(protocol_id)
    except Exception as e:
        print("Exception when calling PPRLProtocolManagerApi->delete_multi_layer_protocol: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **protocol_id** | **str**|  | 

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
> List[MultiLayerProtocol] find_all()

Get all multilayer protocol definitions

### Example


```python
import pprl_protocol_manager_service_api_client
from pprl_protocol_manager_service_api_client.models.multi_layer_protocol import MultiLayerProtocol
from pprl_protocol_manager_service_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8085
# See configuration.py for a list of all supported configuration parameters.
configuration = pprl_protocol_manager_service_api_client.Configuration(
    host = "http://localhost:8085"
)


# Enter a context with an instance of the API client
with pprl_protocol_manager_service_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pprl_protocol_manager_service_api_client.PPRLProtocolManagerApi(api_client)

    try:
        # Get all multilayer protocol definitions
        api_response = api_instance.find_all()
        print("The response of PPRLProtocolManagerApi->find_all:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PPRLProtocolManagerApi->find_all: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[MultiLayerProtocol]**](MultiLayerProtocol.md)

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

# **get_example_multi_layer_protocol**
> MultiLayerProtocol get_example_multi_layer_protocol(protocol_type)

Get an example multilayer protocol definition

### Example


```python
import pprl_protocol_manager_service_api_client
from pprl_protocol_manager_service_api_client.models.multi_layer_protocol import MultiLayerProtocol
from pprl_protocol_manager_service_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8085
# See configuration.py for a list of all supported configuration parameters.
configuration = pprl_protocol_manager_service_api_client.Configuration(
    host = "http://localhost:8085"
)


# Enter a context with an instance of the API client
with pprl_protocol_manager_service_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pprl_protocol_manager_service_api_client.PPRLProtocolManagerApi(api_client)
    protocol_type = 'protocol_type_example' # str | 

    try:
        # Get an example multilayer protocol definition
        api_response = api_instance.get_example_multi_layer_protocol(protocol_type)
        print("The response of PPRLProtocolManagerApi->get_example_multi_layer_protocol:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PPRLProtocolManagerApi->get_example_multi_layer_protocol: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **protocol_type** | **str**|  | 

### Return type

[**MultiLayerProtocol**](MultiLayerProtocol.md)

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

# **get_multi_layer_protocol**
> MultiLayerProtocol get_multi_layer_protocol(protocol_id)

Get a multilayer protocol definition

### Example


```python
import pprl_protocol_manager_service_api_client
from pprl_protocol_manager_service_api_client.models.multi_layer_protocol import MultiLayerProtocol
from pprl_protocol_manager_service_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8085
# See configuration.py for a list of all supported configuration parameters.
configuration = pprl_protocol_manager_service_api_client.Configuration(
    host = "http://localhost:8085"
)


# Enter a context with an instance of the API client
with pprl_protocol_manager_service_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pprl_protocol_manager_service_api_client.PPRLProtocolManagerApi(api_client)
    protocol_id = 'protocol_id_example' # str | 

    try:
        # Get a multilayer protocol definition
        api_response = api_instance.get_multi_layer_protocol(protocol_id)
        print("The response of PPRLProtocolManagerApi->get_multi_layer_protocol:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PPRLProtocolManagerApi->get_multi_layer_protocol: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **protocol_id** | **str**|  | 

### Return type

[**MultiLayerProtocol**](MultiLayerProtocol.md)

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

# **run_multi_layer_protocol**
> MultiLayerProtocol run_multi_layer_protocol(protocol_execution_dto)

Run a multilayer protocol

### Example


```python
import pprl_protocol_manager_service_api_client
from pprl_protocol_manager_service_api_client.models.multi_layer_protocol import MultiLayerProtocol
from pprl_protocol_manager_service_api_client.models.protocol_execution_dto import ProtocolExecutionDto
from pprl_protocol_manager_service_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8085
# See configuration.py for a list of all supported configuration parameters.
configuration = pprl_protocol_manager_service_api_client.Configuration(
    host = "http://localhost:8085"
)


# Enter a context with an instance of the API client
with pprl_protocol_manager_service_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pprl_protocol_manager_service_api_client.PPRLProtocolManagerApi(api_client)
    protocol_execution_dto = pprl_protocol_manager_service_api_client.ProtocolExecutionDto() # ProtocolExecutionDto | 

    try:
        # Run a multilayer protocol
        api_response = api_instance.run_multi_layer_protocol(protocol_execution_dto)
        print("The response of PPRLProtocolManagerApi->run_multi_layer_protocol:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PPRLProtocolManagerApi->run_multi_layer_protocol: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **protocol_execution_dto** | [**ProtocolExecutionDto**](ProtocolExecutionDto.md)|  | 

### Return type

[**MultiLayerProtocol**](MultiLayerProtocol.md)

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

# **skip_step_of_multi_layer_protocol**
> MultiLayerProtocol skip_step_of_multi_layer_protocol(protocol_id)

Skip next step of a multilayer protocol

### Example


```python
import pprl_protocol_manager_service_api_client
from pprl_protocol_manager_service_api_client.models.multi_layer_protocol import MultiLayerProtocol
from pprl_protocol_manager_service_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8085
# See configuration.py for a list of all supported configuration parameters.
configuration = pprl_protocol_manager_service_api_client.Configuration(
    host = "http://localhost:8085"
)


# Enter a context with an instance of the API client
with pprl_protocol_manager_service_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pprl_protocol_manager_service_api_client.PPRLProtocolManagerApi(api_client)
    protocol_id = 'protocol_id_example' # str | 

    try:
        # Skip next step of a multilayer protocol
        api_response = api_instance.skip_step_of_multi_layer_protocol(protocol_id)
        print("The response of PPRLProtocolManagerApi->skip_step_of_multi_layer_protocol:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PPRLProtocolManagerApi->skip_step_of_multi_layer_protocol: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **protocol_id** | **str**|  | 

### Return type

[**MultiLayerProtocol**](MultiLayerProtocol.md)

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

# **transfer_encoded**
> int transfer_encoded(encoded_transfer_request_dto)

Transfer an encoded dataset

### Example


```python
import pprl_protocol_manager_service_api_client
from pprl_protocol_manager_service_api_client.models.encoded_transfer_request_dto import EncodedTransferRequestDto
from pprl_protocol_manager_service_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8085
# See configuration.py for a list of all supported configuration parameters.
configuration = pprl_protocol_manager_service_api_client.Configuration(
    host = "http://localhost:8085"
)


# Enter a context with an instance of the API client
with pprl_protocol_manager_service_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pprl_protocol_manager_service_api_client.PPRLProtocolManagerApi(api_client)
    encoded_transfer_request_dto = pprl_protocol_manager_service_api_client.EncodedTransferRequestDto() # EncodedTransferRequestDto | 

    try:
        # Transfer an encoded dataset
        api_response = api_instance.transfer_encoded(encoded_transfer_request_dto)
        print("The response of PPRLProtocolManagerApi->transfer_encoded:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PPRLProtocolManagerApi->transfer_encoded: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **encoded_transfer_request_dto** | [**EncodedTransferRequestDto**](EncodedTransferRequestDto.md)|  | 

### Return type

**int**

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

# **update_multi_layer_protocol**
> MultiLayerProtocol update_multi_layer_protocol(multi_layer_protocol)

Update a new multilayer protocol definition

### Example


```python
import pprl_protocol_manager_service_api_client
from pprl_protocol_manager_service_api_client.models.multi_layer_protocol import MultiLayerProtocol
from pprl_protocol_manager_service_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8085
# See configuration.py for a list of all supported configuration parameters.
configuration = pprl_protocol_manager_service_api_client.Configuration(
    host = "http://localhost:8085"
)


# Enter a context with an instance of the API client
with pprl_protocol_manager_service_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pprl_protocol_manager_service_api_client.PPRLProtocolManagerApi(api_client)
    multi_layer_protocol = pprl_protocol_manager_service_api_client.MultiLayerProtocol() # MultiLayerProtocol | 

    try:
        # Update a new multilayer protocol definition
        api_response = api_instance.update_multi_layer_protocol(multi_layer_protocol)
        print("The response of PPRLProtocolManagerApi->update_multi_layer_protocol:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PPRLProtocolManagerApi->update_multi_layer_protocol: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **multi_layer_protocol** | [**MultiLayerProtocol**](MultiLayerProtocol.md)|  | 

### Return type

[**MultiLayerProtocol**](MultiLayerProtocol.md)

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

