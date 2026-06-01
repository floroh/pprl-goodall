# pprl_data_owner_service_api_client.CorrupterApi

All URIs are relative to *http://localhost:8181*

Method | HTTP request | Description
------------- | ------------- | -------------
[**corrupt_dataset**](CorrupterApi.md#corrupt_dataset) | **POST** /generate/corrupter | Corrupt dataset
[**get_dataset_generation_config**](CorrupterApi.md#get_dataset_generation_config) | **POST** /generate/corrupter/configs | Create dataset generation config
[**get_dataset_generation_methods**](CorrupterApi.md#get_dataset_generation_methods) | **GET** /generate/corrupter/configs/findAll | Get dataset generation config methods


# **corrupt_dataset**
> int corrupt_dataset(dataset_corruption_request_dto)

Corrupt dataset

### Example


```python
import pprl_data_owner_service_api_client
from pprl_data_owner_service_api_client.models.dataset_corruption_request_dto import DatasetCorruptionRequestDto
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
    api_instance = pprl_data_owner_service_api_client.CorrupterApi(api_client)
    dataset_corruption_request_dto = pprl_data_owner_service_api_client.DatasetCorruptionRequestDto() # DatasetCorruptionRequestDto | 

    try:
        # Corrupt dataset
        api_response = api_instance.corrupt_dataset(dataset_corruption_request_dto)
        print("The response of CorrupterApi->corrupt_dataset:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CorrupterApi->corrupt_dataset: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dataset_corruption_request_dto** | [**DatasetCorruptionRequestDto**](DatasetCorruptionRequestDto.md)|  | 

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

# **get_dataset_generation_config**
> DataSetGeneratorConfig get_dataset_generation_config(dataset_generation_config_creator_dto)

Create dataset generation config

### Example


```python
import pprl_data_owner_service_api_client
from pprl_data_owner_service_api_client.models.data_set_generator_config import DataSetGeneratorConfig
from pprl_data_owner_service_api_client.models.dataset_generation_config_creator_dto import DatasetGenerationConfigCreatorDto
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
    api_instance = pprl_data_owner_service_api_client.CorrupterApi(api_client)
    dataset_generation_config_creator_dto = pprl_data_owner_service_api_client.DatasetGenerationConfigCreatorDto() # DatasetGenerationConfigCreatorDto | 

    try:
        # Create dataset generation config
        api_response = api_instance.get_dataset_generation_config(dataset_generation_config_creator_dto)
        print("The response of CorrupterApi->get_dataset_generation_config:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CorrupterApi->get_dataset_generation_config: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dataset_generation_config_creator_dto** | [**DatasetGenerationConfigCreatorDto**](DatasetGenerationConfigCreatorDto.md)|  | 

### Return type

[**DataSetGeneratorConfig**](DataSetGeneratorConfig.md)

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

# **get_dataset_generation_methods**
> List[str] get_dataset_generation_methods()

Get dataset generation config methods

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
    api_instance = pprl_data_owner_service_api_client.CorrupterApi(api_client)

    try:
        # Get dataset generation config methods
        api_response = api_instance.get_dataset_generation_methods()
        print("The response of CorrupterApi->get_dataset_generation_methods:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CorrupterApi->get_dataset_generation_methods: %s\n" % e)
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

