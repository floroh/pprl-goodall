# coding: utf-8

"""
    PPRL Linkage Unit Service API

    Linkage / Matching services for privacy-preserving record linkage

    The version of the OpenAPI document: 1.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from pprl_linkage_unit_service_api_client.models.record_dto import RecordDto

class TestRecordDto(unittest.TestCase):
    """RecordDto unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> RecordDto:
        """Test RecordDto
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `RecordDto`
        """
        model = RecordDto()
        if include_optional:
            return RecordDto(
                id = pprl_linkage_unit_service_api_client.models.record_id_dto.RecordIdDto(
                    unique = '', 
                    source = '', 
                    local = '', 
                    global = '', 
                    blocks = [
                        ''
                        ], ),
                dataset_id = 56,
                encoding_id = pprl_linkage_unit_service_api_client.models.encoding_id_dto.EncodingIdDto(
                    method = '', 
                    project = '', ),
                attributes = {
                    'key' : pprl_linkage_unit_service_api_client.models.attribute_dto.AttributeDto(
                        type = '', 
                        value = '', )
                    }
            )
        else:
            return RecordDto(
        )
        """

    def testRecordDto(self):
        """Test RecordDto"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
