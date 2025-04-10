# ProtocolExecutionDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**protocol_id** | **str** |  | [optional] 
**number_of_steps** | **int** |  | [optional] 
**step_to_stop** | **str** |  | [optional] 

## Example

```python
from pprl_protocol_manager_service_api_client.models.protocol_execution_dto import ProtocolExecutionDto

# TODO update the JSON string below
json = "{}"
# create an instance of ProtocolExecutionDto from a JSON string
protocol_execution_dto_instance = ProtocolExecutionDto.from_json(json)
# print the JSON string representation of the object
print(ProtocolExecutionDto.to_json())

# convert the object into a dict
protocol_execution_dto_dict = protocol_execution_dto_instance.to_dict()
# create an instance of ProtocolExecutionDto from a dict
protocol_execution_dto_from_dict = ProtocolExecutionDto.from_dict(protocol_execution_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


