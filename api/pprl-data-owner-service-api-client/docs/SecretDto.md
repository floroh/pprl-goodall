# SecretDto

Project-specific secret necessary to create unique encodings per project, that is is only known to the data owners

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**project** | **str** | Unique name of the record-linkage project | 
**secret** | **str** | Secret value | 

## Example

```python
from pprl_data_owner_service_api_client.models.secret_dto import SecretDto

# TODO update the JSON string below
json = "{}"
# create an instance of SecretDto from a JSON string
secret_dto_instance = SecretDto.from_json(json)
# print the JSON string representation of the object
print(SecretDto.to_json())

# convert the object into a dict
secret_dto_dict = secret_dto_instance.to_dict()
# create an instance of SecretDto from a dict
secret_dto_from_dict = SecretDto.from_dict(secret_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


