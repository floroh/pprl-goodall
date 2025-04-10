# coding: utf-8

"""
    PPRL Linkage Unit Service API

    Linkage / Matching services for privacy-preserving record linkage

    The version of the OpenAPI document: 1.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from pprl_linkage_unit_service_api_client.models.clustering_request_dto import ClusteringRequestDto

class TestClusteringRequestDto(unittest.TestCase):
    """ClusteringRequestDto unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> ClusteringRequestDto:
        """Test ClusteringRequestDto
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `ClusteringRequestDto`
        """
        model = ClusteringRequestDto()
        if include_optional:
            return ClusteringRequestDto(
                record_pairs = [
                    pprl_linkage_unit_service_api_client.models.record_pair_dto.RecordPairDto(
                        id0 = pprl_linkage_unit_service_api_client.models.record_id_dto.RecordIdDto(
                            unique = '', 
                            source = '', 
                            local = '', 
                            global = '', 
                            blocks = [
                                ''
                                ], ), 
                        id1 = pprl_linkage_unit_service_api_client.models.record_id_dto.RecordIdDto(
                            unique = '', 
                            source = '', 
                            local = '', 
                            global = '', ), 
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
                    ],
                method = ''
            )
        else:
            return ClusteringRequestDto(
        )
        """

    def testClusteringRequestDto(self):
        """Test ClusteringRequestDto"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
