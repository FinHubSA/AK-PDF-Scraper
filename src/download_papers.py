import time
import os
import emoji
import urllib.parse

from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool
from pathlib import Path
from urllib.parse import urlparse
from termcolor import colored
from src.errors import MainException, TypoException

from src.helpers import system, typo, server_response_request


def get_download_criteria_action():

    print(
        "\n"
        + emoji.emojize(":information:")
        + "   Please indicate your download criteria"
    )

    download_criteria = input(
        colored(
            "\n-- Type [1] to download by journal"
            + "\n-- Type [2] to download by author"
            + "\n-- Type [3] to return to main menu"
            + "\n   : ",
        )
    ).strip()

    try:
        process_download_criteria_action(download_criteria)
    except TypoException:
        get_download_criteria_action()

    return download_criteria


def process_download_criteria_action(download_criteria):

    if download_criteria == "1":
        download_by_journal()
    elif download_criteria == "2":
        download_by_author()
    elif download_criteria == "3":
        raise MainException()
    else:
        typo()
        raise TypoException()


def download_by_author():

    is_windows = system()

    author = select_author()

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

        return {}

    author_name = author["authorName"]

    print(
        "\n"
        + (colored(" i ", "blue", attrs=["reverse"])) * (is_windows)
        + (emoji.emojize(":information:")) * (not is_windows)
        + (f"   Downloading all articles by {author_name}.")
    )

    author_name_urlenc = urllib.parse.quote(author_name)

    get_articles(author_name=author_name_urlenc)


def download_by_journal():

    is_windows = system()

    journal = select_journal()

    if not ("journalID" in journal):

        print(
            "\n\n"
            + colored(" ! ", "red", attrs=["reverse"]) * (is_windows)
            + emoji.emojize(":red_exclamation_mark:") * (not is_windows)
            + colored(
                "  The requested journal could not be found.\n",
                "red",
            )
        )

        return

    while True:

        print(
            "\n"
            + emoji.emojize(":information:")
            + "   Please indicate your download criteria"
        )

        download_by_issue = input(
            colored(
                "\n-- Type [1] to download entire journal"
                + "\n-- Type [2] to download by journal issue"
                + "\n   : ",
            )
        ).strip()

        if download_by_issue == "1" or download_by_issue == "2":
            break

        typo()

    journal_name = journal["journalName"]
    journal_id = journal["journalID"]

    if download_by_issue == "1":

        print(
            "\n"
            + (colored(" i ", "blue", attrs=["reverse"])) * (is_windows)
            + (emoji.emojize(":information:")) * (not is_windows)
            + (f"   Downloading all articles from {journal_name}.")
        )

        get_articles(journal_id=journal_id)

    elif download_by_issue == "2":

        issue = select_issue(journal_name, journal_id)

        if not ("issueID" in issue):
            print(
                "\n"
                + (colored(" ! ", "yellow", attrs=["reverse"])) * (is_windows)
                + (emoji.emojize(":loudspeaker:")) * (not is_windows)
                + (
                    colored(
                        f"   This journal does not have any issues, we will download the entire journal instead.\n",
                        "yellow",
                    )
                )
            )

            get_articles(journal_id=journal_id)

        else:

            issue_id = issue["issueID"]

            get_articles(issue_id=issue_id)


