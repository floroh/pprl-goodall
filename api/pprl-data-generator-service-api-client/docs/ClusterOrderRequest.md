# ClusterOrderRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | [optional] 
**seed** | **str** |  | [optional] 

## Example

```python
from pprl_data_generator_service_api_client.models.cluster_order_request import ClusterOrderRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ClusterOrderRequest from a JSON string
cluster_order_request_instance = ClusterOrderRequest.from_json(json)
# print the JSON string representation of the object
print(ClusterOrderRequest.to_json())

# convert the object into a dict
cluster_order_request_dict = cluster_order_request_instance.to_dict()
# create an instance of ClusterOrderRequest from a dict
cluster_order_request_from_dict = ClusterOrderRequest.from_dict(cluster_order_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


