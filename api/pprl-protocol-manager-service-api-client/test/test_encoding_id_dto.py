# coding: utf-8

"""
    PPRL Protocol Manager Service API

    Protocol manager service for privacy-preserving record linkage

    The version of the OpenAPI document: 1.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from pprl_protocol_manager_service_api_client.models.encoding_id_dto import EncodingIdDto

class TestEncodingIdDto(unittest.TestCase):
    """EncodingIdDto unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> EncodingIdDto:
        """Test EncodingIdDto
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `EncodingIdDto`
        """
        model = EncodingIdDto()
        if include_optional:
            return EncodingIdDto(
                method = '',
                project = ''
            )
        else:
            return EncodingIdDto(
        )
        """

    def testEncodingIdDto(self):
        """Test EncodingIdDto"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
