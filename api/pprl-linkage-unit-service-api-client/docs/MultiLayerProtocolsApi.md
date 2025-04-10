# pprl_linkage_unit_service_api_client.MultiLayerProtocolsApi

All URIs are relative to *http://localhost:8082*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_record_pairs**](MultiLayerProtocolsApi.md#add_record_pairs) | **POST** /protocol/pairs | Add record pairs
[**determine_uncertain_pairs**](MultiLayerProtocolsApi.md#determine_uncertain_pairs) | **GET** /protocol/pairs/uncertain/{projectId} | Determine uncertain record pairs
[**fetch_pairs**](MultiLayerProtocolsApi.md#fetch_pairs) | **POST** /protocol/pairs/fetch/{projectId} | Fetch and compare uncertain pairs from parent project for new records
[**get_wishes**](MultiLayerProtocolsApi.md#get_wishes) | **GET** /protocol/wishlist/{projectId} | Get record encoding wishes
[**reclassify**](MultiLayerProtocolsApi.md#reclassify) | **POST** /protocol/pairs/reclassify/{projectId} | Reclassify active links
[**report_pairs**](MultiLayerProtocolsApi.md#report_pairs) | **POST** /protocol/pairs/report/{projectId} | Report links
[**update2**](MultiLayerProtocolsApi.md#update2) | **POST** /protocol/matcher/update | Update a matcher based on improved links
[**update_record_pairs**](MultiLayerProtocolsApi.md#update_record_pairs) | **PUT** /protocol/pairs | Update record pairs


# **add_record_pairs**
> add_record_pairs(merge, record_pair_dto)

Add record pairs

### Example


```python
import pprl_linkage_unit_service_api_client
from pprl_linkage_unit_service_api_client.models.record_pair_dto import RecordPairDto
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
    api_instance = pprl_linkage_unit_service_api_client.MultiLayerProtocolsApi(api_client)
    merge = True # bool | 
    record_pair_dto = [pprl_linkage_unit_service_api_client.RecordPairDto()] # List[RecordPairDto] | 

    try:
        # Add record pairs
        api_instance.add_record_pairs(merge, record_pair_dto)
    except Exception as e:
        print("Exception when calling MultiLayerProtocolsApi->add_record_pairs: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **merge** | **bool**|  | 
 **record_pair_dto** | [**List[RecordPairDto]**](RecordPairDto.md)|  | 

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

# **determine_uncertain_pairs**
> List[RecordPairDto] determine_uncertain_pairs(project_id, limit=limit)

Determine uncertain record pairs

### Example


```python
import pprl_linkage_unit_service_api_client
from pprl_linkage_unit_service_api_client.models.record_pair_dto import RecordPairDto
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
    api_instance = pprl_linkage_unit_service_api_client.MultiLayerProtocolsApi(api_client)
    project_id = 'project_id_example' # str | 
    limit = -1 # int |  (optional) (default to -1)

    try:
        # Determine uncertain record pairs
        api_response = api_instance.determine_uncertain_pairs(project_id, limit=limit)
        print("The response of MultiLayerProtocolsApi->determine_uncertain_pairs:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MultiLayerProtocolsApi->determine_uncertain_pairs: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **limit** | **int**|  | [optional] [default to -1]

### Return type

[**List[RecordPairDto]**](RecordPairDto.md)

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

# **fetch_pairs**
> fetch_pairs(project_id)

Fetch and compare uncertain pairs from parent project for new records

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
    api_instance = pprl_linkage_unit_service_api_client.MultiLayerProtocolsApi(api_client)
    project_id = 'project_id_example' # str | 

    try:
        # Fetch and compare uncertain pairs from parent project for new records
        api_instance.fetch_pairs(project_id)
    except Exception as e:
        print("Exception when calling MultiLayerProtocolsApi->fetch_pairs: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 

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

# **get_wishes**
> List[RecordEncodingWishDto] get_wishes(project_id, create=create, limit=limit)

Get record encoding wishes

### Example


```python
import pprl_linkage_unit_service_api_client
from pprl_linkage_unit_service_api_client.models.record_encoding_wish_dto import RecordEncodingWishDto
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
    api_instance = pprl_linkage_unit_service_api_client.MultiLayerProtocolsApi(api_client)
    project_id = 'project_id_example' # str | 
    create = 'true' # str |  (optional) (default to 'true')
    limit = 56 # int |  (optional)

    try:
        # Get record encoding wishes
        api_response = api_instance.get_wishes(project_id, create=create, limit=limit)
        print("The response of MultiLayerProtocolsApi->get_wishes:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MultiLayerProtocolsApi->get_wishes: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **create** | **str**|  | [optional] [default to &#39;true&#39;]
 **limit** | **int**|  | [optional] 

### Return type

[**List[RecordEncodingWishDto]**](RecordEncodingWishDto.md)

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

# **reclassify**
> reclassify(project_id)

Reclassify active links

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
    api_instance = pprl_linkage_unit_service_api_client.MultiLayerProtocolsApi(api_client)
    project_id = 'project_id_example' # str | 

    try:
        # Reclassify active links
        api_instance.reclassify(project_id)
    except Exception as e:
        print("Exception when calling MultiLayerProtocolsApi->reclassify: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 

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

# **report_pairs**
> int report_pairs(project_id)

Report links

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
    api_instance = pprl_linkage_unit_service_api_client.MultiLayerProtocolsApi(api_client)
    project_id = 'project_id_example' # str | 

    try:
        # Report links
        api_response = api_instance.report_pairs(project_id)
        print("The response of MultiLayerProtocolsApi->report_pairs:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MultiLayerProtocolsApi->report_pairs: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 

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

# **update2**
> MatchingDto update2(matcher_update_request)

Update a matcher based on improved links

### Example


```python
import pprl_linkage_unit_service_api_client
from pprl_linkage_unit_service_api_client.models.matcher_update_request import MatcherUpdateRequest
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
    api_instance = pprl_linkage_unit_service_api_client.MultiLayerProtocolsApi(api_client)
    matcher_update_request = pprl_linkage_unit_service_api_client.MatcherUpdateRequest() # MatcherUpdateRequest | 

    try:
        # Update a matcher based on improved links
        api_response = api_instance.update2(matcher_update_request)
        print("The response of MultiLayerProtocolsApi->update2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MultiLayerProtocolsApi->update2: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **matcher_update_request** | [**MatcherUpdateRequest**](MatcherUpdateRequest.md)|  | 

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

# **update_record_pairs**
> update_record_pairs(record_pair_dto)

Update record pairs

### Example


```python
import pprl_linkage_unit_service_api_client
from pprl_linkage_unit_service_api_client.models.record_pair_dto import RecordPairDto
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
    api_instance = pprl_linkage_unit_service_api_client.MultiLayerProtocolsApi(api_client)
    record_pair_dto = [pprl_linkage_unit_service_api_client.RecordPairDto()] # List[RecordPairDto] | 

    try:
        # Update record pairs
        api_instance.update_record_pairs(record_pair_dto)
    except Exception as e:
        print("Exception when calling MultiLayerProtocolsApi->update_record_pairs: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **record_pair_dto** | [**List[RecordPairDto]**](RecordPairDto.md)|  | 

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

