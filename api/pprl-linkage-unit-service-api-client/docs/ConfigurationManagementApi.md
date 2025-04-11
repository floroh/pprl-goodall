# pprl_linkage_unit_service_api_client.ConfigurationManagementApi

All URIs are relative to *http://localhost:8082*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add**](ConfigurationManagementApi.md#add) | **POST** /config/ | Add a configuration
[**get_classifier_description**](ConfigurationManagementApi.md#get_classifier_description) | **POST** /config/classifier | Get classifier description
[**get_configs**](ConfigurationManagementApi.md#get_configs) | **GET** /config/findAll | Get a list of all configuration IDs
[**get_matching**](ConfigurationManagementApi.md#get_matching) | **POST** /config/findById | Get the configuration by its ID
[**get_method_requirements**](ConfigurationManagementApi.md#get_method_requirements) | **GET** /config/findAllRequirements | Get descriptions of the requirements of all matching methods
[**remove**](ConfigurationManagementApi.md#remove) | **DELETE** /config/unused | Remove unused configurations
[**remove1**](ConfigurationManagementApi.md#remove1) | **DELETE** /config/ | Remove a configuration
[**update1**](ConfigurationManagementApi.md#update1) | **PUT** /config/ | Override an existing configuration


# **add**
> add(matching_dto)

Add a configuration

### Example


```python
import pprl_linkage_unit_service_api_client
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
    api_instance = pprl_linkage_unit_service_api_client.ConfigurationManagementApi(api_client)
    matching_dto = pprl_linkage_unit_service_api_client.MatchingDto() # MatchingDto | 

    try:
        # Add a configuration
        api_instance.add(matching_dto)
    except Exception as e:
        print("Exception when calling ConfigurationManagementApi->add: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **matching_dto** | [**MatchingDto**](MatchingDto.md)|  | 

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

# **get_classifier_description**
> MatchingDto get_classifier_description(matcher_id_dto)

Get classifier description

### Example


```python
import pprl_linkage_unit_service_api_client
from pprl_linkage_unit_service_api_client.models.matcher_id_dto import MatcherIdDto
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
    api_instance = pprl_linkage_unit_service_api_client.ConfigurationManagementApi(api_client)
    matcher_id_dto = pprl_linkage_unit_service_api_client.MatcherIdDto() # MatcherIdDto | 

    try:
        # Get classifier description
        api_response = api_instance.get_classifier_description(matcher_id_dto)
        print("The response of ConfigurationManagementApi->get_classifier_description:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ConfigurationManagementApi->get_classifier_description: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **matcher_id_dto** | [**MatcherIdDto**](MatcherIdDto.md)|  | 

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

# **get_configs**
> List[MatcherIdDto] get_configs()

Get a list of all configuration IDs

### Example


```python
import pprl_linkage_unit_service_api_client
from pprl_linkage_unit_service_api_client.models.matcher_id_dto import MatcherIdDto
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
    api_instance = pprl_linkage_unit_service_api_client.ConfigurationManagementApi(api_client)

    try:
        # Get a list of all configuration IDs
        api_response = api_instance.get_configs()
        print("The response of ConfigurationManagementApi->get_configs:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ConfigurationManagementApi->get_configs: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[MatcherIdDto]**](MatcherIdDto.md)

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

# **get_matching**
> MatchingDto get_matching(matcher_id_dto)

Get the configuration by its ID

### Example


```python
import pprl_linkage_unit_service_api_client
from pprl_linkage_unit_service_api_client.models.matcher_id_dto import MatcherIdDto
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
    api_instance = pprl_linkage_unit_service_api_client.ConfigurationManagementApi(api_client)
    matcher_id_dto = pprl_linkage_unit_service_api_client.MatcherIdDto() # MatcherIdDto | 

    try:
        # Get the configuration by its ID
        api_response = api_instance.get_matching(matcher_id_dto)
        print("The response of ConfigurationManagementApi->get_matching:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ConfigurationManagementApi->get_matching: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **matcher_id_dto** | [**MatcherIdDto**](MatcherIdDto.md)|  | 

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

# **get_method_requirements**
> List[RecordRequirementsDto] get_method_requirements()

Get descriptions of the requirements of all matching methods

### Example


```python
import pprl_linkage_unit_service_api_client
from pprl_linkage_unit_service_api_client.models.record_requirements_dto import RecordRequirementsDto
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
    api_instance = pprl_linkage_unit_service_api_client.ConfigurationManagementApi(api_client)

    try:
        # Get descriptions of the requirements of all matching methods
        api_response = api_instance.get_method_requirements()
        print("The response of ConfigurationManagementApi->get_method_requirements:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ConfigurationManagementApi->get_method_requirements: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[RecordRequirementsDto]**](RecordRequirementsDto.md)

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

# **remove**
> int remove(dry_run)

Remove unused configurations

### Example


```python
import pprl_linkage_unit_service_api_client
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
    api_instance = pprl_linkage_unit_service_api_client.ConfigurationManagementApi(api_client)
    dry_run = True # bool | 

    try:
        # Remove unused configurations
        api_response = api_instance.remove(dry_run)
        print("The response of ConfigurationManagementApi->remove:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ConfigurationManagementApi->remove: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dry_run** | **bool**|  | 

### Return type

**int**

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

# **remove1**
> remove1(matcher_id_dto)

Remove a configuration

### Example


```python
import pprl_linkage_unit_service_api_client
from pprl_linkage_unit_service_api_client.models.matcher_id_dto import MatcherIdDto
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
    api_instance = pprl_linkage_unit_service_api_client.ConfigurationManagementApi(api_client)
    matcher_id_dto = pprl_linkage_unit_service_api_client.MatcherIdDto() # MatcherIdDto | 

    try:
        # Remove a configuration
        api_instance.remove1(matcher_id_dto)
    except Exception as e:
        print("Exception when calling ConfigurationManagementApi->remove1: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **matcher_id_dto** | [**MatcherIdDto**](MatcherIdDto.md)|  | 

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

# **update1**
> update1(matching_dto)

Override an existing configuration

### Example


```python
import pprl_linkage_unit_service_api_client
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
    api_instance = pprl_linkage_unit_service_api_client.ConfigurationManagementApi(api_client)
    matching_dto = pprl_linkage_unit_service_api_client.MatchingDto() # MatchingDto | 

    try:
        # Override an existing configuration
        api_instance.update1(matching_dto)
    except Exception as e:
        print("Exception when calling ConfigurationManagementApi->update1: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **matching_dto** | [**MatchingDto**](MatchingDto.md)|  | 

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

