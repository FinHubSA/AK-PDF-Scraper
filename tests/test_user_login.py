import unittest
import os, sys
from unittest import mock
from unittest.mock import patch
from src.errors import MainException, TypoException

from src.user_login import (
    receive_login_action,
    validate_login,
    vpn_login,
    manual_login,
    validate_page_load,
    receive_proceed_action,
    receive_end_program_action,
    process_end_program_action,
)

from src.contribute_papers import create_driver_session, options
from src.temp_storage import get_temp_storage_path

# connect to uct VPN before testing

storage_directory = get_temp_storage_path()
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36"


class TestUserLogin(unittest.TestCase):
    def setUp(self):
        self.input_1 = "1"
        self.input_2 = "2"
        self.input_3 = "3"
        self.input_4 = "$"

    # test process_end_program_action
    def test_process_end_program_action(self):

        os._exit = sys.exit

        with self.assertRaises(SystemExit):
            process_end_program_action(
                create_driver_session(options(1, USER_AGENT, storage_directory)),
                self.input_1,
            )

        restart_count = process_end_program_action(
            create_driver_session(options(1, USER_AGENT, storage_directory)),
            self.input_2,
        )

        self.assertEqual(restart_count, 0)

        with self.assertRaises(MainException):
            process_end_program_action(
                create_driver_session(options(1, USER_AGENT, storage_directory)),
                self.input_3,
            )

        with self.assertRaises(TypoException):
            process_end_program_action(
                create_driver_session(options(1, USER_AGENT, storage_directory)),
                self.input_4,
            )

    # test receive_end_program_action
    def test_receive_end_program_action(self):

        with mock.patch(
            "src.user_login.get_input",
            side_effect=[
                self.input_1,
            ],
        ):

            os._exit = sys.exit

            with self.assertRaises(SystemExit):
                receive_end_program_action(
                    create_driver_session(options(1, USER_AGENT, storage_directory))
                )

        with mock.patch(
            "src.user_login.get_input",
            side_effect=[
                self.input_2,
            ],
        ):
            restart_count = receive_end_program_action(
                create_driver_session(options(1, USER_AGENT, storage_directory))
            )

            self.assertEqual(restart_count, 0)

        with mock.patch(
            "src.user_login.get_input",
            side_effect=[
                self.input_3,
            ],
        ):
            with self.assertRaises(MainException):
                receive_end_program_action(
                    create_driver_session(options(1, USER_AGENT, storage_directory))
                )

        with mock.patch(
            "src.user_login.get_input",
            side_effect=[self.input_4, self.input_3],
        ):
            with self.assertRaises(MainException):
                receive_end_program_action(
                    create_driver_session(options(1, USER_AGENT, storage_directory))
                )

    # test receive_proceed_action
    def test_receive_proceed_action(self):

        with mock.patch(
            "src.user_login.get_input",
            side_effect=[
                self.input_1,
            ],
        ):
            self.assertEqual(receive_proceed_action(), "1")

        with mock.patch(
            "src.user_login.get_input",
            side_effect=[
                self.input_2,
            ],
        ):
            self.assertEqual(receive_proceed_action(), "2")

        with mock.patch(
            "src.user_login.get_input",
            side_effect=[self.input_4, self.input_2],
        ):
            self.assertEqual(receive_proceed_action(), "2")

    # test validate_login
    # pass
    def test_validate_login(self):

        driver = create_driver_session(options(1, USER_AGENT, storage_directory))

        driver.get("https://www.jstor.org/")

        self.assertEqual(
            validate_login(driver, "pds__access-provided-by"),
            True,
        )

    # test validate_login
    # fail
    def test_validate_login(self):

        driver = create_driver_session(options(1, USER_AGENT, storage_directory))

        driver.get("https://www.jstor.org/")

        self.assertEqual(
            validate_login(driver, "pds__access-provided-b"),
            False,
        )

    # test validate_page_load
    # fail
    def test_validate_page_load(self):

        self.assertEqual(
            validate_page_load(
                create_driver_session(options(1, USER_AGENT, storage_directory)),
                "query-builder-input-group",
            ),
            False,
        )

    # test manual_login
    def test_manual_login(self):

        # page load unsucessfull
        self.assertEqual(
            manual_login(
                create_driver_session(options(1, USER_AGENT, storage_directory)),
                "https://github.com/",
                "query-builder-input-group",
                "pds__access-provided-by",
            ),
            False,
        )

        # page load sucessfull, don't proceed with login
        with mock.patch("src.user_login.get_input", side_effect=[self.input_2]):

            self.assertEqual(
                manual_login(
                    create_driver_session(options(1, USER_AGENT, storage_directory)),
                    "https://www.jstor.org/",
                    "query-builder-input-group",
                    "pds__access-provided-by",
                ),
                False,
            )

        # page load sucessfull, proceed with login, login successful
        with mock.patch("src.user_login.get_input", side_effect=[self.input_1]):

            self.assertEqual(
                manual_login(
                    create_driver_session(options(1, USER_AGENT, storage_directory)),
                    "https://www.jstor.org/",
                    "query-builder-input-group",
                    "pds__access-provided-by",
                ),
                True,
            )

        # page load sucessfull, proceed with login, login unsuccessful
        with mock.patch("src.user_login.get_input", side_effect=[self.input_1]):

            self.assertEqual(
                manual_login(
                    create_driver_session(options(1, USER_AGENT, storage_directory)),
                    "https://www.jstor.org/",
                    "query-builder-input-group",
                    "pds__access-provided-b",
                ),
                False,
            )

    # test vpn_login
    def test_vpn_login(self):

        # don't proceed with login
        with mock.patch("src.user_login.get_input", side_effect=[self.input_2]):

            self.assertEqual(
                vpn_login(
                    create_driver_session(options(2, USER_AGENT, storage_directory)),
                    "https://www.jstor.org/",
                    "query-builder-input-group",
                    "pds__access-provided-by",
                ),
                False,
            )

        # proceed with login, page load unsucessful
        with mock.patch("src.user_login.get_input", side_effect=[self.input_1]):

            self.assertEqual(
                vpn_login(
                    create_driver_session(options(2, USER_AGENT, storage_directory)),
                    "https://www.jstor.org/",
                    "query-builder-input-grou",
                    "pds__access-provided-by",
                ),
                False,
            )

        # proceed with login, page load sucessful, login unsucessful
        with mock.patch("src.user_login.get_input", side_effect=[self.input_1]):

            self.assertEqual(
                vpn_login(
                    create_driver_session(options(2, USER_AGENT, storage_directory)),
                    "https://www.jstor.org/",
                    "query-builder-input-group",
                    "pds__access-provided-b",
                ),
                False,
            )

            # proceed with login, page load sucessful, login sucessful
            with mock.patch("src.user_login.get_input", side_effect=[self.input_1]):

                self.assertEqual(
                    vpn_login(
                        create_driver_session(
                            options(2, USER_AGENT, storage_directory)
                        ),
                        "https://www.jstor.org/",
                        "query-builder-input-group",
                        "pds__access-provided-by",
                    ),
                    True,
                )

    # test receive_login_action
    def test_receive_login_action(self):

        with mock.patch("src.user_login.get_input", side_effect=[self.input_1]):

            self.assertEqual(receive_login_action(), "1")
