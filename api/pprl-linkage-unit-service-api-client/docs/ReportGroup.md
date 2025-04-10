# ReportGroup


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**reports** | [**Dict[str, Report]**](Report.md) |  | [optional] 

## Example

```python
from pprl_linkage_unit_service_api_client.models.report_group import ReportGroup

# TODO update the JSON string below
json = "{}"
# create an instance of ReportGroup from a JSON string
report_group_instance = ReportGroup.from_json(json)
# print the JSON string representation of the object
print(ReportGroup.to_json())

# convert the object into a dict
report_group_dict = report_group_instance.to_dict()
# create an instance of ReportGroup from a dict
report_group_from_dict = ReportGroup.from_dict(report_group_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


