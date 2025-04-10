# coding: utf-8

"""
    PPRL Protocol Manager Service API

    Protocol manager service for privacy-preserving record linkage

    The version of the OpenAPI document: 1.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from pprl_protocol_manager_service_api_client.models.report import Report
from typing import Optional, Set
from typing_extensions import Self

class ReportGroup(BaseModel):
    """
    ReportGroup
    """ # noqa: E501
    name: Optional[StrictStr] = None
    reports: Optional[Dict[str, Report]] = None
    __properties: ClassVar[List[str]] = ["name", "reports"]

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
        """Create an instance of ReportGroup from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each value in reports (dict)
        _field_dict = {}
        if self.reports:
            for _key_reports in self.reports:
                if self.reports[_key_reports]:
                    _field_dict[_key_reports] = self.reports[_key_reports].to_dict()
            _dict['reports'] = _field_dict
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of ReportGroup from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "name": obj.get("name"),
            "reports": dict(
                (_k, Report.from_dict(_v))
                for _k, _v in obj["reports"].items()
            )
            if obj.get("reports") is not None
            else None
        })
        return _obj


