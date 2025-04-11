# pprl_linkage_unit_service_api_client.DatasetManagementApi

All URIs are relative to *http://localhost:8082*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_dataset_description**](DatasetManagementApi.md#add_dataset_description) | **POST** /record/datasets | Add a dataset description
[**compare_datasets**](DatasetManagementApi.md#compare_datasets) | **GET** /record/compare/{idDataset0}/{idDataset1} | Compare dataset
[**count**](DatasetManagementApi.md#count) | **GET** /record/{idDataset}/count | Get the number of records in the database
[**delete_all**](DatasetManagementApi.md#delete_all) | **DELETE** /record/{idDataset}/all | Clear the record database
[**delete_dataset**](DatasetManagementApi.md#delete_dataset) | **DELETE** /record/datasets/{idDataset} | Delete dataset
[**find_by_dataset_and_source**](DatasetManagementApi.md#find_by_dataset_and_source) | **POST** /record/findBySource/{idDataset} | Retrieve a persisted record by source
[**find_by_record_id**](DatasetManagementApi.md#find_by_record_id) | **POST** /record/findByRecordId/{idDataset} | Retrieve a persisted record by its record id (source + local)
[**find_by_unique_id**](DatasetManagementApi.md#find_by_unique_id) | **GET** /record/{uniqueId} | Retrieve a persisted record
[**find_by_unique_ids**](DatasetManagementApi.md#find_by_unique_ids) | **POST** /record/findByIds | Retrieve multiple persisted records
[**get_all**](DatasetManagementApi.md#get_all) | **GET** /record/{idDataset}/all | Get all records from the database
[**get_dataset_description**](DatasetManagementApi.md#get_dataset_description) | **GET** /record/datasets/{idDataset} | Get dataset description
[**get_dataset_descriptions**](DatasetManagementApi.md#get_dataset_descriptions) | **GET** /record/datasets | Get available dataset descriptions, optionally filtered by plaintextDatasetId
[**get_dataset_ids**](DatasetManagementApi.md#get_dataset_ids) | **GET** /record/datasets/ids | Get available dataset ids
[**insert**](DatasetManagementApi.md#insert) | **POST** /record | Add a record to the database
[**insert_batch**](DatasetManagementApi.md#insert_batch) | **POST** /record/batch | Add multiple records to the database
[**update**](DatasetManagementApi.md#update) | **PUT** /record | Update an existing record in the database


# **add_dataset_description**
> DatasetDto add_dataset_description(dataset_dto)

Add a dataset description

### Example


```python
import pprl_linkage_unit_service_api_client
from pprl_linkage_unit_service_api_client.models.dataset_dto import DatasetDto
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
    api_instance = pprl_linkage_unit_service_api_client.DatasetManagementApi(api_client)
    dataset_dto = pprl_linkage_unit_service_api_client.DatasetDto() # DatasetDto | 

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
> int compare_datasets(id_dataset0, id_dataset1)

Compare dataset

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
    api_instance = pprl_linkage_unit_service_api_client.DatasetManagementApi(api_client)
    id_dataset0 = 56 # int | 
    id_dataset1 = 56 # int | 

    try:
        # Compare dataset
        api_response = api_instance.compare_datasets(id_dataset0, id_dataset1)
        print("The response of DatasetManagementApi->compare_datasets:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatasetManagementApi->compare_datasets: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id_dataset0** | **int**|  | 
 **id_dataset1** | **int**|  | 

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
> int count(id_dataset)

Get the number of records in the database

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
    api_instance = pprl_linkage_unit_service_api_client.DatasetManagementApi(api_client)
    id_dataset = 56 # int | 

    try:
        # Get the number of records in the database
        api_response = api_instance.count(id_dataset)
        print("The response of DatasetManagementApi->count:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatasetManagementApi->count: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id_dataset** | **int**|  | 

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
> delete_all(id_dataset)

Clear the record database

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
    api_instance = pprl_linkage_unit_service_api_client.DatasetManagementApi(api_client)
    id_dataset = 56 # int | 

    try:
        # Clear the record database
        api_instance.delete_all(id_dataset)
    except Exception as e:
        print("Exception when calling DatasetManagementApi->delete_all: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id_dataset** | **int**|  | 

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
> delete_dataset(id_dataset)

Delete dataset

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
    api_instance = pprl_linkage_unit_service_api_client.DatasetManagementApi(api_client)
    id_dataset = 56 # int | 

    try:
        # Delete dataset
        api_instance.delete_dataset(id_dataset)
    except Exception as e:
        print("Exception when calling DatasetManagementApi->delete_dataset: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id_dataset** | **int**|  | 

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
> List[RecordDto] find_by_dataset_and_source(id_dataset, body)

Retrieve a persisted record by source

### Example


```python
import pprl_linkage_unit_service_api_client
from pprl_linkage_unit_service_api_client.models.record_dto import RecordDto
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
    api_instance = pprl_linkage_unit_service_api_client.DatasetManagementApi(api_client)
    id_dataset = 'id_dataset_example' # str | 
    body = 'body_example' # str | 

    try:
        # Retrieve a persisted record by source
        api_response = api_instance.find_by_dataset_and_source(id_dataset, body)
        print("The response of DatasetManagementApi->find_by_dataset_and_source:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatasetManagementApi->find_by_dataset_and_source: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id_dataset** | **str**|  | 
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
> RecordDto find_by_record_id(id_dataset, record_id_dto)

Retrieve a persisted record by its record id (source + local)

### Example


```python
import pprl_linkage_unit_service_api_client
from pprl_linkage_unit_service_api_client.models.record_dto import RecordDto
from pprl_linkage_unit_service_api_client.models.record_id_dto import RecordIdDto
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
    api_instance = pprl_linkage_unit_service_api_client.DatasetManagementApi(api_client)
    id_dataset = 'id_dataset_example' # str | 
    record_id_dto = pprl_linkage_unit_service_api_client.RecordIdDto() # RecordIdDto | 

    try:
        # Retrieve a persisted record by its record id (source + local)
        api_response = api_instance.find_by_record_id(id_dataset, record_id_dto)
        print("The response of DatasetManagementApi->find_by_record_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatasetManagementApi->find_by_record_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id_dataset** | **str**|  | 
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
import pprl_linkage_unit_service_api_client
from pprl_linkage_unit_service_api_client.models.record_dto import RecordDto
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
    api_instance = pprl_linkage_unit_service_api_client.DatasetManagementApi(api_client)
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
import pprl_linkage_unit_service_api_client
from pprl_linkage_unit_service_api_client.models.record_dto import RecordDto
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
    api_instance = pprl_linkage_unit_service_api_client.DatasetManagementApi(api_client)
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
> List[RecordDto] get_all(id_dataset, limit=limit)

Get all records from the database

### Example


```python
import pprl_linkage_unit_service_api_client
from pprl_linkage_unit_service_api_client.models.record_dto import RecordDto
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
    api_instance = pprl_linkage_unit_service_api_client.DatasetManagementApi(api_client)
    id_dataset = 56 # int | 
    limit = -1 # int |  (optional) (default to -1)

    try:
        # Get all records from the database
        api_response = api_instance.get_all(id_dataset, limit=limit)
        print("The response of DatasetManagementApi->get_all:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatasetManagementApi->get_all: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id_dataset** | **int**|  | 
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
> DatasetDto get_dataset_description(id_dataset)

Get dataset description

### Example


```python
import pprl_linkage_unit_service_api_client
from pprl_linkage_unit_service_api_client.models.dataset_dto import DatasetDto
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
    api_instance = pprl_linkage_unit_service_api_client.DatasetManagementApi(api_client)
    id_dataset = 56 # int | 

    try:
        # Get dataset description
        api_response = api_instance.get_dataset_description(id_dataset)
        print("The response of DatasetManagementApi->get_dataset_description:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatasetManagementApi->get_dataset_description: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id_dataset** | **int**|  | 

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
import pprl_linkage_unit_service_api_client
from pprl_linkage_unit_service_api_client.models.dataset_dto import DatasetDto
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
    api_instance = pprl_linkage_unit_service_api_client.DatasetManagementApi(api_client)
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
    api_instance = pprl_linkage_unit_service_api_client.DatasetManagementApi(api_client)

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
import pprl_linkage_unit_service_api_client
from pprl_linkage_unit_service_api_client.models.record_dto import RecordDto
from pprl_linkage_unit_service_api_client.models.record_id_dto import RecordIdDto
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
    api_instance = pprl_linkage_unit_service_api_client.DatasetManagementApi(api_client)
    record_dto = pprl_linkage_unit_service_api_client.RecordDto() # RecordDto | 

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
import pprl_linkage_unit_service_api_client
from pprl_linkage_unit_service_api_client.models.record_dto import RecordDto
from pprl_linkage_unit_service_api_client.models.record_id_dto import RecordIdDto
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
    api_instance = pprl_linkage_unit_service_api_client.DatasetManagementApi(api_client)
    record_dto = [pprl_linkage_unit_service_api_client.RecordDto()] # List[RecordDto] | 

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

# **update**
> RecordIdDto update(record_dto)

Update an existing record in the database

### Example


```python
import pprl_linkage_unit_service_api_client
from pprl_linkage_unit_service_api_client.models.record_dto import RecordDto
from pprl_linkage_unit_service_api_client.models.record_id_dto import RecordIdDto
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
    api_instance = pprl_linkage_unit_service_api_client.DatasetManagementApi(api_client)
    record_dto = pprl_linkage_unit_service_api_client.RecordDto() # RecordDto | 

    try:
        # Update an existing record in the database
        api_response = api_instance.update(record_dto)
        print("The response of DatasetManagementApi->update:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatasetManagementApi->update: %s\n" % e)
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

