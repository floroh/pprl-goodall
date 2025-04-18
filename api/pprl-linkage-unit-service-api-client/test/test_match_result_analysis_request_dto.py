# coding: utf-8

"""
    PPRL Linkage Unit Service API

    Linkage / Matching services for privacy-preserving record linkage

    The version of the OpenAPI document: 1.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from pprl_linkage_unit_service_api_client.models.match_result_analysis_request_dto import MatchResultAnalysisRequestDto

class TestMatchResultAnalysisRequestDto(unittest.TestCase):
    """MatchResultAnalysisRequestDto unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> MatchResultAnalysisRequestDto:
        """Test MatchResultAnalysisRequestDto
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `MatchResultAnalysisRequestDto`
        """
        model = MatchResultAnalysisRequestDto()
        if include_optional:
            return MatchResultAnalysisRequestDto(
                analysis_request = pprl_linkage_unit_service_api_client.models.analysis_request_dto.AnalysisRequestDto(
                    dataset_id = 56, 
                    project_id = '', 
                    type = '', 
                    parameters = {
                        'key' : ''
                        }, ),
                match_result = pprl_linkage_unit_service_api_client.models.match_result_dto.MatchResultDto(
                    records = [
                        pprl_linkage_unit_service_api_client.models.record_dto.RecordDto(
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
                                }, )
                        ], 
                    record_ids = [
                        pprl_linkage_unit_service_api_client.models.record_id_dto.RecordIdDto(
                            unique = '', 
                            source = '', 
                            local = '', 
                            global = '', )
                        ], 
                    record_pairs = [
                        pprl_linkage_unit_service_api_client.models.record_pair_dto.RecordPairDto(
                            id0 = , 
                            id1 = , 
                            project_id = '', 
                            match_grade = '', 
                            similarity = 1.337, 
                            properties = [
                                ''
                                ], 
                            attribute_similarities = {
                                'key' : 1.337
                                }, 
                            tags = [
                                pprl_linkage_unit_service_api_client.models.tag.Tag(
                                    attribute = '', 
                                    tag = '', 
                                    string_value = '', 
                                    numeric_value = 1.337, )
                                ], )
                        ], )
            )
        else:
            return MatchResultAnalysisRequestDto(
        )
        """

    def testMatchResultAnalysisRequestDto(self):
        """Test MatchResultAnalysisRequestDto"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
