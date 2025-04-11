# ClusteringRequestDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**record_pairs** | [**List[RecordPairDto]**](RecordPairDto.md) |  | [optional] 
**method** | **str** |  | [optional] 

## Example

```python
from pprl_linkage_unit_service_api_client.models.clustering_request_dto import ClusteringRequestDto

# TODO update the JSON string below
json = "{}"
# create an instance of ClusteringRequestDto from a JSON string
clustering_request_dto_instance = ClusteringRequestDto.from_json(json)
# print the JSON string representation of the object
print(ClusteringRequestDto.to_json())

# convert the object into a dict
clustering_request_dto_dict = clustering_request_dto_instance.to_dict()
# create an instance of ClusteringRequestDto from a dict
clustering_request_dto_from_dict = ClusteringRequestDto.from_dict(clustering_request_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


