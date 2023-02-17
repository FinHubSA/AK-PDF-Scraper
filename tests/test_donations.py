import unittest
from unittest import mock
from unittest.mock import patch
from algosdk import encoding
import os
import json

from src.donations import (
    create_account,
    store_address,
    check_address_on_record,
    validate_correct_address,
)
from src.temp_storage import misc_path
from src.helpers import get_user_address_from_json

misc_directory = misc_path()


class TestDonations(unittest.TestCase):
    def test_create_account(self):

        user_address = create_account()[1]
        self.assertTrue(encoding.is_valid_address(user_address))

    def test_store_address(self):

        user_address = create_account()[1]

        store_address(user_address)

        user_address_dict = get_user_address_from_json(misc_directory)

        self.assertEqual(user_address, user_address_dict["address"])

    # def test_validate_correct_address_yes(self):
    #     inputs_list = ["y", "Y"]

    #     store_address("IZ5X3C3TS33UBYEZPSQBGBPULS7ROJVKOHLVS7GQE2SMUKP5DP5KFRXLMU")

    #     for input in inputs_list:
    #         self.assertEqual(
    #             validate_correct_address(input),
    #             "IZ5X3C3TS33UBYEZPSQBGBPULS7ROJVKOHLVS7GQE2SMUKP5DP5KFRXLMU",
    #         )

    # @patch("src.donations.get_input", return_value="N4RPE6CUFVJSUUUQNRK7WWJ2HAVYDSMSPHBJ47TQSPTXR4QF7SF36ETLMY")
    # def test_validate_correct_address_no(self, input):
    #     inputs_list = ["n", "N"]

    #     for input in inputs_list:

    # def test_check_address_on_record_no(self):

    #     store_address("")

    #     self.assertEqual(check_address_on_record()[0], "")
    #     self.assertEqual(check_address_on_record()[1], "n")

    # @patch("src.donations.get_input", return_value="y")
    # def test_check_address_on_record_yes(self, input):

    #     store_address("IZ5X3C3TS33UBYEZPSQBGBPULS7ROJVKOHLVS7GQE2SMUKP5DP5KFRXLMU")

    #     self.assertEqual(
    #         check_address_on_record()[0],
    #         "IZ5X3C3TS33UBYEZPSQBGBPULS7ROJVKOHLVS7GQE2SMUKP5DP5KFRXLMU",
    #     )

    #     self.assertEqual(
    #         check_address_on_record()[1],
    #         "y",
    #     )


if __name__ == "__main__":
    unittest.main()