def select_author():

    is_windows = system()

    print(
        "\n"
        + (colored(" i ", attrs=["reverse"])) * (is_windows)
        + (emoji.emojize(":information:")) * (not is_windows)
        + "   You have chosen to search by Author Name.\n"
    )

    print(
        "\n"
        + colored(
            "Please enter the Name and Surname of an Author (EXAMPLE: Rebecca Gould).",
            "blue",
        )
        * (is_windows)
        + colored(
            "Please enter the Name and Surname of an Author (EXAMPLE: Rebecca Gould).",
            attrs=["bold"],
        )
        * (not is_windows)
    )

    author_search = True

    while author_search == True:

        Author_Name = input(
            colored(
                "\n-- Type Author Name and Surname\n   : ",
            )
        ).strip()

        Author_Name_urlenc = urllib.parse.quote(Author_Name)

        server_error, Author_List_json = server_response_request(
            f"https://api-service-mrz6aygprq-oa.a.run.app/api/authors?authorName={Author_Name_urlenc}"
        )

        if server_error:
            os._exit(0)

        try:

            Author_List_json = Author_List_json.json()

        except:

            return {}

        print(
            "\n\n"
            + (
                colored(
                    "Please select an Author from the list below:\n",
                    "blue",
                )
            )
            * (is_windows)
            + (
                colored(
                    "Please select an Author from the list below:\n",
                    attrs=["bold"],
                )
            )
            * (not is_windows)
        )

        time.sleep(1)

        author_list_number = 0

        for Author_Name in Author_List_json:

            author_list_number += 1

            print("[" + str(author_list_number) + "] " + Author_Name["authorName"])

        Author_Number_typo = True

        while Author_Number_typo == True:

            Author_Number = input(
                colored(
                    "\n\n-- Type the Number of the Author\n   : ",
                )
            ).strip()

            if Author_Number not in [
                str(x) for x in list(range(1, author_list_number + 1))
            ]:

                print(
                    "\n\n"
                    + (colored(" ! ", "yellow", attrs=["reverse"])) * (is_windows)
                    + (emoji.emojize(":loudspeaker:")) * (not is_windows)
                    + colored(
                        "  It appears that you made a typo, please re-enter your selection.",
                        "yellow",
                    )
                )

            else:
                Author_Number_typo = False

        return Author_List_json[int(Author_Number) - 1]


def select_journal():

    is_windows = system()

    print(
        "\n"
        + (colored(" i ", attrs=["reverse"])) * (is_windows)
        + (emoji.emojize(":information:")) * (not is_windows)
        + "   You have chosen to search by Journal Name.\n"
    )

    print(
        "\n"
        + (
            colored(
                "Please enter the Name of a Journal (EXAMPLE: Journal of Financial Education).\n",
                "blue",
            )
        )
        * (is_windows)
        + (
            colored(
                "Please enter the Name of a Journal (EXAMPLE: Journal of Financial Education).\n",
                attrs=["bold"],
            )
        )
        * (not is_windows)
    )

    Journal_Name = input(
        colored(
            "-- Type Journal Name\n   : ",
        )
    ).strip()

    Journal_Name_urlenc = urllib.parse.quote(Journal_Name)

    server_error, Journal_List_json = server_response_request(
        f"https://api-service-mrz6aygprq-oa.a.run.app/api/journals?journalName={Journal_Name_urlenc}"
    )

    if server_error:
        os._exit(0)

    try:

        Journal_List_json = Journal_List_json.json()

    except:

        return {}

    print(
        "\n\n"
        + (
            colored(
                "Please select a Journal from the list below:\n",
                "blue",
            )
        )
        * (is_windows)
        + (
            colored(
                "Please select a Journal from the list below:\n",
                attrs=["bold"],
            )
        )
        * (not is_windows)
    )

    time.sleep(1)

    journal_list_number = 0

    for Journal_Name in Journal_List_json:

        journal_list_number += 1

        print("[" + str(journal_list_number) + "] " + Journal_Name["journalName"])

    Journal_Number_typo = True

    while Journal_Number_typo == True:

        Journal_Number = input(
            colored(
                "\n\n-- Type the Number of the Journal\n   : ",
            )
        ).strip()

        if Journal_Number not in [
            str(x) for x in list(range(1, journal_list_number + 1))
        ]:

            print(
                "\n\n"
                + (colored(" ! ", "yellow", attrs=["reverse"])) * (is_windows)
                + (emoji.emojize(":loudspeaker:")) * (not is_windows)
                + colored(
                    "  It appears that you made a typo, please re-enter your selection.",
                    "yellow",
                )
            )

        else:

            Journal_Number_typo = False

    return Journal_List_json[int(Journal_Number) - 1]


