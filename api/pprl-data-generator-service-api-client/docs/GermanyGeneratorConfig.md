# GermanyGeneratorConfig


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**seed** | **str** |  | [optional] 
**number_of_records** | **int** |  | [optional] 
**include_household_structures** | **bool** |  | [optional] 
**include_header** | **bool** |  | [optional] 
**destination_folder** | **str** |  | [optional] 
**file_name** | **str** |  | [optional] 
**attributes** | **List[str]** |  | [optional] 
**source_name** | **str** |  | [optional] 

## Example

```python
from pprl_data_generator_service_api_client.models.germany_generator_config import GermanyGeneratorConfig

# TODO update the JSON string below
json = "{}"
# create an instance of GermanyGeneratorConfig from a JSON string
germany_generator_config_instance = GermanyGeneratorConfig.from_json(json)
# print the JSON string representation of the object
print(GermanyGeneratorConfig.to_json())

# convert the object into a dict
germany_generator_config_dict = germany_generator_config_instance.to_dict()
# create an instance of GermanyGeneratorConfig from a dict
germany_generator_config_from_dict = GermanyGeneratorConfig.from_dict(germany_generator_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


