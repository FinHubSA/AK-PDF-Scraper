import time
import os
import emoji
import urllib.parse
import warnings
import logging

from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool
from pathlib import Path
from urllib.parse import urlparse
from termcolor import colored
from src.errors import MainException, TypoException

from src.helpers import system, print_typo, server_response_request

logging.getLogger().setLevel(logging.CRITICAL)
warnings.filterwarnings("ignore", category=UserWarning)

is_windows = system()


def receive_download_criteria_action():

    print(
        "\n"
        + emoji.emojize(":information:") * (not is_windows)
        + colored(" i ", "blue", attrs=["reverse"]) * (is_windows)
        + "   Please indicate your download criteria."
    )

    download_criteria = get_input(
        colored(
            "\n-- Type [1] to download by journal"
            + "\n-- Type [2] to download by author"
            + "\n-- Type [3] to return to main menu"
            + "\n   : ",
        )
    )

    try:
        process_download_criteria_action(download_criteria)
    except TypoException:
        receive_download_criteria_action()


def process_download_criteria_action(download_criteria):

    if download_criteria == "1":

        global journal_name, journal_id

        journal = request_journal_download()

        if not ("journalID" in journal):

            print(
                "\n\n"
                + colored(" ! ", "red", attrs=["reverse"]) * (is_windows)
                + emoji.emojize(":red_exclamation_mark:") * (not is_windows)
                + colored(
                    "   The requested journal could not be found.\n",
                    "red",
                )
            )

            receive_download_criteria_action()

        else:

            journal_name = journal["journalName"]
            journal_id = journal["journalID"]

            receive_journal_download_criteria(journal_name, journal_id)

    elif download_criteria == "2":

        author = request_author_download()

        if not ("authorID" in author):

            print(
                "\n\n"
                + (colored(" ! ", "red", attrs=["reverse"])) * (is_windows)
                + (emoji.emojize(":red_exclamation_mark:")) * (not is_windows)
                + colored(
                    "  The requested author could not be found.\n",
                    "red",
                )
            )

            receive_download_criteria_action()

        else:

            author_name = author["authorName"]

            get_articles(author_name=author_name)

    elif download_criteria == "3":
        raise MainException()
    else:
        print_typo()
        raise TypoException()


def request_journal_download():

    print(
        "\n"
        + (colored(" i ", "blue", attrs=["reverse"])) * (is_windows)
        + (emoji.emojize(":information:")) * (not is_windows)
        + "   You have chosen to search by Journal Name.\n"
    )

    print(
        colored(
            "\nPlease enter the Name of a Journal (EXAMPLE: Journal of Financial Education).\n",
            attrs=["bold"],
        )
    )

    Journal_Name = get_input(
        colored(
            "-- Type Journal Name\n   : ",
        )
    )

    server_error, Journal_List_json = server_response_request(
        f"https://api-service-mrz6aygprq-oa.a.run.app/api/journals?journalName={urllib.parse.quote(Journal_Name)}"
    )

    if server_error:
        print_server_error()

    try:
        Journal_List_json = Journal_List_json.json()
        return receive_journal_selection_action(Journal_List_json)
    except:
        return {}


def receive_journal_selection_action(Journal_List_json):

    print(
        colored(
            "\n\nPlease select a Journal from the list below:\n",
            attrs=["bold"],
        )
    )

    time.sleep(1)

    journal_list_number = 0

    for Journal_Name in Journal_List_json:

        journal_list_number += 1

        print("[" + str(journal_list_number) + "] " + Journal_Name["journalName"])

    Journal_Number = get_input(
        colored(
            "\n\n-- Type the Number of the Journal\n   : ",
        )
    )

    try:
        return process_journal_selection_action(
            Journal_Number, Journal_List_json, journal_list_number
        )
    except TypoException:
        return receive_journal_selection_action(Journal_List_json)


def process_journal_selection_action(
    Journal_Number, Journal_List_json, journal_list_number
):

    if Journal_Number in [str(x) for x in list(range(1, journal_list_number + 1))]:

        return Journal_List_json[int(Journal_Number) - 1]

    else:
        print_typo()
        raise TypoException