def select_issue(journal_name, journal_id):

    is_windows = system()

    print("\n\nSearching for issues in " + journal_name + ".")

    server_error, issue_list_json = server_response_request(
        f"https://api-service-mrz6aygprq-oa.a.run.app/api/issues?journalID={journal_id}"
    )

    if server_error:
        os._exit(0)

    try:

        issue_list_json = issue_list_json.json()

    except:

        return {}

    print(
        "\n\n"
        + (
            colored(
                "Please select an Issue from the list below:\n",
                "blue",
            )
        )
        * (is_windows)
        + (
            colored(
                "Please select an Issue from the list below:\n",
                attrs=["bold"],
            )
        )
        * (not is_windows)
    )

    time.sleep(1)

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

    issue_number_typo = True

    while issue_number_typo == True:

        issue_number = input(
            colored(
                "\n\n-- Type the Number of the Issue\n   : ",
            )
        ).strip()

        if issue_number not in [str(x) for x in list(range(1, issue_list_number + 1))]:

            print(
                "\n\n"
                + (colored(" ! ", "yellow", attrs=["reverse"])) * (is_windows)
                + (emoji.emojize(":loudspeaker:")) * (not is_windows)
                + colored(
                    "  It appears that you made a typo, please re-enter your selection.",
                    "yellow",
                )
            )

        else:

            issue_number_typo = False

    return issue_list_json[int(issue_number) - 1]


def get_articles(journal_id=None, issue_id=None, author_name=None):

    is_windows = system()

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
        os._exit(0)

    articles = articles.json()

    articles_size = len(articles)

    if articles_size > 0:
        print(
            "\n"
            + (colored(" i ", "blue", attrs=["reverse"])) * (is_windows)
            + (emoji.emojize(":information:")) * (not is_windows)
            + (f"   Downloading {articles_size} articles.")
        )

        bulk_download(articles)

    else:

        print(
            "\n"
            + (colored(" i ", "yellow", attrs=["reverse"])) * (is_windows)
            + (emoji.emojize(":loudspeaker:")) * (not is_windows)
            + colored(
                "   Unfortunately we currently have no articles for this search criteria.\n",
                "yellow",
            )
        )


def bulk_download(articles):

    is_windows = system()

    path = os.path.join(str(Path.home() / "Downloads"), "AaronsKit_PDF_Downloads")

    if not os.path.exists(path):
        os.makedirs(path)

    cpus = cpu_count()

    results = ThreadPool(cpus - 1).imap_unordered(download_url, articles)

    results_size = 0

    for result in results:
        results_size += 1

    print(
        "\n"
        + (colored(" ! ", "green", attrs=["reverse"])) * (is_windows)
        + (emoji.emojize(":check_mark_button:")) * (not is_windows)
        + colored(
            f"  Successfully downloaded {results_size} articles! Navigate to ", "green"
        )
        + colored("AaronsKit_PDF_Downloads", "green", attrs=["reverse"]) * (is_windows)
        + colored("AaronsKit_PDF_Downloads", "green", attrs=["bold"]) * (not is_windows)
        + colored(" in your downloads folder to view your files.\n", "green")
    )

    input(
        colored("\n\n-- Press ")
        + colored("ENTER/RETURN", attrs=["reverse"]) * (is_windows)
        + colored("ENTER/RETURN", attrs=["bold"]) * (not is_windows)
        + colored(" to go back to the downloads menu:")
    )


def download_url(article):

    path = os.path.join(str(Path.home() / "Downloads"), "AaronsKit_PDF_Downloads")

    bucket_url = article["bucketURL"]

    file_path = urlparse(bucket_url)
    download_url = path + "/" + os.path.basename(file_path.path)

    t0 = time.time()
    url, fn = bucket_url, download_url
    server_error, r = server_response_request(url)

    try:
        with open(fn, "wb") as f:
            f.write(r.content)
        return (url, time.time() - t0)
    except Exception as e:
        # what should the user do when exception occurs?
        print("Exception in download_url():", e)

    if server_error:
        os._exit(0)
