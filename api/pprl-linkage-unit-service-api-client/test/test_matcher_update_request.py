# coding: utf-8

"""
    PPRL Linkage Unit Service API

    Linkage / Matching services for privacy-preserving record linkage

    The version of the OpenAPI document: 1.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from pprl_linkage_unit_service_api_client.models.matcher_update_request import MatcherUpdateRequest

class TestMatcherUpdateRequest(unittest.TestCase):
    """MatcherUpdateRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> MatcherUpdateRequest:
        """Test MatcherUpdateRequest
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `MatcherUpdateRequest`
        """
        model = MatcherUpdateRequest()
        if include_optional:
            return MatcherUpdateRequest(
                project_id = '',
                type = 'NEW_IMPROVED'
            )
        else:
            return MatcherUpdateRequest(
        )
        """

    def testMatcherUpdateRequest(self):
        """Test MatcherUpdateRequest"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
