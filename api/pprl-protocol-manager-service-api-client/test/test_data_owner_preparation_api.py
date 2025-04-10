# coding: utf-8

"""
    PPRL Protocol Manager Service API

    Protocol manager service for privacy-preserving record linkage

    The version of the OpenAPI document: 1.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from pprl_protocol_manager_service_api_client.api.data_owner_preparation_api import DataOwnerPreparationApi


class TestDataOwnerPreparationApi(unittest.TestCase):
    """DataOwnerPreparationApi unit test stubs"""

    def setUp(self) -> None:
        self.api = DataOwnerPreparationApi()

    def tearDown(self) -> None:
        pass

    def test_insert_from_csv(self) -> None:
        """Test case for insert_from_csv

        Insert dataset from csv file
        """
        pass


if __name__ == '__main__':
    unittest.main()
