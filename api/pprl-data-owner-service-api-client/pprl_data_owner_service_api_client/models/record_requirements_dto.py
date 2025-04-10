# coding: utf-8

"""
    PPRL Data Owner Service API

    Services for the data owners for privacy-preserving record linkage, including analysing and encoding of the local dataset

    The version of the OpenAPI document: 1.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from pprl_data_owner_service_api_client.models.attribute_description_dto import AttributeDescriptionDto
from typing import Optional, Set
from typing_extensions import Self

class RecordRequirementsDto(BaseModel):
    """
    Description of requirements for this scheme
    """ # noqa: E501
    method: Optional[StrictStr] = None
    supported_encoding_methods: Optional[List[StrictStr]] = Field(default=None, description="List of encoding methods that can be matched with this scheme", alias="supportedEncodingMethods")
    attributes: Optional[List[AttributeDescriptionDto]] = None
    __properties: ClassVar[List[str]] = ["method", "supportedEncodingMethods", "attributes"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of RecordRequirementsDto from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of each item in attributes (list)
        _items = []
        if self.attributes:
            for _item_attributes in self.attributes:
                if _item_attributes:
                    _items.append(_item_attributes.to_dict())
            _dict['attributes'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of RecordRequirementsDto from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "method": obj.get("method"),
            "supportedEncodingMethods": obj.get("supportedEncodingMethods"),
            "attributes": [AttributeDescriptionDto.from_dict(_item) for _item in obj["attributes"]] if obj.get("attributes") is not None else None
        })
        return _obj


