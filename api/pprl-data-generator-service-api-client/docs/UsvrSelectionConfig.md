# UsvrSelectionConfig


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dataset_variant_suffix** | **str** |  | [optional] 
**cluster_type** | **str** |  | [optional] 
**num_records_a** | **int** |  | [optional] 
**num_records_b** | **int** |  | [optional] 
**num_duplicates** | **int** |  | [optional] 
**num_clusters** | **int** |  | [optional] 
**snapshot_date_a** | **str** |  | [optional] 
**snapshot_date_b** | **str** |  | [optional] 
**source_a** | **str** |  | [optional] 
**source_b** | **str** |  | [optional] 
**attribute_columns** | **List[str]** |  | [optional] 
**ordering_strategy** | **str** |  | [optional] 
**ordering_seed** | **str** |  | [optional] 
**fix_yob_jitter** | **bool** |  | [optional] 
**change_filter** | [**ChangeFilter**](ChangeFilter.md) |  | [optional] 
**time_filter** | [**TimeFilter**](TimeFilter.md) |  | [optional] 
**content_filter** | [**ContentFilter**](ContentFilter.md) |  | [optional] 

## Example

```python
from pprl_data_generator_service_api_client.models.usvr_selection_config import UsvrSelectionConfig

# TODO update the JSON string below
json = "{}"
# create an instance of UsvrSelectionConfig from a JSON string
usvr_selection_config_instance = UsvrSelectionConfig.from_json(json)
# print the JSON string representation of the object
print(UsvrSelectionConfig.to_json())

# convert the object into a dict
usvr_selection_config_dict = usvr_selection_config_instance.to_dict()
# create an instance of UsvrSelectionConfig from a dict
usvr_selection_config_from_dict = UsvrSelectionConfig.from_dict(usvr_selection_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


