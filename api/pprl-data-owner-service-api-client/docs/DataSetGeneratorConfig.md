# DataSetGeneratorConfig

Configuration for generating the corrupted dataset

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Name of the configuration | [optional] 
**original_size** | **int** | Number of records from the original source | [optional] 
**modified_size** | **int** | Number of records from the modified source | [optional] 
**source_overlap** | **float** | Share of records from original source that have a duplicate in modified source | [optional] 
**input_filter** | [**SelectorRecord**](SelectorRecord.md) | Filter the input records before using them in the generator | [optional] 
**source_modifier_configs** | [**List[DataSetModifierConfig]**](DataSetModifierConfig.md) | Modifiers to sequentially apply on the input records before creating the modified two-source dataset | [optional] 
**duplicate_modifier_configs** | [**List[DataSetModifierConfig]**](DataSetModifierConfig.md) | Modifiers to create true matches and true non-matches | [optional] 
**seed** | **int** | Global seed for randomness, e.g., when shuffling the input records before corruption  Take care: Does not necessarily affect random selectors within modifier configs! | [optional] 
**modifier_distribution_strategy** | **str** | Setting on how to apply the duplicateModifierConfigs | [optional] 
**var_class** | **str** |  | 

## Example

```python
from pprl_data_owner_service_api_client.models.data_set_generator_config import DataSetGeneratorConfig

# TODO update the JSON string below
json = "{}"
# create an instance of DataSetGeneratorConfig from a JSON string
data_set_generator_config_instance = DataSetGeneratorConfig.from_json(json)
# print the JSON string representation of the object
print(DataSetGeneratorConfig.to_json())

# convert the object into a dict
data_set_generator_config_dict = data_set_generator_config_instance.to_dict()
# create an instance of DataSetGeneratorConfig from a dict
data_set_generator_config_from_dict = DataSetGeneratorConfig.from_dict(data_set_generator_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


