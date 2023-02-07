import time
import os
import emoji
import urllib.parse

from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool
from pathlib import Path
from urllib.parse import urlparse
from termcolor import colored

from src.helpers import system, typo, server_response_request
from src.download_criteria import select_journal, select_author, select_issue


def download_papers():

    while True:

        download_criteria = get_download_criteria()

        if download_criteria == "1":
            download_by_journal()
        elif download_criteria == "2":
            download_by_author()
        elif download_criteria == "3":
            break
        else:
            typo()


def get_download_criteria():

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

    return download_criteria


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
        + (f"   Downloading all articles by {author_name}...")
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
            + (f"   Downloading all articles from {journal_name}...")
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
            f"https://api-service-mrz6aygprq-oa.a.run.app/api/articles?authorName={author_name}&scraped=1"
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
            + (f"   Downloading {articles_size} articles...")
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
