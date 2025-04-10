# MultiLayerProtocol


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**protocol_id** | **str** |  | [optional] 
**layers** | [**List[Layer]**](Layer.md) |  | [optional] 
**plaintext_dataset_id** | **int** |  | [optional] 
**initial_dataset_id** | **int** |  | [optional] 
**last_update** | **str** |  | [optional] 
**step_history** | [**List[ProcessingStep]**](ProcessingStep.md) |  | [optional] 
**step_queue** | [**List[ProcessingStep]**](ProcessingStep.md) |  | [optional] 

## Example

```python
from pprl_protocol_manager_service_api_client.models.multi_layer_protocol import MultiLayerProtocol

# TODO update the JSON string below
json = "{}"
# create an instance of MultiLayerProtocol from a JSON string
multi_layer_protocol_instance = MultiLayerProtocol.from_json(json)
# print the JSON string representation of the object
print(MultiLayerProtocol.to_json())

# convert the object into a dict
multi_layer_protocol_dict = multi_layer_protocol_instance.to_dict()
# create an instance of MultiLayerProtocol from a dict
multi_layer_protocol_from_dict = MultiLayerProtocol.from_dict(multi_layer_protocol_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