def request_author_download():

    print(
        "\n"
        + (colored(" i ", "blue", attrs=["reverse"])) * (is_windows)
        + (emoji.emojize(":information:")) * (not is_windows)
        + "   You have chosen to search by Author Name.\n"
    )

    print(
        colored(
            "\nPlease enter the Name and Surname of an Author (EXAMPLE: Rebecca Gould).",
            attrs=["bold"],
        )
    )

    Author_Name = get_input(
        colored(
            "\n-- Type Author Name and Surname\n   : ",
        )
    )

    server_error, Author_List_json = server_response_request(
        f"https://api-service-mrz6aygprq-oa.a.run.app/api/authors?authorName={urllib.parse.quote(Author_Name)}"
    )

    if server_error:
        print_server_error()

    try:

        Author_List_json = Author_List_json.json()
        return receive_author_selection_action(Author_List_json)

    except:

        return {}


def receive_author_selection_action(Author_List_json):

    print(
        colored(
            "\n\nPlease select an Author from the list below:\n",
            attrs=["bold"],
        )
    )

    time.sleep(1)

    author_list_number = 0

    for Author_Name in Author_List_json:

        author_list_number += 1

        print("[" + str(author_list_number) + "] " + Author_Name["authorName"])

    Author_Number = get_input(
        colored(
            "\n\n-- Type the Number of the Author\n   : ",
        )
    )

    try:
        return process_author_selection_action(
            Author_Number, Author_List_json, author_list_number
        )
    except TypoException:
        return receive_author_selection_action(Author_List_json)


def process_author_selection_action(
    Author_Number, Author_List_json, author_list_number
):

    if Author_Number in [str(x) for x in list(range(1, author_list_number + 1))]:

        return Author_List_json[int(Author_Number) - 1]

    else:
        print_typo()
        raise TypoException


def receive_journal_download_criteria(journal_name, journal_id):

    print(
        "\n"
        + emoji.emojize(":information:") * (not is_windows)
        + colored(" i ", "blue", attrs=["reverse"]) * (is_windows)
        + "   Please indicate your download criteria."
    )

    download_by_issue = get_input(
        colored(
            "\n-- Type [1] to download entire journal"
            + "\n-- Type [2] to download by journal issue"
            + "\n   : ",
        )
    )

    try:
        process_journal_download_criteria(download_by_issue, journal_name, journal_id)
    except TypoException:
        receive_journal_download_criteria(journal_name, journal_id)


def process_journal_download_criteria(download_by_issue, journal_name, journal_id):

    if download_by_issue == "1":

        get_articles(journal_id=journal_id, journal_name=journal_name)

    elif download_by_issue == "2":

        issue = request_issue(journal_name, journal_id)

        if not ("issueID" in issue):

            print(
                "\n"
                + (colored(" ! ", "yellow", attrs=["reverse"])) * (is_windows)
                + (emoji.emojize(":loudspeaker:")) * (not is_windows)
                + (
                    colored(
                        f"  This journal has no issues, we will download the entire journal instead.\n",
                        "yellow",
                    )
                )
            )

            get_articles(journal_id=journal_id, journal_name=journal_name)

        else:

            get_articles(issue_id=issue["issueID"], journal_name=journal_name)

    else:
        print_typo()
        raise TypoException


def request_issue(journal_name, journal_id):

    print("\n\nSearching for issues in " + journal_name + ".")

    server_error, issue_list_json = server_response_request(
        f"https://api-service-mrz6aygprq-oa.a.run.app/api/issues?journalID={journal_id}"
    )

    if server_error:
        print_server_error()

    try:
        issue_list_json = issue_list_json.json()
        return receive_issue_selection_action(issue_list_json)
    except:
        return {}


def receive_issue_selection_action(issue_list_json):

    print(
        colored(
            "\n\nPlease select an Issue from the list below:\n",
            attrs=["bold"],
        )
    )

    issue_list_number = 0

    for issue in issue_list_json:

        issue_list_number += 1

        print(
            "["
            + str(issue_list_number)
            + "] "
            + "Vol. "
            + str(issue["volume"])
            + ", "
            + "No. "
            + str(issue["number"])
            + ", "
            + "Year. "
            + str(issue["year"])
        )

    issue_number = get_input(
        colored(
            "\n\n-- Type the Number of the Issue\n   : ",
        )
    )

    try:
        return process_issue_selection_action(
            issue_number, issue_list_json, issue_list_number
        )
    except TypoException:
        return receive_issue_selection_action(issue_list_json)


def process_issue_selection_action(issue_number, issue_list_json, issue_list_number):

    if issue_number in [str(x) for x in list(range(1, issue_list_number + 1))]:

        return issue_list_json[int(issue_number) - 1]

    else:
        print_typo()
        raise TypoException


