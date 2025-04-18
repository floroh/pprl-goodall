# coding: utf-8

"""
    PPRL Protocol Manager Service API

    Protocol manager service for privacy-preserving record linkage

    The version of the OpenAPI document: 1.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from pprl_protocol_manager_service_api_client.models.multi_layer_protocol import MultiLayerProtocol

class TestMultiLayerProtocol(unittest.TestCase):
    """MultiLayerProtocol unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> MultiLayerProtocol:
        """Test MultiLayerProtocol
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `MultiLayerProtocol`
        """
        model = MultiLayerProtocol()
        if include_optional:
            return MultiLayerProtocol(
                protocol_id = '',
                layers = [
                    pprl_protocol_manager_service_api_client.models.layer.Layer(
                        name = '', 
                        matcher_method = '', 
                        batch_size_config = [
                            56
                            ], 
                        max_batches = 56, 
                        encoding_method = '', 
                        update_matcher = True, 
                        update_type = 'NEW_IMPROVED', 
                        initial_threshold = 1.337, 
                        budget = 56, 
                        error_rate = 1.337, 
                        project_id = '', 
                        batch_size = 56, 
                        current_batch = 56, 
                        number_of_reviews = 56, 
                        active = True, )
                    ],
                plaintext_dataset_id = 56,
                initial_dataset_id = 56,
                last_update = '',
                step_history = [
                    pprl_protocol_manager_service_api_client.models.processing_step.ProcessingStep(
                        type = '', 
                        properties = {
                            'key' : ''
                            }, 
                        phase_progress = pprl_protocol_manager_service_api_client.models.phase_progress.PhaseProgress(
                            done = True, 
                            progress = 1.337, 
                            description = '', ), 
                        report_groups = {
                            'key' : pprl_protocol_manager_service_api_client.models.report_group.ReportGroup(
                                name = '', 
                                reports = {
                                    'key' : pprl_protocol_manager_service_api_client.models.report.Report(
                                        name = '', 
                                        type = 'TEXT', 
                                        report = '', 
                                        table = pprl_protocol_manager_service_api_client.models.serializable_table.SerializableTable(
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
                            }, )
                    ],
                step_queue = [
                    pprl_protocol_manager_service_api_client.models.processing_step.ProcessingStep(
                        type = '', 
                        properties = {
                            'key' : ''
                            }, 
                        phase_progress = pprl_protocol_manager_service_api_client.models.phase_progress.PhaseProgress(
                            done = True, 
                            progress = 1.337, 
                            description = '', ), 
                        report_groups = {
                            'key' : pprl_protocol_manager_service_api_client.models.report_group.ReportGroup(
                                name = '', 
                                reports = {
                                    'key' : pprl_protocol_manager_service_api_client.models.report.Report(
                                        name = '', 
                                        type = 'TEXT', 
                                        report = '', 
                                        table = pprl_protocol_manager_service_api_client.models.serializable_table.SerializableTable(
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
                            }, )
                    ]
            )
        else:
            return MultiLayerProtocol(
        )
        """

    def testMultiLayerProtocol(self):
        """Test MultiLayerProtocol"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
