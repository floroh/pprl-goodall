# Layer


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**matcher_method** | **str** |  | [optional] 
**batch_size_config** | **List[int]** |  | [optional] 
**max_batches** | **int** |  | [optional] 
**encoding_method** | **str** |  | [optional] 
**update_matcher** | **bool** |  | [optional] 
**update_type** | **str** |  | [optional] 
**initial_threshold** | **float** |  | [optional] 
**budget** | **int** |  | [optional] 
**error_rate** | **float** |  | [optional] 
**project_id** | **str** |  | [optional] 
**batch_size** | **int** |  | [optional] 
**current_batch** | **int** |  | [optional] 
**number_of_reviews** | **int** |  | [optional] 
**active** | **bool** |  | [optional] 

## Example

```python
from pprl_protocol_manager_service_api_client.models.layer import Layer

# TODO update the JSON string below
json = "{}"
# create an instance of Layer from a JSON string
layer_instance = Layer.from_json(json)
# print the JSON string representation of the object
print(Layer.to_json())

# convert the object into a dict
layer_dict = layer_instance.to_dict()
# create an instance of Layer from a dict
layer_from_dict = Layer.from_dict(layer_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


