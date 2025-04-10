# AnalysisResultDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**report_groups** | [**Dict[str, ReportGroup]**](ReportGroup.md) |  | [optional] 

## Example

```python
from pprl_linkage_unit_service_api_client.models.analysis_result_dto import AnalysisResultDto

# TODO update the JSON string below
json = "{}"
# create an instance of AnalysisResultDto from a JSON string
analysis_result_dto_instance = AnalysisResultDto.from_json(json)
# print the JSON string representation of the object
print(AnalysisResultDto.to_json())

# convert the object into a dict
analysis_result_dto_dict = analysis_result_dto_instance.to_dict()
# create an instance of AnalysisResultDto from a dict
analysis_result_dto_from_dict = AnalysisResultDto.from_dict(analysis_result_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


