# ProcessingStep


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | [optional] 
**properties** | **Dict[str, str]** |  | [optional] 
**phase_progress** | [**PhaseProgress**](PhaseProgress.md) |  | [optional] 
**report_groups** | [**Dict[str, ReportGroup]**](ReportGroup.md) |  | [optional] 

## Example

```python
from pprl_protocol_manager_service_api_client.models.processing_step import ProcessingStep

# TODO update the JSON string below
json = "{}"
# create an instance of ProcessingStep from a JSON string
processing_step_instance = ProcessingStep.from_json(json)
# print the JSON string representation of the object
print(ProcessingStep.to_json())

# convert the object into a dict
processing_step_dict = processing_step_instance.to_dict()
# create an instance of ProcessingStep from a dict
processing_step_from_dict = ProcessingStep.from_dict(processing_step_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


