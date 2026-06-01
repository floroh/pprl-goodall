# EncodingCreationRequestDto

Request for creating an encoding definition.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**weight_selection_method** | **str** |  | [optional] 
**frequency_selection_method** | **str** |  | [optional] 
**encoding_creation_method** | **str** |  | [optional] 
**base_encoding_id** | [**EncodingIdDto**](EncodingIdDto.md) |  | [optional] 
**output_encoding_id** | [**EncodingIdDto**](EncodingIdDto.md) |  | [optional] 
**attribute_weights** | **Dict[str, float]** |  | [optional] 
**attribute_length** | **Dict[str, float]** |  | [optional] 
**source_specific** | **bool** |  | [optional] 
**attribute_error_rates** | **Dict[str, float]** | Precomputed/estimated error rates.Required if sourceSpecific &#x3D; true because the error rate cannot be determined per source. | [optional] 
**source_specific_attribute_weights** | **Dict[str, Dict[str, float]]** | Attribute weights for each data source. Only relevant if sourceSpecific &#x3D; true. | [optional] 
**source_specific_attribute_length** | **Dict[str, Dict[str, float]]** | Attribute lengths for each data source. Only relevant if sourceSpecific &#x3D; true. | [optional] 
**sources** | **List[str]** | Names of sources. Only relevant for sourceSpecific &#x3D; true and WeightSelectionMethod.None. | [optional] 
**dataset_id** | **int** |  | [optional] 
**average_fillrate** | **float** |  | [optional] 
**max_fillrate** | **float** |  | [optional] 
**bloom_filter_size** | **int** |  | [optional] 
**persist** | **bool** |  | [optional] 

## Example

```python
from pprl_data_owner_service_api_client.models.encoding_creation_request_dto import EncodingCreationRequestDto

# TODO update the JSON string below
json = "{}"
# create an instance of EncodingCreationRequestDto from a JSON string
encoding_creation_request_dto_instance = EncodingCreationRequestDto.from_json(json)
# print the JSON string representation of the object
print(EncodingCreationRequestDto.to_json())

# convert the object into a dict
encoding_creation_request_dto_dict = encoding_creation_request_dto_instance.to_dict()
# create an instance of EncodingCreationRequestDto from a dict
encoding_creation_request_dto_from_dict = EncodingCreationRequestDto.from_dict(encoding_creation_request_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


