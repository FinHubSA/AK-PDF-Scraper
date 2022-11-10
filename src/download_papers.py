import requests
import time
import os
import urllib.parse
import emoji
import platform

from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool
from pathlib import Path
from urllib.parse import urlparse
from termcolor import colored
from helpers import *
import platform
import emoji

system = platform.system()

is_windows = False

if system == "Windows":
    is_windows = True

def download_papers():

    while True:
        download_criteria = get_download_criteria()

        system = platform.system()

        if system == "Windows":
            os.system("color")

        if download_criteria == "1":
            download_by_journal()
        elif download_criteria == "2":
            download_by_author()
        elif download_criteria == "3":
            os._exit(0)


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
            + "\n-- Type [3] to exit"
            + "\n   : ",
        )
    )

    return download_criteria

def download_by_author():
    global is_windows

    author = select_author()

    if "authorID" in author:
        author_name = author["authorName"]

        print(
            "\n"
            + (colored(" i ", "blue", attrs=["reverse"])) * (is_windows)
            + (emoji.emojize(":information:")) * (not is_windows)
            + (f" Downloading articles for {author_name}.\n")
        )

        get_articles(author_name=author_name)

def download_by_journal():
    global is_windows

    journal = select_journal()

    if not ("journalID" in journal):

        print(
            "\n"
            + (colored(" i ", "red", attrs=["reverse"])) * (is_windows)
            + (emoji.emojize(":information:")) * (not is_windows)
            + (f" Journal not found.\n")
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
        )

        if download_by_issue == "1" or download_by_issue == "2":
            break

    journal_name = journal["journalName"]
    journal_id = journal["journalID"]

    if download_by_issue == "1":
        
        print(
            "\n"
            + (colored(" i ", "blue", attrs=["reverse"])) * (is_windows)
            + (emoji.emojize(":information:")) * (not is_windows)
            + (f" Downloading articles for {journal_name}.\n")
        )

    else:
        issue = select_issue(journal_id)

        if not ("issueID" in issue):
            print(
                "\n"
                + (colored(" i ", "red", attrs=["reverse"])) * (is_windows)
                + (emoji.emojize(":information:")) * (not is_windows)
                + (f" Issue not found.\n")
            )

            return

        issue_id = issue["issueID"]

        get_articles(issue_id=issue_id)


def get_articles(journal_id = None, issue_id = None, author_name = None):
    global is_windows

    if (journal_id):
        articles = requests.get(
            f"https://api-service-mrz6aygprq-oa.a.run.app/api/articles?journalID={journal_id}&scraped=1"
        )
    elif issue_id:
        articles = requests.get(
            f"https://api-service-mrz6aygprq-oa.a.run.app/api/articles?issueID={issue_id}&scraped=1"
        )
    elif author_name:
        # print("author name", author_name)
        articles = requests.get(
            f"https://api-service-mrz6aygprq-oa.a.run.app/api/articles?authorName={author_name}&scraped=1"
        )
    
    articles = articles.json()

    articles_size = len(articles)

    if articles_size > 0:
        print(
            "\n"
            + (colored(" i ", "blue", attrs=["reverse"])) * (is_windows)
            + (emoji.emojize(":information:")) * (not is_windows)
            + (f" Downloading {articles_size} articles....\n")
        )

        bulk_download(articles)
    else:
        print(
            "\n"
            + (colored(" i ", "yellow", attrs=["reverse"])) * (is_windows)
            + (emoji.emojize(":loudspeaker:")) * (not is_windows)
            + colored(
                " No articles were found. Please contribute to the repository.\n",
                "yellow",
            )
        )

def bulk_download(articles):
    global is_windows

    cpus = cpu_count()

    results = ThreadPool(cpus - 1).imap_unordered(download_url, articles)

    results_size = 0

    for result in results:
        results_size += 1

    print(
        "\n"
        + (colored(" i ", "blue", attrs=["reverse"])) * (is_windows)
        + (emoji.emojize(":information:")) * (not is_windows)
        + (f" Successfully downloaded {results_size} articles.\n")
    )

def download_url(article):
    # print("article ", article["title"])

    path = os.path.join(str(Path.home() / "Downloads"), "AaronsKit_PDF_Downloads")
    if not os.path.exists(path):
        os.makedirs(path)

    bucket_url = article["bucketURL"]

    file_path = urlparse(bucket_url)
    download_url = path + "/" + os.path.basename(file_path.path)

    t0 = time.time()
    url, fn = bucket_url, download_url
    try:
        r = requests.get(url)
        with open(fn, "wb") as f:
            f.write(r.content)
        return (url, time.time() - t0)
    except Exception as e:
        print("Exception in download_url():", e)


