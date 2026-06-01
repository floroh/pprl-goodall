# pprl_data_owner_service_api_client.DatasetManagementApi

All URIs are relative to *http://localhost:8181*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_dataset_description**](DatasetManagementApi.md#add_dataset_description) | **POST** /record/datasets | Add a dataset description
[**compare_datasets**](DatasetManagementApi.md#compare_datasets) | **GET** /record/compare/{datasetId0}/{datasetId1} | Compare dataset
[**count**](DatasetManagementApi.md#count) | **GET** /record/{datasetId}/count | Get the number of records in the database
[**delete_all**](DatasetManagementApi.md#delete_all) | **DELETE** /record/{datasetId}/all | Clear the record database
[**delete_dataset**](DatasetManagementApi.md#delete_dataset) | **DELETE** /record/datasets/{datasetId} | Delete dataset
[**find_by_dataset_and_source**](DatasetManagementApi.md#find_by_dataset_and_source) | **POST** /record/findBySource/{datasetId} | Retrieve a persisted record by source
[**find_by_record_id**](DatasetManagementApi.md#find_by_record_id) | **POST** /record/findByRecordId/{datasetId} | Retrieve a persisted record by its record id (source + local)
[**find_by_unique_id**](DatasetManagementApi.md#find_by_unique_id) | **GET** /record/{uniqueId} | Retrieve a persisted record
[**find_by_unique_ids**](DatasetManagementApi.md#find_by_unique_ids) | **POST** /record/findByIds | Retrieve multiple persisted records
[**get_all**](DatasetManagementApi.md#get_all) | **GET** /record/{datasetId}/all | Get all records from the database
[**get_dataset_description**](DatasetManagementApi.md#get_dataset_description) | **GET** /record/datasets/{datasetId} | Get dataset description
[**get_dataset_descriptions**](DatasetManagementApi.md#get_dataset_descriptions) | **GET** /record/datasets | Get available dataset descriptions, optionally filtered by plaintextDatasetId
[**get_dataset_ids**](DatasetManagementApi.md#get_dataset_ids) | **GET** /record/datasets/ids | Get available dataset ids
[**insert**](DatasetManagementApi.md#insert) | **POST** /record | Add a record to the database
[**insert_batch**](DatasetManagementApi.md#insert_batch) | **POST** /record/batch | Add multiple records to the database
[**update1**](DatasetManagementApi.md#update1) | **PUT** /record | Update an existing record in the database


# **add_dataset_description**
> DatasetDto add_dataset_description(dataset_dto)

Add a dataset description

### Example


```python
import pprl_data_owner_service_api_client
from pprl_data_owner_service_api_client.models.dataset_dto import DatasetDto
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
    api_instance = pprl_data_owner_service_api_client.DatasetManagementApi(api_client)
    dataset_dto = pprl_data_owner_service_api_client.DatasetDto() # DatasetDto | 

    try:
        # Add a dataset description
        api_response = api_instance.add_dataset_description(dataset_dto)
        print("The response of DatasetManagementApi->add_dataset_description:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatasetManagementApi->add_dataset_description: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dataset_dto** | [**DatasetDto**](DatasetDto.md)|  | 

### Return type

[**DatasetDto**](DatasetDto.md)

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

# **compare_datasets**
> int compare_datasets(dataset_id0, dataset_id1)

Compare dataset

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
    api_instance = pprl_data_owner_service_api_client.DatasetManagementApi(api_client)
    dataset_id0 = 56 # int | 
    dataset_id1 = 56 # int | 

    try:
        # Compare dataset
        api_response = api_instance.compare_datasets(dataset_id0, dataset_id1)
        print("The response of DatasetManagementApi->compare_datasets:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatasetManagementApi->compare_datasets: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dataset_id0** | **int**|  | 
 **dataset_id1** | **int**|  | 

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

# **count**
> int count(dataset_id)

Get the number of records in the database

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
    api_instance = pprl_data_owner_service_api_client.DatasetManagementApi(api_client)
    dataset_id = 56 # int | 

    try:
        # Get the number of records in the database
        api_response = api_instance.count(dataset_id)
        print("The response of DatasetManagementApi->count:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatasetManagementApi->count: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dataset_id** | **int**|  | 

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

# **delete_all**
> delete_all(dataset_id)

Clear the record database

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
    api_instance = pprl_data_owner_service_api_client.DatasetManagementApi(api_client)
    dataset_id = 56 # int | 

    try:
        # Clear the record database
        api_instance.delete_all(dataset_id)
    except Exception as e:
        print("Exception when calling DatasetManagementApi->delete_all: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dataset_id** | **int**|  | 

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

# **delete_dataset**
> delete_dataset(dataset_id)

Delete dataset

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
    api_instance = pprl_data_owner_service_api_client.DatasetManagementApi(api_client)
    dataset_id = 56 # int | 

    try:
        # Delete dataset
        api_instance.delete_dataset(dataset_id)
    except Exception as e:
        print("Exception when calling DatasetManagementApi->delete_dataset: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dataset_id** | **int**|  | 

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

# **find_by_dataset_and_source**
> List[RecordDto] find_by_dataset_and_source(dataset_id, body)

Retrieve a persisted record by source

### Example


```python
import pprl_data_owner_service_api_client
from pprl_data_owner_service_api_client.models.record_dto import RecordDto
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
    api_instance = pprl_data_owner_service_api_client.DatasetManagementApi(api_client)
    dataset_id = 56 # int | 
    body = 'body_example' # str | 

    try:
        # Retrieve a persisted record by source
        api_response = api_instance.find_by_dataset_and_source(dataset_id, body)
        print("The response of DatasetManagementApi->find_by_dataset_and_source:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatasetManagementApi->find_by_dataset_and_source: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dataset_id** | **int**|  | 
 **body** | **str**|  | 

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

# **find_by_record_id**
> RecordDto find_by_record_id(dataset_id, record_id_dto)

Retrieve a persisted record by its record id (source + local)

### Example


```python
import pprl_data_owner_service_api_client
from pprl_data_owner_service_api_client.models.record_dto import RecordDto
from pprl_data_owner_service_api_client.models.record_id_dto import RecordIdDto
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
    api_instance = pprl_data_owner_service_api_client.DatasetManagementApi(api_client)
    dataset_id = 56 # int | 
    record_id_dto = pprl_data_owner_service_api_client.RecordIdDto() # RecordIdDto | 

    try:
        # Retrieve a persisted record by its record id (source + local)
        api_response = api_instance.find_by_record_id(dataset_id, record_id_dto)
        print("The response of DatasetManagementApi->find_by_record_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatasetManagementApi->find_by_record_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dataset_id** | **int**|  | 
 **record_id_dto** | [**RecordIdDto**](RecordIdDto.md)|  | 

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

# **find_by_unique_id**
> RecordDto find_by_unique_id(unique_id)

Retrieve a persisted record

### Example


```python
import pprl_data_owner_service_api_client
from pprl_data_owner_service_api_client.models.record_dto import RecordDto
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
    api_instance = pprl_data_owner_service_api_client.DatasetManagementApi(api_client)
    unique_id = 'unique_id_example' # str | 

    try:
        # Retrieve a persisted record
        api_response = api_instance.find_by_unique_id(unique_id)
        print("The response of DatasetManagementApi->find_by_unique_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatasetManagementApi->find_by_unique_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **unique_id** | **str**|  | 

### Return type

[**RecordDto**](RecordDto.md)

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

# **find_by_unique_ids**
> List[RecordDto] find_by_unique_ids(request_body)

Retrieve multiple persisted records

### Example


```python
import pprl_data_owner_service_api_client
from pprl_data_owner_service_api_client.models.record_dto import RecordDto
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
    api_instance = pprl_data_owner_service_api_client.DatasetManagementApi(api_client)
    request_body = ['request_body_example'] # List[str] | 

    try:
        # Retrieve multiple persisted records
        api_response = api_instance.find_by_unique_ids(request_body)
        print("The response of DatasetManagementApi->find_by_unique_ids:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatasetManagementApi->find_by_unique_ids: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **request_body** | [**List[str]**](str.md)|  | 

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

# **get_all**
> List[RecordDto] get_all(dataset_id, limit=limit)

Get all records from the database

### Example


```python
import pprl_data_owner_service_api_client
from pprl_data_owner_service_api_client.models.record_dto import RecordDto
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
    api_instance = pprl_data_owner_service_api_client.DatasetManagementApi(api_client)
    dataset_id = 56 # int | 
    limit = -1 # int |  (optional) (default to -1)

    try:
        # Get all records from the database
        api_response = api_instance.get_all(dataset_id, limit=limit)
        print("The response of DatasetManagementApi->get_all:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatasetManagementApi->get_all: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dataset_id** | **int**|  | 
 **limit** | **int**|  | [optional] [default to -1]

### Return type

[**List[RecordDto]**](RecordDto.md)

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

# **get_dataset_description**
> DatasetDto get_dataset_description(dataset_id)

Get dataset description

### Example


```python
import pprl_data_owner_service_api_client
from pprl_data_owner_service_api_client.models.dataset_dto import DatasetDto
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
    api_instance = pprl_data_owner_service_api_client.DatasetManagementApi(api_client)
    dataset_id = 56 # int | 

    try:
        # Get dataset description
        api_response = api_instance.get_dataset_description(dataset_id)
        print("The response of DatasetManagementApi->get_dataset_description:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatasetManagementApi->get_dataset_description: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dataset_id** | **int**|  | 

### Return type

[**DatasetDto**](DatasetDto.md)

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

# **get_dataset_descriptions**
> List[DatasetDto] get_dataset_descriptions(plaintext_dataset_id=plaintext_dataset_id)

Get available dataset descriptions, optionally filtered by plaintextDatasetId

### Example


```python
import pprl_data_owner_service_api_client
from pprl_data_owner_service_api_client.models.dataset_dto import DatasetDto
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
    api_instance = pprl_data_owner_service_api_client.DatasetManagementApi(api_client)
    plaintext_dataset_id = 56 # int |  (optional)

    try:
        # Get available dataset descriptions, optionally filtered by plaintextDatasetId
        api_response = api_instance.get_dataset_descriptions(plaintext_dataset_id=plaintext_dataset_id)
        print("The response of DatasetManagementApi->get_dataset_descriptions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatasetManagementApi->get_dataset_descriptions: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **plaintext_dataset_id** | **int**|  | [optional] 

### Return type

[**List[DatasetDto]**](DatasetDto.md)

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

# **get_dataset_ids**
> List[int] get_dataset_ids()

Get available dataset ids

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
    api_instance = pprl_data_owner_service_api_client.DatasetManagementApi(api_client)

    try:
        # Get available dataset ids
        api_response = api_instance.get_dataset_ids()
        print("The response of DatasetManagementApi->get_dataset_ids:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatasetManagementApi->get_dataset_ids: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

**List[int]**

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

# **insert**
> RecordIdDto insert(record_dto)

Add a record to the database

### Example


```python
import pprl_data_owner_service_api_client
from pprl_data_owner_service_api_client.models.record_dto import RecordDto
from pprl_data_owner_service_api_client.models.record_id_dto import RecordIdDto
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
    api_instance = pprl_data_owner_service_api_client.DatasetManagementApi(api_client)
    record_dto = pprl_data_owner_service_api_client.RecordDto() # RecordDto | 

    try:
        # Add a record to the database
        api_response = api_instance.insert(record_dto)
        print("The response of DatasetManagementApi->insert:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatasetManagementApi->insert: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **record_dto** | [**RecordDto**](RecordDto.md)|  | 

### Return type

[**RecordIdDto**](RecordIdDto.md)

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

# **insert_batch**
> List[RecordIdDto] insert_batch(record_dto)

Add multiple records to the database

### Example


```python
import pprl_data_owner_service_api_client
from pprl_data_owner_service_api_client.models.record_dto import RecordDto
from pprl_data_owner_service_api_client.models.record_id_dto import RecordIdDto
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
    api_instance = pprl_data_owner_service_api_client.DatasetManagementApi(api_client)
    record_dto = [pprl_data_owner_service_api_client.RecordDto()] # List[RecordDto] | 

    try:
        # Add multiple records to the database
        api_response = api_instance.insert_batch(record_dto)
        print("The response of DatasetManagementApi->insert_batch:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatasetManagementApi->insert_batch: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **record_dto** | [**List[RecordDto]**](RecordDto.md)|  | 

### Return type

[**List[RecordIdDto]**](RecordIdDto.md)

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

# **update1**
> RecordIdDto update1(record_dto)

Update an existing record in the database

### Example


```python
import pprl_data_owner_service_api_client
from pprl_data_owner_service_api_client.models.record_dto import RecordDto
from pprl_data_owner_service_api_client.models.record_id_dto import RecordIdDto
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
    api_instance = pprl_data_owner_service_api_client.DatasetManagementApi(api_client)
    record_dto = pprl_data_owner_service_api_client.RecordDto() # RecordDto | 

    try:
        # Update an existing record in the database
        api_response = api_instance.update1(record_dto)
        print("The response of DatasetManagementApi->update1:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatasetManagementApi->update1: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **record_dto** | [**RecordDto**](RecordDto.md)|  | 

### Return type

[**RecordIdDto**](RecordIdDto.md)

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

