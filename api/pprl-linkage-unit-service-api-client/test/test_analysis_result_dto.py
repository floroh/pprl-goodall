# coding: utf-8

"""
    PPRL Linkage Unit Service API

    Linkage / Matching services for privacy-preserving record linkage

    The version of the OpenAPI document: 1.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from pprl_linkage_unit_service_api_client.models.analysis_result_dto import AnalysisResultDto

class TestAnalysisResultDto(unittest.TestCase):
    """AnalysisResultDto unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> AnalysisResultDto:
        """Test AnalysisResultDto
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `AnalysisResultDto`
        """
        model = AnalysisResultDto()
        if include_optional:
            return AnalysisResultDto(
                name = '',
                description = '',
                report_groups = {
                    'key' : pprl_linkage_unit_service_api_client.models.report_group.ReportGroup(
                        name = '', 
                        reports = {
                            'key' : pprl_linkage_unit_service_api_client.models.report.Report(
                                name = '', 
                                type = 'TEXT', 
                                report = '', 
                                table = pprl_linkage_unit_service_api_client.models.serializable_table.SerializableTable(
                                    name = '', 
                                    header = [
                                        ''
                                        ], 
                                    types = [
                                        ''
                                        ], 
                                    data = [
                                        [
                                            ''
                                            ]
                                        ], ), )
                            }, )
                    }
            )
        else:
            return AnalysisResultDto(
        )
        """

    def testAnalysisResultDto(self):
        """Test AnalysisResultDto"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
