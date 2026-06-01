# ProtocolAnalysisRequestDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**protocol_id** | **str** |  | [optional] 
**type** | **str** |  | [optional] 
**parameters** | **Dict[str, str]** |  | [optional] 

## Example

```python
from pprl_protocol_manager_service_api_client.models.protocol_analysis_request_dto import ProtocolAnalysisRequestDto

# TODO update the JSON string below
json = "{}"
# create an instance of ProtocolAnalysisRequestDto from a JSON string
protocol_analysis_request_dto_instance = ProtocolAnalysisRequestDto.from_json(json)
# print the JSON string representation of the object
print(ProtocolAnalysisRequestDto.to_json())

# convert the object into a dict
protocol_analysis_request_dto_dict = protocol_analysis_request_dto_instance.to_dict()
# create an instance of ProtocolAnalysisRequestDto from a dict
protocol_analysis_request_dto_from_dict = ProtocolAnalysisRequestDto.from_dict(protocol_analysis_request_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


