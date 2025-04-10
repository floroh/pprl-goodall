# BatchMatchProjectPhase


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**phase_progress** | [**PhaseProgress**](PhaseProgress.md) |  | [optional] 
**report_groups** | [**Dict[str, ReportGroup]**](ReportGroup.md) |  | [optional] 

## Example

```python
from pprl_linkage_unit_service_api_client.models.batch_match_project_phase import BatchMatchProjectPhase

# TODO update the JSON string below
json = "{}"
# create an instance of BatchMatchProjectPhase from a JSON string
batch_match_project_phase_instance = BatchMatchProjectPhase.from_json(json)
# print the JSON string representation of the object
print(BatchMatchProjectPhase.to_json())

# convert the object into a dict
batch_match_project_phase_dict = batch_match_project_phase_instance.to_dict()
# create an instance of BatchMatchProjectPhase from a dict
batch_match_project_phase_from_dict = BatchMatchProjectPhase.from_dict(batch_match_project_phase_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


