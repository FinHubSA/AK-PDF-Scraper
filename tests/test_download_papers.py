import unittest
import os, sys
from unittest import mock
from unittest.mock import patch
from pathlib import Path

from src.download_papers import (
    bulk_download,
    download_url,
    get_articles,
    print_server_error,
    process_author_selection_action,
    process_continue_download_action,
    process_download_criteria_action,
    process_issue_selection_action,
    process_journal_download_criteria,
    process_journal_selection_action,
    receive_author_selection_action,
    receive_continue_download_action,
    receive_download_criteria_action,
    receive_issue_selection_action,
    receive_journal_download_criteria,
    receive_journal_selection_action,
    request_author,
    request_issue,
    request_journal,
)

from src.errors import MainException, TypoException
from src.temp_storage import delete_temp_storage


class TestDownloadPapers(unittest.TestCase):
    def setUp(self):

        self.input_1 = "1"
        self.input_2 = "2"
        self.input_3 = "3"
        self.input_4 = "$"

    # test process_continue_download_option
    def test_process_continue_download_option(self):

        os._exit = sys.exit

        with self.assertRaises(SystemExit):
            process_continue_download_action(self.input_1)

        with mock.patch(
            "src.download_papers.get_input",
            side_effect=[
                self.input_3,
            ],
        ):
            with self.assertRaises(MainException):
                process_continue_download_action(self.input_2)

        with self.assertRaises(MainException):
            process_continue_download_action(self.input_3)

        with self.assertRaises(TypoException):
            process_continue_download_action(self.input_4)

    # test receive_continue_download_option
    def test_receive_continue_download_option(self):

        with mock.patch(
            "src.download_papers.get_input",
            side_effect=[
                self.input_1,
            ],
        ):

            os._exit = sys.exit

            with self.assertRaises(SystemExit):
                receive_continue_download_action()

        with mock.patch(
            "src.download_papers.get_input",
            side_effect=[self.input_4, self.input_3],
        ):
            with self.assertRaises(MainException):
                receive_continue_download_action()

    # test print_server_error
    def test_print_server_error(self):

        os._exit = sys.exit

        with self.assertRaises(SystemExit):
            print_server_error()

    # test download_url
    def test_download_url(self):

        path = os.path.join(str(Path.home() / "Downloads"), "AaronsKit_PDF_Downloads")

        if os.path.exists(path):
            delete_temp_storage(path)

        os.makedirs(path)

        article = {
            "articleID": 22,
            "issue": 4,
            "articleJstorID": "10.2307/20716123",
            "title": "TO OUR READERS",
            "abstract": "",
            "bucketURL": "https://storage.googleapis.com/clean-aarons-kit-360209/10.2307-20716123-cnhapiwjqlgb.pdf",
            "authors": [
                {"authorID": 1, "authorName": "Ritamary Bradley"},
                {"authorID": 2, "authorName": "Valerie M. Lagorio"},
            ],
            "account": 1,
        }

        download_url(article)

        count_paper = len(
            [
                entry
                for entry in os.listdir(path)
                if os.path.isfile(os.path.join(path, entry))
            ]
        )

        self.assertEqual(count_paper, 1)

    # test bulk_downloads
    def test_bulk_downloads(self):

        path = os.path.join(str(Path.home() / "Downloads"), "AaronsKit_PDF_Downloads")

        if os.path.exists(path):
            delete_temp_storage(path)

        articles = [
            {
                "articleID": 22,
                "issue": 4,
                "articleJstorID": "10.2307/20716123",
                "title": "TO OUR READERS",
                "abstract": "",
                "bucketURL": "https://storage.googleapis.com/clean-aarons-kit-360209/10.2307-20716123-cnhapiwjqlgb.pdf",
                "authors": [
                    {"authorID": 1, "authorName": "Ritamary Bradley"},
                    {"authorID": 2, "authorName": "Valerie M. Lagorio"},
                ],
                "account": 1,
            },
            {
                "articleID": 23,
                "issue": 4,
                "articleJstorID": "10.2307/20716124",
                "title": "CORRESPONDENCE AND INTERVIEWS",
                "abstract": "",
                "bucketURL": "https://storage.googleapis.com/clean-aarons-kit-360209/10.2307-20716124-f387msyxqt0p.pdf",
                "authors": [],
                "account": 2,
            },
            {
                "articleID": 24,
                "issue": 4,
                "articleJstorID": "10.2307/20716125",
                "title": "PUBLICATIONS AND REVIEWS",
                "abstract": "",
                "bucketURL": "https://storage.googleapis.com/clean-aarons-kit-360209/10.2307-20716125-ykl513zqsb0m.pdf",
                "authors": [],
                "account": 2,
            },
            {
                "articleID": 25,
                "issue": 4,
                "articleJstorID": "10.2307/20716126",
                "title": "CAVEAT LECTOR",
                "abstract": "",
                "bucketURL": "https://storage.googleapis.com/clean-aarons-kit-360209/10.2307-20716126-xm69adkoqucp.pdf",
                "authors": [],
                "account": None,
            },
            {
                "articleID": 26,
                "issue": 4,
                "articleJstorID": "10.2307/20716127",
                "title": "nan",
                "abstract": "",
                "bucketURL": "https://storage.googleapis.com/clean-aarons-kit-360209/10.2307-20716127-n67wxmhj84e9.pdf",
                "authors": [{"authorID": 1, "authorName": "Ritamary Bradley"}],
                "account": None,
            },
            {
                "articleID": 27,
                "issue": 4,
                "articleJstorID": "10.2307/20716128",
                "title": "nan",
                "abstract": "",
                "bucketURL": "https://storage.googleapis.com/clean-aarons-kit-360209/10.2307-20716128-zdf2h7qone9g.pdf",
                "authors": [{"authorID": 18, "authorName": "Marion Glasscoe"}],
                "account": None,
            },
            {
                "articleID": 28,
                "issue": 4,
                "articleJstorID": "10.2307/20716129",
                "title": "AMONG RESEARCHERS",
                "abstract": "",
                "bucketURL": "https://storage.googleapis.com/clean-aarons-kit-360209/10.2307-20716129-rs3nxk17ft4z.pdf",
                "authors": [],
                "account": None,
            },
        ]

        with mock.patch(
            "src.download_papers.get_input",
            side_effect=[
                self.input_3,
            ],
        ):
            with self.assertRaises(MainException):
                bulk_download(articles)

            count_paper = len(
                [
                    entry
                    for entry in os.listdir(path)
                    if os.path.isfile(os.path.join(path, entry))
                ]
            )

            self.assertEqual(count_paper, 7)

    # test get_articles
    def test_get_articles(self):

        path = os.path.join(str(Path.home() / "Downloads"), "AaronsKit_PDF_Downloads")

        if os.path.exists(path):
            delete_temp_storage(path)

        # test issue
        with mock.patch(
            "src.download_papers.get_input",
            side_effect=[
                self.input_3,
            ],
        ):

            with self.assertRaises(MainException):
                get_articles(issue_id=16, journal_name="test Journal")

            count_paper = len(
                [
                    entry
                    for entry in os.listdir(path)
                    if os.path.isfile(os.path.join(path, entry))
                ]
            )

            self.assertEqual(count_paper, 11)

        # test author
        with mock.patch(
            "src.download_papers.get_input",
            side_effect=[
                self.input_3,
            ],
        ):

            with self.assertRaises(MainException):
                get_articles(author_name="Marc Uetz")

            count_paper = len(
                [
                    entry
                    for entry in os.listdir(path)
                    if os.path.isfile(os.path.join(path, entry))
                ]
            )

            self.assertEqual(count_paper, 12)

            # test journal
            with mock.patch(
                "src.download_papers.get_input",
                side_effect=[
                    self.input_3,
                ],
            ):
                with self.assertRaises(MainException):
                    get_articles(journal_id=1)

                count_paper = len(
                    [
                        entry
                        for entry in os.listdir(path)
                        if os.path.isfile(os.path.join(path, entry))
                    ]
                )

                self.assertEqual(count_paper, 62)

            # test no articles
            with mock.patch(
                "src.download_papers.get_input",
                side_effect=[
                    self.input_3,
                ],
            ):
                with self.assertRaises(MainException):
                    get_articles(author_name="Mary Gowin")

                count_paper = len(
                    [
                        entry
                        for entry in os.listdir(path)
                        if os.path.isfile(os.path.join(path, entry))
                    ]
                )

                self.assertEqual(count_paper, 62)

    # test process_issue_selection
    def test_process_issue_selection(self):

        issue_list_json = [
            {
                "issueID": 16,
                "journal": 1,
                "issueJstorID": "i20716455",
                "year": 1983,
                "volume": 9,
                "number": 4,
            },
            {
                "issueID": 6,
                "journal": 1,
                "issueJstorID": "i20716370",
                "year": 1982,
                "volume": 8,
                "number": 1,
            },
            {
                "issueID": 21,
                "journal": 1,
                "issueJstorID": "i20716379",
                "year": 1982,
                "volume": 8,
                "number": 2,
            },
            {
                "issueID": 20,
                "journal": 1,
                "issueJstorID": "i20716391",
                "year": 1982,
                "volume": 8,
                "number": 3,
            },
            {
                "issueID": 13,
                "journal": 1,
                "issueJstorID": "i20716400",
                "year": 1982,
                "volume": 8,
                "number": 4,
            },
            {
                "issueID": 11,
                "journal": 1,
                "issueJstorID": "i20716317",
                "year": 1981,
                "volume": 7,
                "number": 1,
            },
            {
                "issueID": 12,
                "journal": 1,
                "issueJstorID": "i20716361",
                "year": 1981,
                "volume": 7,
                "number": 4,
            },
            {
                "issueID": 5,
                "journal": 1,
                "issueJstorID": "i20716286",
                "year": 1980,
                "volume": 6,
                "number": 2,
            },
            {
                "issueID": 2,
                "journal": 1,
                "issueJstorID": "i20716296",
                "year": 1980,
                "volume": 6,
                "number": 3,
            },
            {
                "issueID": 3,
                "journal": 1,
                "issueJstorID": "i20716307",
                "year": 1980,
                "volume": 6,
                "number": 4,
            },
            {
                "issueID": 10,
                "journal": 1,
                "issueJstorID": "i20716240",
                "year": 1979,
                "volume": 5,
                "number": 2,
            },
            {
                "issueID": 14,
                "journal": 1,
                "issueJstorID": "i20716263",
                "year": 1979,
                "volume": 5,
                "number": 4,
            },
            {
                "issueID": 17,
                "journal": 1,
                "issueJstorID": "i20716186",
                "year": 1978,
                "volume": 4,
                "number": 1,
            },
            {
                "issueID": 8,
                "journal": 1,
                "issueJstorID": "i20716216",
                "year": 1978,
                "volume": 4,
                "number": 4,
            },
            {
                "issueID": 18,
                "journal": 1,
                "issueJstorID": "i20716152",
                "year": 1977,
                "volume": 3,
                "number": 1,
            },
            {
                "issueID": 7,
                "journal": 1,
                "issueJstorID": "i20716159",
                "year": 1977,
                "volume": 3,
                "number": 2,
            },
            {
                "issueID": 1,
                "journal": 1,
                "issueJstorID": "i20716140",
                "year": 1976,
                "volume": 2,
                "number": 3,
            },
            {
                "issueID": 15,
                "journal": 1,
                "issueJstorID": "i20716148",
                "year": 1976,
                "volume": 2,
                "number": 4,
            },
            {
                "issueID": 19,
                "journal": 1,
                "issueJstorID": "i20716109",
                "year": 1975,
                "volume": 1,
                "number": 2,
            },
            {
                "issueID": 9,
                "journal": 1,
                "issueJstorID": "i20716116",
                "year": 1975,
                "volume": 1,
                "number": 3,
            },
            {
                "issueID": 4,
                "journal": 1,
                "issueJstorID": "i20716122",
                "year": 1975,
                "volume": 1,
                "number": 4,
            },
        ]

        issue_list_number = 10

        test_issue = {
            "issueID": 16,
            "journal": 1,
            "issueJstorID": "i20716455",
            "year": 1983,
            "volume": 9,
            "number": 4,
        }

        self.assertEqual(
            process_issue_selection_action(
                self.input_1, issue_list_json, issue_list_number
            ),
            test_issue,
        )

        with self.assertRaises(TypoException):
            process_issue_selection_action(
                self.input_4, issue_list_json, issue_list_number
            )

    # test receive_issue_selection_action
    def test_receive_issue_selection_action(self):
        issue_list_json = [
            {
                "issueID": 16,
                "journal": 1,
                "issueJstorID": "i20716455",
                "year": 1983,
                "volume": 9,
                "number": 4,
            },
            {
                "issueID": 6,
                "journal": 1,
                "issueJstorID": "i20716370",
                "year": 1982,
                "volume": 8,
                "number": 1,
            },
            {
                "issueID": 21,
                "journal": 1,
                "issueJstorID": "i20716379",
                "year": 1982,
                "volume": 8,
                "number": 2,
            },
            {
                "issueID": 20,
                "journal": 1,
                "issueJstorID": "i20716391",
                "year": 1982,
                "volume": 8,
                "number": 3,
            },
            {
                "issueID": 13,
                "journal": 1,
                "issueJstorID": "i20716400",
                "year": 1982,
                "volume": 8,
                "number": 4,
            },
            {
                "issueID": 11,
                "journal": 1,
                "issueJstorID": "i20716317",
                "year": 1981,
                "volume": 7,
                "number": 1,
            },
            {
                "issueID": 12,
                "journal": 1,
                "issueJstorID": "i20716361",
                "year": 1981,
                "volume": 7,
                "number": 4,
            },
            {
                "issueID": 5,
                "journal": 1,
                "issueJstorID": "i20716286",
                "year": 1980,
                "volume": 6,
                "number": 2,
            },
            {
                "issueID": 2,
                "journal": 1,
                "issueJstorID": "i20716296",
                "year": 1980,
                "volume": 6,
                "number": 3,
            },
            {
                "issueID": 3,
                "journal": 1,
                "issueJstorID": "i20716307",
                "year": 1980,
                "volume": 6,
                "number": 4,
            },
            {
                "issueID": 10,
                "journal": 1,
                "issueJstorID": "i20716240",
                "year": 1979,
                "volume": 5,
                "number": 2,
            },
            {
                "issueID": 14,
                "journal": 1,
                "issueJstorID": "i20716263",
                "year": 1979,
                "volume": 5,
                "number": 4,
            },
            {
                "issueID": 17,
                "journal": 1,
                "issueJstorID": "i20716186",
                "year": 1978,
                "volume": 4,
                "number": 1,
            },
            {
                "issueID": 8,
                "journal": 1,
                "issueJstorID": "i20716216",
                "year": 1978,
                "volume": 4,
                "number": 4,
            },
            {
                "issueID": 18,
                "journal": 1,
                "issueJstorID": "i20716152",
                "year": 1977,
                "volume": 3,
                "number": 1,
            },
            {
                "issueID": 7,
                "journal": 1,
                "issueJstorID": "i20716159",
                "year": 1977,
                "volume": 3,
                "number": 2,
            },
            {
                "issueID": 1,
                "journal": 1,
                "issueJstorID": "i20716140",
                "year": 1976,
                "volume": 2,
                "number": 3,
            },
            {
                "issueID": 15,
                "journal": 1,
                "issueJstorID": "i20716148",
                "year": 1976,
                "volume": 2,
                "number": 4,
            },
            {
                "issueID": 19,
                "journal": 1,
                "issueJstorID": "i20716109",
                "year": 1975,
                "volume": 1,
                "number": 2,
            },
            {
                "issueID": 9,
                "journal": 1,
                "issueJstorID": "i20716116",
                "year": 1975,
                "volume": 1,
                "number": 3,
            },
            {
                "issueID": 4,
                "journal": 1,
                "issueJstorID": "i20716122",
                "year": 1975,
                "volume": 1,
                "number": 4,
            },
        ]

        test_issue = {
            "issueID": 16,
            "journal": 1,
            "issueJstorID": "i20716455",
            "year": 1983,
            "volume": 9,
            "number": 4,
        }

        with mock.patch("src.download_papers.get_input", side_effect=[self.input_1]):

            self.assertEqual(
                receive_issue_selection_action(issue_list_json), test_issue
            )

        # typo
        with mock.patch(
            "src.download_papers.get_input", side_effect=[self.input_4, self.input_1]
        ):

            self.assertEqual(
                receive_issue_selection_action(issue_list_json), test_issue
            )

    # test request_issue
    def test_request_issue(self):

        # has issues
        test_issue = {
            "issueID": 16,
            "journal": 1,
            "issueJstorID": "i20716455",
            "year": 1983,
            "volume": 9,
            "number": 4,
        }

        with mock.patch("src.download_papers.get_input", side_effect=[self.input_1]):
            self.assertEqual(request_issue("Test Name", 1), test_issue)

        # has no issues

        with mock.patch("src.download_papers.get_input", side_effect=[self.input_1]):
            self.assertEqual(request_issue("Test Name", 3714), {})

    # test process_journal_download_criteria
    def test_process_journal_download_criteria(self):

        path = os.path.join(str(Path.home() / "Downloads"), "AaronsKit_PDF_Downloads")

        if os.path.exists(path):
            delete_temp_storage(path)

        # test download journal
        with mock.patch(
            "src.download_papers.get_input",
            side_effect=[
                self.input_3,
            ],
        ):

            with self.assertRaises(MainException):
                process_journal_download_criteria(self.input_1, "test Journal", 1)

            count_paper = len(
                [
                    entry
                    for entry in os.listdir(path)
                    if os.path.isfile(os.path.join(path, entry))
                ]
            )

            self.assertEqual(count_paper, 50)

        # test download issue
        with mock.patch(
            "src.download_papers.get_input",
            side_effect=[self.input_1, self.input_3],
        ):

            with self.assertRaises(MainException):
                process_journal_download_criteria(self.input_2, "test Journal", 1)

            count_paper = len(
                [
                    entry
                    for entry in os.listdir(path)
                    if os.path.isfile(os.path.join(path, entry))
                ]
            )

            self.assertEqual(count_paper, 61)

        # test download issue but no issue
        with mock.patch(
            "src.download_papers.get_input",
            side_effect=[self.input_3],
        ):

            with self.assertRaises(MainException):
                process_journal_download_criteria(self.input_2, "test Journal", 3714)

            count_paper = len(
                [
                    entry
                    for entry in os.listdir(path)
                    if os.path.isfile(os.path.join(path, entry))
                ]
            )

            self.assertEqual(count_paper, 61)

    # test receive_journal_download_criteria
    def test_receive_journal_download_criteria(self):

        path = os.path.join(str(Path.home() / "Downloads"), "AaronsKit_PDF_Downloads")

        if os.path.exists(path):
            delete_temp_storage(path)

        with mock.patch(
            "src.download_papers.get_input", side_effect=[self.input_1, self.input_3]
        ):

            with self.assertRaises(MainException):
                receive_journal_download_criteria("test Journal", 1)

            count_paper = len(
                [
                    entry
                    for entry in os.listdir(path)
                    if os.path.isfile(os.path.join(path, entry))
                ]
            )

            self.assertEqual(count_paper, 50)

        # typo
        with mock.patch(
            "src.download_papers.get_input",
            side_effect=[self.input_4, self.input_1, self.input_3],
        ):

            with self.assertRaises(MainException):
                receive_journal_download_criteria("test Journal", 1)

            count_paper = len(
                [
                    entry
                    for entry in os.listdir(path)
                    if os.path.isfile(os.path.join(path, entry))
                ]
            )

            self.assertEqual(count_paper, 50)

    # test process_author_selection_action
    def test_process_author_selection_action(self):

        Author_list_json = [
            {"authorID": 37660, "authorName": "Marc Uetz"},
            {"authorID": 23257, "authorName": "Marc Lazar"},
            {"authorID": 33669, "authorName": "Marc Aymes"},
            {"authorID": 64280, "authorName": "Marc McLeod"},
            {"authorID": 30975, "authorName": "Marc BLOCH"},
            {"authorID": 74616, "authorName": "MARC NEVEU"},
            {"authorID": 70460, "authorName": "Marc Milner"},
            {"authorID": 28601, "authorName": "Marc Molgat"},
            {"authorID": 30914, "authorName": "Marc Sauzet"},
            {"authorID": 17551, "authorName": "Marc SAVARD"},
        ]

        author_list_number = 10

        test_author = {"authorID": 37660, "authorName": "Marc Uetz"}

        self.assertEqual(
            process_author_selection_action(
                self.input_1, Author_list_json, author_list_number
            ),
            test_author,
        )

        with self.assertRaises(TypoException):
            process_author_selection_action(
                self.input_4, Author_list_json, author_list_number
            )

    # test receive_author_selection_action
    def test_receive_author_selection_action(self):

        Author_list_json = [
            {"authorID": 37660, "authorName": "Marc Uetz"},
            {"authorID": 23257, "authorName": "Marc Lazar"},
            {"authorID": 33669, "authorName": "Marc Aymes"},
            {"authorID": 64280, "authorName": "Marc McLeod"},
            {"authorID": 30975, "authorName": "Marc BLOCH"},
            {"authorID": 74616, "authorName": "MARC NEVEU"},
            {"authorID": 70460, "authorName": "Marc Milner"},
            {"authorID": 28601, "authorName": "Marc Molgat"},
            {"authorID": 30914, "authorName": "Marc Sauzet"},
            {"authorID": 17551, "authorName": "Marc SAVARD"},
        ]

        test_author = {"authorID": 37660, "authorName": "Marc Uetz"}

        with mock.patch("src.download_papers.get_input", side_effect=[self.input_1]):

            self.assertEqual(
                receive_author_selection_action(Author_list_json), test_author
            )

        # typo
        with mock.patch(
            "src.download_papers.get_input", side_effect=[self.input_4, self.input_1]
        ):

            self.assertEqual(
                receive_author_selection_action(Author_list_json), test_author
            )

    # test request_author
    def test_request_author(self):

        test_author = {"authorID": 37660, "authorName": "Marc Uetz"}

        # can find author
        with mock.patch(
            "src.download_papers.get_input", side_effect=["Marc", self.input_1]
        ):

            self.assertEqual(request_author(), test_author)

        # cannot find author
        with mock.patch("src.download_papers.get_input", side_effect=["$"]):

            self.assertEqual(request_author(), {})

    # test process_journal_selection
    def test_process_journal_selection(self):

        Journal_list_json = [
            {
                "journalID": 2,
                "issn": "01482076",
                "altISSN": "15338606",
                "journalName": "19th-Century Music",
            },
            {
                "journalID": 4155,
                "issn": "10542043",
                "altISSN": "15314715",
                "journalName": "TDR (1988-)",
            },
            {
                "journalID": 3327,
                "issn": "00318906",
                "altISSN": "23257199",
                "journalName": "Phylon (1960-)",
            },
            {
                "journalID": 1379,
                "issn": "01847791",
                "altISSN": "24197157",
                "journalName": "Esprit (1932-1939)",
            },
            {
                "journalID": 929,
                "issn": "11476753",
                "altISSN": "22729828",
                "journalName": "Caravelle (1988-)",
            },
            {
                "journalID": 3326,
                "issn": "08856818",
                "altISSN": "23257210",
                "journalName": "Phylon (1940-1956)",
            },
            {
                "journalID": 1373,
                "issn": "01650106",
                "altISSN": "15728420",
                "journalName": "Erkenntnis (1975-)",
            },
            {
                "journalID": 3510,
                "issn": "00333549",
                "altISSN": "14682877",
                "journalName": "Public Health Reports (1974-)",
            },
            {
                "journalID": 3163,
                "issn": "03606724",
                "altISSN": "2577929X",
                "journalName": "Obsidian (1975-1982)",
            },
        ]

        journal_list_number = 1

        test_journal = {
            "journalID": 2,
            "issn": "01482076",
            "altISSN": "15338606",
            "journalName": "19th-Century Music",
        }

        self.assertEqual(
            process_journal_selection_action(
                self.input_1, Journal_list_json, journal_list_number
            ),
            test_journal,
        )

        with self.assertRaises(TypoException):
            process_journal_selection_action(
                self.input_4, Journal_list_json, journal_list_number
            )

    # test receive_journal_selection_action
    def test_receive_journal_selection_action(self):

        Journal_list_json = [
            {
                "journalID": 2,
                "issn": "01482076",
                "altISSN": "15338606",
                "journalName": "19th-Century Music",
            },
            {
                "journalID": 4155,
                "issn": "10542043",
                "altISSN": "15314715",
                "journalName": "TDR (1988-)",
            },
            {
                "journalID": 3327,
                "issn": "00318906",
                "altISSN": "23257199",
                "journalName": "Phylon (1960-)",
            },
            {
                "journalID": 1379,
                "issn": "01847791",
                "altISSN": "24197157",
                "journalName": "Esprit (1932-1939)",
            },
            {
                "journalID": 929,
                "issn": "11476753",
                "altISSN": "22729828",
                "journalName": "Caravelle (1988-)",
            },
            {
                "journalID": 3326,
                "issn": "08856818",
                "altISSN": "23257210",
                "journalName": "Phylon (1940-1956)",
            },
            {
                "journalID": 1373,
                "issn": "01650106",
                "altISSN": "15728420",
                "journalName": "Erkenntnis (1975-)",
            },
            {
                "journalID": 3510,
                "issn": "00333549",
                "altISSN": "14682877",
                "journalName": "Public Health Reports (1974-)",
            },
            {
                "journalID": 3163,
                "issn": "03606724",
                "altISSN": "2577929X",
                "journalName": "Obsidian (1975-1982)",
            },
        ]

        test_journal = {
            "journalID": 2,
            "issn": "01482076",
            "altISSN": "15338606",
            "journalName": "19th-Century Music",
        }

        with mock.patch("src.download_papers.get_input", side_effect=[self.input_1]):

            self.assertEqual(
                receive_journal_selection_action(Journal_list_json), test_journal
            )

        # typo
        with mock.patch(
            "src.download_papers.get_input", side_effect=[self.input_4, self.input_1]
        ):

            self.assertEqual(
                receive_journal_selection_action(Journal_list_json), test_journal
            )

    # test request_journal
    def test_request_journal(self):

        test_journal = {
            "journalID": 2,
            "issn": "01482076",
            "altISSN": "15338606",
            "journalName": "19th-Century Music",
        }

        # can find journal
        with mock.patch(
            "src.download_papers.get_input", side_effect=["19th", self.input_1]
        ):

            self.assertEqual(request_journal(), test_journal)

        # cannot find journal
        with mock.patch("src.download_papers.get_input", side_effect=["$"]):

            self.assertEqual(request_journal(), {})

    # test process_download_criteria_action
    # test input 1
    @patch(
        "src.download_papers.request_journal",
        return_value={
            "journalID": 2,
            "issn": "01482076",
            "altISSN": "15338606",
            "journalName": "19th-Century Music",
        },
    )
    def test_process_download_criteria_action_1(self, input):

        path = os.path.join(str(Path.home() / "Downloads"), "AaronsKit_PDF_Downloads")

        if os.path.exists(path):
            delete_temp_storage(path)

        with mock.patch(
            "src.download_papers.get_input", side_effect=[self.input_1, self.input_3]
        ):
            with self.assertRaises(MainException):
                process_download_criteria_action(self.input_1)

            count_paper = len(
                [
                    entry
                    for entry in os.listdir(path)
                    if os.path.isfile(os.path.join(path, entry))
                ]
            )

            self.assertEqual(count_paper, 50)

    # test process_download_criteria_action
    # test input 2
    @patch(
        "src.download_papers.request_author",
        return_value={"authorID": 37660, "authorName": "Marc Uetz"},
    )
    def test_process_download_criteria_action_2(self, input):

        path = os.path.join(str(Path.home() / "Downloads"), "AaronsKit_PDF_Downloads")

        if os.path.exists(path):
            delete_temp_storage(path)

        with mock.patch("src.download_papers.get_input", side_effect=[self.input_3]):
            with self.assertRaises(MainException):
                process_download_criteria_action(self.input_2)

            count_paper = len(
                [
                    entry
                    for entry in os.listdir(path)
                    if os.path.isfile(os.path.join(path, entry))
                ]
            )

            self.assertEqual(count_paper, 1)

    # test process_download_criteria_action
    # test input 3 and 4
    def test_process_download_criteria_action_3(self):

        with self.assertRaises(MainException):
            process_download_criteria_action(self.input_3)

        with self.assertRaises(TypoException):
            process_download_criteria_action(self.input_4)

    # test receive_download_criteria_action
    def test_receive_download_criteria_action(self):

        with mock.patch("src.download_papers.get_input", side_effect=[self.input_3]):

            with self.assertRaises(MainException):
                receive_download_criteria_action()

        with mock.patch(
            "src.download_papers.get_input", side_effect=[self.input_4, self.input_3]
        ):

            with self.assertRaises(MainException):
                receive_download_criteria_action()
