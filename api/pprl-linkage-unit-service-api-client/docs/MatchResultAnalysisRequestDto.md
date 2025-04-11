# MatchResultAnalysisRequestDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**analysis_request** | [**AnalysisRequestDto**](AnalysisRequestDto.md) |  | [optional] 
**match_result** | [**MatchResultDto**](MatchResultDto.md) |  | [optional] 

## Example

```python
from pprl_linkage_unit_service_api_client.models.match_result_analysis_request_dto import MatchResultAnalysisRequestDto

# TODO update the JSON string below
json = "{}"
# create an instance of MatchResultAnalysisRequestDto from a JSON string
match_result_analysis_request_dto_instance = MatchResultAnalysisRequestDto.from_json(json)
# print the JSON string representation of the object
print(MatchResultAnalysisRequestDto.to_json())

# convert the object into a dict
match_result_analysis_request_dto_dict = match_result_analysis_request_dto_instance.to_dict()
# create an instance of MatchResultAnalysisRequestDto from a dict
match_result_analysis_request_dto_from_dict = MatchResultAnalysisRequestDto.from_dict(match_result_analysis_request_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


