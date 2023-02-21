import unittest
import re
import os

from src.user_agent import get_user_agent_fixed, get_user_agent


class TestUserAgent(unittest.TestCase):

    # test get_user_agent
    # test with internet connection
    def test_get_user_agent_1(self):

        self.assertEqual(
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
            get_user_agent(30),
        )

    # test without internet connection
    def test_get_user_agent_2(self):

        os.system("networksetup -setairportpower airport off")

        user_agent = get_user_agent(30)

        self.assertIsNotNone(
            re.search(
                "^Mozilla/5.0.*Safari/537.36$",
                user_agent,
            )
        )

        os.system("networksetup -setairportpower airport on")

    # test get_user_agent_fixed
    def test_get_user_agent_fixed(self):

        user_agent = get_user_agent_fixed()

        self.assertIsNotNone(
            re.search(
                "^Mozilla/5.0.*Safari/537.36$",
                user_agent,
            )
        )


if __name__ == "__main__":
    unittest.main()
