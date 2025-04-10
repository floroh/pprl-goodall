# PhaseProgress


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**done** | **bool** |  | [optional] 
**progress** | **float** |  | [optional] 
**description** | **str** |  | [optional] 

## Example

```python
from pprl_linkage_unit_service_api_client.models.phase_progress import PhaseProgress

# TODO update the JSON string below
json = "{}"
# create an instance of PhaseProgress from a JSON string
phase_progress_instance = PhaseProgress.from_json(json)
# print the JSON string representation of the object
print(PhaseProgress.to_json())

# convert the object into a dict
phase_progress_dict = phase_progress_instance.to_dict()
# create an instance of PhaseProgress from a dict
phase_progress_from_dict = PhaseProgress.from_dict(phase_progress_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


