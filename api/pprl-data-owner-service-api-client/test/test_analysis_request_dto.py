# coding: utf-8

"""
    PPRL Data Owner Service API

    Services for the data owners for privacy-preserving record linkage, including analysing and encoding of the local dataset

    The version of the OpenAPI document: 1.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from pprl_data_owner_service_api_client.models.analysis_request_dto import AnalysisRequestDto

class TestAnalysisRequestDto(unittest.TestCase):
    """AnalysisRequestDto unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> AnalysisRequestDto:
        """Test AnalysisRequestDto
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `AnalysisRequestDto`
        """
        model = AnalysisRequestDto()
        if include_optional:
            return AnalysisRequestDto(
                dataset_id = 56,
                project_id = '',
                type = '',
                parameters = {
                    'key' : ''
                    }
            )
        else:
            return AnalysisRequestDto(
        )
        """

    def testAnalysisRequestDto(self):
        """Test AnalysisRequestDto"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
