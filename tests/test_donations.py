import unittest
from unittest import mock
from unittest.mock import patch
from algosdk import encoding
import os
import json
from src.errors import TypoException, MainException

from src.donations import (
    create_account,
    store_address,
    check_address_on_record,
    validate_correct_address,
    validate_existing_account,
    process_validation_action,
    receive_not_validated_action,
    process_donation_action,
    receive_donation_action,
)
from src.temp_storage import misc_path
from src.helpers import get_user_address_from_json

misc_directory = misc_path()

test_address = "N4RPE6CUFVJSUUUQNRK7WWJ2HAVYDSMSPHBJ47TQSPTXR4QF7SF36ETLMY"


class TestDonations(unittest.TestCase):

    # set up inputs
    def setUp(self):
        self.input_1 = "N"
        self.input_2 = "n"
        self.input_3 = "$"
        self.input_4 = "1"
        self.input_5 = "2"
        self.input_6 = "3"
        self.input_7 = "4"

    # test store_address
    def test_store_address(self):

        store_address(test_address)

        user_address_dict = get_user_address_from_json(misc_directory)

        self.assertEqual(test_address, user_address_dict["address"])

    # test create account
    def test_create_account(self):

        address = create_account()[1]

        self.assertTrue(encoding.is_valid_address(address))

    # test validate_correct_address
    @patch(
        "src.donations.validate_existing_account",
        return_value=test_address,
    )
    def test_validate_correct_address(self, input):

        # Lowercase n
        self.assertEqual(
            validate_correct_address(self.input_1),
            test_address,
        )
        # Uppercase N
        self.assertEqual(
            validate_correct_address(self.input_2),
            test_address,
        )

        # Typo
        with self.assertRaises(TypoException):
            validate_correct_address(self.input_3)

    # test check_address_on_record
    # Address on record but not the correct one
    @patch("src.donations.get_input")
    def test_check_address_on_record_1(self, input):

        store_address(test_address)

        with mock.patch(
            "src.donations.get_input",
            side_effect=[
                "n",
                "IZ5X3C3TS33UBYEZPSQBGBPULS7ROJVKOHLVS7GQE2SMUKP5DP5KFRXLMU",
            ],
        ):
            self.assertEqual(
                check_address_on_record(),
                "IZ5X3C3TS33UBYEZPSQBGBPULS7ROJVKOHLVS7GQE2SMUKP5DP5KFRXLMU",
            )

    # test check_address_on_record
    # Address on record and the correct one
    @patch("src.donations.get_input", return_value="y")
    def test_check_address_on_record_2(self, input):

        store_address(test_address)

        self.assertEqual(
            check_address_on_record(),
            test_address,
        )

    # test check_address_on_record
    # Address not on record
    @patch(
        "src.donations.get_input",
        return_value=test_address,
    )
    def test_check_address_on_record_3(self, input):

        store_address("")

        self.assertEqual(
            check_address_on_record(),
            test_address,
        )

    # test validate_existing_account
    # Address is correct
    @patch(
        "src.donations.get_input",
        return_value=test_address,
    )
    def test_validate_existing_account_1(self, input):

        self.assertEqual(
            validate_existing_account(),
            test_address,
        )

    # test validate_existing_account
    # Address is incorrect
    @patch("src.donations.get_input")
    def test_validate_existing_account_2(self, input):

        with mock.patch(
            "src.donations.get_input",
            side_effect=[
                "QVLEXG2GMTP5BL2BDQKTTJYQHLGOXZ43W5DWJER7RDODBH7WSZRDA4N4",
                "1",
                test_address,
            ],
        ):

            self.assertEqual(
                validate_existing_account(),
                test_address,
            )

    # test process_validation_action
    @patch("src.donations.get_input")
    def test_process_validation_action(self, input):

        # Input option 1 (retry)
        store_address(test_address)

        with mock.patch(
            "src.donations.get_input",
            side_effect=[
                "IZ5X3C3TS33UBYEZPSQBGBPULS7ROJVKOHLVS7GQE2SMUKP5DP5KFRXLMU",
            ],
        ):
            self.assertEqual(
                process_validation_action(self.input_4),
                "IZ5X3C3TS33UBYEZPSQBGBPULS7ROJVKOHLVS7GQE2SMUKP5DP5KFRXLMU",
            )

        # Input option 2 (create a new account)
        self.assertTrue(
            encoding.is_valid_address(process_validation_action(self.input_5))
        )

        # Input option 3 (go back to donation menu)
        with mock.patch(
            "src.donations.get_input",
            side_effect=["4", "3"],
        ):
            with self.assertRaises(MainException):
                process_validation_action(self.input_6)

        # Input option 4 (typo)
        with self.assertRaises(TypoException):
            process_validation_action(self.input_3)

    # test receive_not_validated_action
    # Valid input
    @patch("src.donations.get_input", return_value="2")
    def test_receive_not_validated_action_1(self, input):

        self.assertTrue(encoding.is_valid_address(receive_not_validated_action()))

    # Typo
    @patch("src.donations.get_input")
    def test_receive_not_validated_action_2(self, input):

        with mock.patch(
            "src.donations.get_input",
            side_effect=["$", "2", ""],
        ):
            self.assertTrue(encoding.is_valid_address(receive_not_validated_action()))

    # test process_donation_action
    @patch("src.donations.get_input")
    def test_process_donation_action(self, input):

        # Input option 1.1 (existing address + no typo)
        store_address(test_address)

        with mock.patch(
            "src.donations.get_input",
            side_effect=["Y"],
        ):

            self.assertEqual(
                process_donation_action(self.input_4),
                test_address,
            )

        # Input option 1.2 (existing address + typo)
        with mock.patch(
            "src.donations.get_input",
            side_effect=["$", "Y"],
        ):
            self.assertEqual(
                process_donation_action(self.input_4),
                test_address,
            )

        # Input option 2 (create account)
        self.assertTrue(
            encoding.is_valid_address(process_donation_action(self.input_5))
        )

        # Input option 3 (don't want donations)
        self.assertIsNone(process_donation_action(self.input_6))

        # Input option 4 (back to main)
        with self.assertRaises(MainException):
            process_donation_action(self.input_7)

        # Typo
        with self.assertRaises(TypoException):
            process_donation_action(self.input_3)

    # test receive_donation_action
    @patch("src.donations.get_input")
    def test_receive_donation_action(self, input):

        # Valid input
        with mock.patch(
            "src.donations.get_input",
            side_effect=["3"],
        ):

            self.assertIsNone(receive_donation_action())

        # Typo
        with mock.patch(
            "src.donations.get_input",
            side_effect=["$", "3"],
        ):

            self.assertIsNone(receive_donation_action())


if __name__ == "__main__":
    unittest.main()
