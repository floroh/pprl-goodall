# GroundTruthDto

Ground truth links of a dataset

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dataset_id** | **int** |  | [optional] 
**record_id_pairs** | [**List[RecordIdPairDto]**](RecordIdPairDto.md) |  | [optional] 

## Example

```python
from pprl_linkage_unit_service_api_client.models.ground_truth_dto import GroundTruthDto

# TODO update the JSON string below
json = "{}"
# create an instance of GroundTruthDto from a JSON string
ground_truth_dto_instance = GroundTruthDto.from_json(json)
# print the JSON string representation of the object
print(GroundTruthDto.to_json())

# convert the object into a dict
ground_truth_dto_dict = ground_truth_dto_instance.to_dict()
# create an instance of GroundTruthDto from a dict
ground_truth_dto_from_dict = GroundTruthDto.from_dict(ground_truth_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


