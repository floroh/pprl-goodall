# pprl_data_generator_service_api_client.DataSelectorApi

All URIs are relative to *http://localhost:8186*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_cluster_order**](DataSelectorApi.md#create_cluster_order) | **POST** /selector/prepare/cluster-order | 
[**delete_cluster_order**](DataSelectorApi.md#delete_cluster_order) | **DELETE** /selector/prepare/cluster-order | 
[**example_usvr_selection_config**](DataSelectorApi.md#example_usvr_selection_config) | **GET** /selector/configs/example/{name} | 
[**prepare_import_panse_ncvr**](DataSelectorApi.md#prepare_import_panse_ncvr) | **POST** /selector/prepare/import-ncvr | Import NCVR data
[**retrieve_clusters**](DataSelectorApi.md#retrieve_clusters) | **POST** /selector/clusters | 
[**select**](DataSelectorApi.md#select) | **POST** /selector/select | 


# **create_cluster_order**
> create_cluster_order(cluster_order_request)

### Example


```python
import pprl_data_generator_service_api_client
from pprl_data_generator_service_api_client.models.cluster_order_request import ClusterOrderRequest
from pprl_data_generator_service_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8186
# See configuration.py for a list of all supported configuration parameters.
configuration = pprl_data_generator_service_api_client.Configuration(
    host = "http://localhost:8186"
)


# Enter a context with an instance of the API client
with pprl_data_generator_service_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pprl_data_generator_service_api_client.DataSelectorApi(api_client)
    cluster_order_request = pprl_data_generator_service_api_client.ClusterOrderRequest() # ClusterOrderRequest | 

    try:
        api_instance.create_cluster_order(cluster_order_request)
    except Exception as e:
        print("Exception when calling DataSelectorApi->create_cluster_order: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cluster_order_request** | [**ClusterOrderRequest**](ClusterOrderRequest.md)|  | 

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

# **delete_cluster_order**
> delete_cluster_order(cluster_order_request)

### Example


```python
import pprl_data_generator_service_api_client
from pprl_data_generator_service_api_client.models.cluster_order_request import ClusterOrderRequest
from pprl_data_generator_service_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8186
# See configuration.py for a list of all supported configuration parameters.
configuration = pprl_data_generator_service_api_client.Configuration(
    host = "http://localhost:8186"
)


# Enter a context with an instance of the API client
with pprl_data_generator_service_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pprl_data_generator_service_api_client.DataSelectorApi(api_client)
    cluster_order_request = pprl_data_generator_service_api_client.ClusterOrderRequest() # ClusterOrderRequest | 

    try:
        api_instance.delete_cluster_order(cluster_order_request)
    except Exception as e:
        print("Exception when calling DataSelectorApi->delete_cluster_order: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cluster_order_request** | [**ClusterOrderRequest**](ClusterOrderRequest.md)|  | 

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

# **example_usvr_selection_config**
> UsvrSelectionConfig example_usvr_selection_config(name)

### Example


```python
import pprl_data_generator_service_api_client
from pprl_data_generator_service_api_client.models.usvr_selection_config import UsvrSelectionConfig
from pprl_data_generator_service_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8186
# See configuration.py for a list of all supported configuration parameters.
configuration = pprl_data_generator_service_api_client.Configuration(
    host = "http://localhost:8186"
)


# Enter a context with an instance of the API client
with pprl_data_generator_service_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pprl_data_generator_service_api_client.DataSelectorApi(api_client)
    name = 'name_example' # str | 

    try:
        api_response = api_instance.example_usvr_selection_config(name)
        print("The response of DataSelectorApi->example_usvr_selection_config:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataSelectorApi->example_usvr_selection_config: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**|  | 

### Return type

[**UsvrSelectionConfig**](UsvrSelectionConfig.md)

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

# **prepare_import_panse_ncvr**
> prepare_import_panse_ncvr(ncvr_panse_import_request)

Import NCVR data

Import record clusters from North Carolina Voter Registry as provied by Panse et al. at EDBT

### Example


```python
import pprl_data_generator_service_api_client
from pprl_data_generator_service_api_client.models.ncvr_panse_import_request import NcvrPanseImportRequest
from pprl_data_generator_service_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8186
# See configuration.py for a list of all supported configuration parameters.
configuration = pprl_data_generator_service_api_client.Configuration(
    host = "http://localhost:8186"
)


# Enter a context with an instance of the API client
with pprl_data_generator_service_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pprl_data_generator_service_api_client.DataSelectorApi(api_client)
    ncvr_panse_import_request = pprl_data_generator_service_api_client.NcvrPanseImportRequest() # NcvrPanseImportRequest | 

    try:
        # Import NCVR data
        api_instance.prepare_import_panse_ncvr(ncvr_panse_import_request)
    except Exception as e:
        print("Exception when calling DataSelectorApi->prepare_import_panse_ncvr: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ncvr_panse_import_request** | [**NcvrPanseImportRequest**](NcvrPanseImportRequest.md)|  | 

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

# **retrieve_clusters**
> List[RecordCluster] retrieve_clusters(usvr_selection_config)

### Example


```python
import pprl_data_generator_service_api_client
from pprl_data_generator_service_api_client.models.record_cluster import RecordCluster
from pprl_data_generator_service_api_client.models.usvr_selection_config import UsvrSelectionConfig
from pprl_data_generator_service_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8186
# See configuration.py for a list of all supported configuration parameters.
configuration = pprl_data_generator_service_api_client.Configuration(
    host = "http://localhost:8186"
)


# Enter a context with an instance of the API client
with pprl_data_generator_service_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pprl_data_generator_service_api_client.DataSelectorApi(api_client)
    usvr_selection_config = pprl_data_generator_service_api_client.UsvrSelectionConfig() # UsvrSelectionConfig | 

    try:
        api_response = api_instance.retrieve_clusters(usvr_selection_config)
        print("The response of DataSelectorApi->retrieve_clusters:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataSelectorApi->retrieve_clusters: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **usvr_selection_config** | [**UsvrSelectionConfig**](UsvrSelectionConfig.md)|  | 

### Return type

[**List[RecordCluster]**](RecordCluster.md)

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

# **select**
> TaggedDatasetDto select(usvr_selection_config)

### Example


```python
import pprl_data_generator_service_api_client
from pprl_data_generator_service_api_client.models.tagged_dataset_dto import TaggedDatasetDto
from pprl_data_generator_service_api_client.models.usvr_selection_config import UsvrSelectionConfig
from pprl_data_generator_service_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8186
# See configuration.py for a list of all supported configuration parameters.
configuration = pprl_data_generator_service_api_client.Configuration(
    host = "http://localhost:8186"
)


# Enter a context with an instance of the API client
with pprl_data_generator_service_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pprl_data_generator_service_api_client.DataSelectorApi(api_client)
    usvr_selection_config = pprl_data_generator_service_api_client.UsvrSelectionConfig() # UsvrSelectionConfig | 

    try:
        api_response = api_instance.select(usvr_selection_config)
        print("The response of DataSelectorApi->select:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataSelectorApi->select: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **usvr_selection_config** | [**UsvrSelectionConfig**](UsvrSelectionConfig.md)|  | 

### Return type

[**TaggedDatasetDto**](TaggedDatasetDto.md)

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