def get_articles(journal_id=None, issue_id=None, author_name=None, journal_name=None):

    if journal_id:
        server_error, articles = server_response_request(
            f"https://api-service-mrz6aygprq-oa.a.run.app/api/articles?journalID={journal_id}&scraped=1"
        )
    elif issue_id:
        server_error, articles = server_response_request(
            f"https://api-service-mrz6aygprq-oa.a.run.app/api/articles?issueID={issue_id}&scraped=1"
        )

    elif author_name:
        server_error, articles = server_response_request(
            f"https://api-service-mrz6aygprq-oa.a.run.app/api/articles?authorName={author_name}&scraped=1&exact=1"
        )

    if server_error:
        print_server_error()

    articles = articles.json()

    articles_size = len(articles)

    if articles_size > 0:

        if issue_id or journal_id:
            print(
                "\n"
                + (colored(" i ", "blue", attrs=["reverse"])) * (is_windows)
                + (emoji.emojize(":information:")) * (not is_windows)
                + (f"   Downloading {articles_size} articles from {journal_name}.")
            )

        elif author_name:
            print(
                "\n"
                + (colored(" i ", "blue", attrs=["reverse"])) * (is_windows)
                + (emoji.emojize(":information:")) * (not is_windows)
                + (f"   Downloading {articles_size} articles by {author_name}.")
            )

        bulk_download(articles)

    else:

        print(
            "\n"
            + (colored(" ! ", "yellow", attrs=["reverse"])) * (is_windows)
            + (emoji.emojize(":loudspeaker:")) * (not is_windows)
            + colored(
                "   Unfortunately we currently have no articles for this search criteria.\n",
                "yellow",
            )
        )

        receive_continue_download_action()


def bulk_download(articles):

    path = os.path.join(str(Path.home() / "Downloads"), "AaronsKit_PDF_Downloads")

    if not os.path.exists(path):
        os.makedirs(path)

    cpus = cpu_count()

    results = ThreadPool(cpus - 1).imap_unordered(download_url, articles)

    if not results == None:

        results_size = 0

        for result in results:
            results_size += 1

        print(
            "\n"
            + (colored(" ! ", "green", attrs=["reverse"])) * (is_windows)
            + (emoji.emojize(":check_mark_button:")) * (not is_windows)
            + colored(
                f"   Successfully downloaded {results_size} articles! Navigate to ",
                "green",
            )
            + colored("AaronsKit_PDF_Downloads", "green", attrs=["reverse"])
            * (is_windows)
            + colored("AaronsKit_PDF_Downloads", "green", attrs=["bold"])
            * (not is_windows)
            + colored(" in your downloads folder to view your files.\n", "green")
        )

    receive_continue_download_action()


def download_url(article):

    path = os.path.join(str(Path.home() / "Downloads"), "AaronsKit_PDF_Downloads")

    bucket_url = article["bucketURL"]

    file_path = urlparse(bucket_url)
    download_url = path + "/" + os.path.basename(file_path.path)

    t0 = time.time()
    url, fn = bucket_url, download_url
    server_error, r = server_response_request(url)

    if server_error:
        print_server_error()

    try:
        with open(fn, "wb") as f:
            f.write(r.content)
        return (url, time.time() - t0)
    except Exception as e:

        print(
            "\n"
            + (colored(" i ", "red", attrs=["reverse"])) * (is_windows)
            + (emoji.emojize(":red_exclamation_mark:")) * (not is_windows)
            + colored(
                f"  An error occured: {e}",
                "red",
            )
        )

        return


def print_server_error():

    print(
        "\n"
        + (colored(" i ", "red", attrs=["reverse"])) * (is_windows)
        + (emoji.emojize(":red_exclamation_mark:")) * (not is_windows)
        + colored(f"  A server error occured, try again later.", "red")
    )

    os._exit(0)


def receive_continue_download_action():

    download_more_option = get_input(
        colored(
            "\n-- Type [1] to return to downloads menu\n-- Type [2] to return to main menu\n-- Type [3] to exit\n   : "
        )
    )

    try:
        process_continue_download_action(download_more_option)
    except TypoException:
        receive_continue_download_action()


def process_continue_download_action(download_more_option):

    if download_more_option == "1":
        receive_download_criteria_action()
    elif download_more_option == "2":
        raise MainException
    elif download_more_option == "3":
        os._exit(0)
    else:
        print_typo()
        raise TypoException


def get_input(text):
    return input(text).strip()
