# pprl_data_generator_service_api_client.DataGeneratorApi

All URIs are relative to *http://localhost:8186*

Method | HTTP request | Description
------------- | ------------- | -------------
[**example_germany_generator_configuration**](DataGeneratorApi.md#example_germany_generator_configuration) | **GET** /generator/configs/example/{name} | Get example configuration
[**generate**](DataGeneratorApi.md#generate) | **POST** /generator/generate | Generate synthetic records


# **example_germany_generator_configuration**
> GermanyGeneratorConfig example_germany_generator_configuration(name)

Get example configuration

Retrieves an example GermanyGeneratorConfiguration with specified parameters

### Example


```python
import pprl_data_generator_service_api_client
from pprl_data_generator_service_api_client.models.germany_generator_config import GermanyGeneratorConfig
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
    api_instance = pprl_data_generator_service_api_client.DataGeneratorApi(api_client)
    name = 'name_example' # str | Name of the example configuration (embed 'HH' to include households structures)

    try:
        # Get example configuration
        api_response = api_instance.example_germany_generator_configuration(name)
        print("The response of DataGeneratorApi->example_germany_generator_configuration:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataGeneratorApi->example_germany_generator_configuration: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| Name of the example configuration (embed &#39;HH&#39; to include households structures) | 

### Return type

[**GermanyGeneratorConfig**](GermanyGeneratorConfig.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully retrieved example configuration |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **generate**
> TaggedDatasetDto generate(germany_generator_config)

Generate synthetic records

Generates a list of synthetic records based on the provided configuration

### Example


```python
import pprl_data_generator_service_api_client
from pprl_data_generator_service_api_client.models.germany_generator_config import GermanyGeneratorConfig
from pprl_data_generator_service_api_client.models.tagged_dataset_dto import TaggedDatasetDto
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
    api_instance = pprl_data_generator_service_api_client.DataGeneratorApi(api_client)
    germany_generator_config = pprl_data_generator_service_api_client.GermanyGeneratorConfig() # GermanyGeneratorConfig | 

    try:
        # Generate synthetic records
        api_response = api_instance.generate(germany_generator_config)
        print("The response of DataGeneratorApi->generate:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataGeneratorApi->generate: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **germany_generator_config** | [**GermanyGeneratorConfig**](GermanyGeneratorConfig.md)|  | 

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

