# RecordCluster


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | [**ObjectId**](ObjectId.md) |  | [optional] 
**domain_id** | **str** |  | [optional] 
**origin** | [**GenericRawRecordWithDates**](GenericRawRecordWithDates.md) |  | [optional] 
**duplicates** | [**List[Duplicate]**](Duplicate.md) |  | [optional] 

## Example

```python
from pprl_data_generator_service_api_client.models.record_cluster import RecordCluster

# TODO update the JSON string below
json = "{}"
# create an instance of RecordCluster from a JSON string
record_cluster_instance = RecordCluster.from_json(json)
# print the JSON string representation of the object
print(RecordCluster.to_json())

# convert the object into a dict
record_cluster_dict = record_cluster_instance.to_dict()
# create an instance of RecordCluster from a dict
record_cluster_from_dict = RecordCluster.from_dict(record_cluster_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


