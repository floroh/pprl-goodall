# coding: utf-8

"""
    PPRL Data Owner Service API

    Services for the data owners for privacy-preserving record linkage, including analysing and encoding of the local dataset

    The version of the OpenAPI document: 1.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from pprl_data_owner_service_api_client.models.multi_record_encoding_request_dto import MultiRecordEncodingRequestDto

class TestMultiRecordEncodingRequestDto(unittest.TestCase):
    """MultiRecordEncodingRequestDto unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> MultiRecordEncodingRequestDto:
        """Test MultiRecordEncodingRequestDto
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `MultiRecordEncodingRequestDto`
        """
        model = MultiRecordEncodingRequestDto()
        if include_optional:
            return MultiRecordEncodingRequestDto(
                encoding_id = pprl_data_owner_service_api_client.models.encoding_id_dto.EncodingIdDto(
                    method = '', 
                    project = '', ),
                records = [
                    pprl_data_owner_service_api_client.models.record_dto.RecordDto(
                        id = pprl_data_owner_service_api_client.models.record_id_dto.RecordIdDto(
                            unique = '', 
                            source = '', 
                            local = '', 
                            global = '', 
                            blocks = [
                                ''
                                ], ), 
                        dataset_id = 56, 
                        encoding_id = pprl_data_owner_service_api_client.models.encoding_id_dto.EncodingIdDto(
                            method = '', 
                            project = '', ), 
                        attributes = {
                            'key' : pprl_data_owner_service_api_client.models.attribute_dto.AttributeDto(
                                type = '', 
                                value = '', )
                            }, )
                    ]
            )
        else:
            return MultiRecordEncodingRequestDto(
        )
        """

    def testMultiRecordEncodingRequestDto(self):
        """Test MultiRecordEncodingRequestDto"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
