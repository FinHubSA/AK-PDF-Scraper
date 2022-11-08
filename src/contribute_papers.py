import pickle
import time
import os.path
from datetime import datetime
import logging
import platform
import emoji
import os
import requests
import string
import random
import warnings
import traceback

import urllib.parse
from termcolor import colored
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

from recaptcha_solver import recaptcha_solver
from user_agent import user_agent
from temp_storage import (
    get_temp_storage_path,
    rename_file,
    delete_files,
    delete_temp_storage,
)

from internet_speed import download_speed, delay, internet_speed_retry
from download_papers import download_papers
from user_login import *

warnings.filterwarnings("ignore")
logging.getLogger().setLevel(logging.CRITICAL)

system = jstor_url = now = USER_AGENT = wait = driver = storage_directory = Article_ID_list = src_directory = misc_directory = None

restart_count = article_index = t_c_try_accept = mbps = index = 0

restart = t_c_accepted = False

def contribute_papers():

    global driver, mbps, driver, system, index, restart_count, article_index

    setup()

    # login
    logged_in = False
    while (not logged_in):
        logged_in = login(driver, system)
    
    while True:
        try:
            get_article_ids()
            download_articles()
        except Exception as e:
            
            # traceback.print_exc()

            print_error(e)

            internet_speed_retry(system)

            wait = delay(mbps)

            restart_count += 1

            time.sleep(wait * 10)


def print_error(e):
    # print(e)

    # Error occured, try to check internet and try again.
    if system == "Windows":

        print(
            "\n"
            + colored(" ! ", "yellow", attrs=["reverse"])
            + colored(
                "   Something went wrong, you might have an unstable internet connection",
                "yellow",
            )
        )

        input(
            colored("\n\n-- Please check your connection and then press ")
            + colored("ENTER/RETURN", attrs=["reverse"])
            + colored(" to continue: ")
        )

    else:

        print(
            "\n"
            + emoji.emojize(":loudspeaker:")
            + colored(
                "   Something went wrong, you might have an unstable internet connection",
                "yellow",
            )
        )

        input(
            colored("\n\n-- Please check your connection and then press ")
            + colored("ENTER/RETURN", attrs=["bold"])
            + colored(" to continue: ")
        )

def setup():
    
    global system, now, USER_AGENT, wait, driver, storage_directory, src_directory, misc_directory, mbps
    
    storage_directory = get_temp_storage_path()

    src_directory = os.path.dirname(__file__)

    misc_directory = os.path.normpath(src_directory + os.sep + os.pardir)

    system = platform.system()

    if system == "Windows":
        os.system("color")

    # set the file source directory
    os.chdir(src_directory)

    # calculate the internet speed and driver sleep time
    mbps = internet_speed_retry(system)

    wait = delay(mbps)
    # wait = 10

    # define the User Agent
    print("\n\ndetermining User Agent...")

    USER_AGENT = user_agent(system)
    # USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36"

    # define loop to facilitate restart when an error occurs
    now = datetime.now().timestamp()

    driver = create_driver_session(
        options(get_login_method, USER_AGENT, storage_directory)
    )

def create_driver_session(chrome_options):

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options,
    )

    driver.minimize_window()

    return driver

def options(login_method, USER_AGENT, storage_directory):
    chrome_options = webdriver.ChromeOptions()

    if login_method == "1":
        chrome_options.headless = True
    chrome_options.add_argument(f"user-agent={USER_AGENT}")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option(
        "prefs",
        {
            "download.default_directory": storage_directory,  # Change default directory for downloads
            "download.prompt_for_download": False,  # To auto download the file
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True,  # It will not show PDF directly in chrome
            "credentials_enable_service": False,  # Gets rid of password saver popup
            "profile.password_manager_enabled": False,  # Gets rid of password saver popup
        },
    )
    return chrome_options

def restart_driver_session(jstor_url, chrome_options, executor_url, session_id):

    driver = webdriver.Remote(command_executor=executor_url, options=chrome_options)

    driver.close()

    driver.session_id = session_id

    driver.get(jstor_url)


def latest_downloaded_pdf(storage_directory, src_directory):

    os.chdir(storage_directory)

    pdf_download_list = sorted(os.listdir(storage_directory), key=os.path.getmtime)

    latest_pdf = pdf_download_list[-1]

    os.chdir(src_directory)

    return latest_pdf

def download_articles():

    global restart, t_c_accepted, t_c_try_accept, article_index, Article_ID_list, now, wait, src_directory, storage_directory, restart_count

    # loop through user requested article ID's
    # if error occurs, restart the web session and start at last indexed ID - TEST
    for index, article_json in enumerate(Article_ID_list):

        article = article_json["articleJstorID"]

        # calculate the waiting time every 30 mins to adjust wait according to user internet speed
        if datetime.now().timestamp() >= now + 1200:

            mbps = download_speed()

            try:

                wait = delay(mbps)

            except:

                wait = 15

            now = datetime.now().timestamp()

        url = os.path.join(storage_directory, article.split("/")[-1] + ".pdf")

        url_pending = os.path.join(
            storage_directory, article.split("/")[-1] + ".pdf.crdownload"
        )

        random_string = string.ascii_lowercase + string.digits

        doi = os.path.join(
            storage_directory,
            article.split("/")[0]
            + "-"
            + article.split("/")[-1]
            + "-"
            + "".join(random.sample(random_string, 12))
            + ".pdf",
        )

        # check if pdf file already exists in user directory - TEST
        # delete if download pending or file exist to circumvent malicious actors
        if os.path.exists(url):

            os.remove(url)

        elif os.path.exists(url_pending):

            os.remove(url_pending)

        driver.get(jstor_url + "stable/pdf/" + article + ".pdf")

        start_time = datetime.now().timestamp()

        # check for cookies, t&c's and reCAPTCHA
        # the t&c's only appear when the browser session restarts
        while not t_c_accepted and t_c_try_accept <= 3:

            t_c_try_accept += 1

            # accept cookies
            try:

                WebDriverWait(driver, wait).until(
                    expected_conditions.element_to_be_clickable(
                        (By.XPATH, r"//button[@id='onetrust-accept-btn-handler']")
                    )
                ).click()

                print("cookies accepted")

            except:

                print("no cookies")

            # accept t&c's
            try:

                WebDriverWait(driver, wait).until(
                    expected_conditions.element_to_be_clickable(
                        (
                            By.XPATH,
                            r".//terms-and-conditions-pharos-button[@data-qa='accept-terms-and-conditions-button']",
                        )
                    )
                ).click()

                print("t&c's accepted")

                start_time = datetime.now().timestamp()

                t_c_accepted = True

            # check for reCAPTCHA
            except:

                if not (os.path.exists(url) or os.path.exists(url_pending)):

                    success, start_time = recaptcha_solver(
                        driver, url, url_pending, wait, src_directory, jstor_url
                    )

                    if success:

                        print("solved")

                        continue

                    else:

                        print(
                            "[ERR] reCAPTCHA could not be solved, restarting driver session"
                        )

                        restart = True

                        break

                else:

                    print("no t&c's")

                    t_c_accepted = True

        if restart:

            restart_count += 1

            break

        time.sleep(wait)

        # check for reCAPTCHA
        if not (os.path.exists(url) or os.path.exists(url_pending)):

            success, start_time = recaptcha_solver(
                driver, url, url_pending, wait, misc_directory, jstor_url
            )

            if not success:

                print(
                    "[ERR] reCAPTCHA could not be solved or pdf could not be downloaded, restarting driver session"
                )

                restart = True

                restart_count = +1

                break

        # check if download is complete
        file = url_pending

        count = 0

        while file == url_pending and count <= 120:

            time.sleep(1)

            count += 1

            latest_file = latest_downloaded_pdf(storage_directory, src_directory)

            if latest_file == article.split("/")[-1] + ".pdf":

                file = url

            else:

                file = url_pending

        end_time = datetime.now().timestamp()

        # rename the pdf
        try:

            rename_file(url, doi)

        except Exception as e:

            print(e)

            print("[ERR] Could not download pdf file, restarting driver session")

            restart_count = +1

            restart = True

            break

        # Navigate to home page
        driver.get(jstor_url)

        # append log file
        with open(os.path.join(misc_directory, "scraperlog.txt"), "a+") as log:
            log.write("\n")
            log.write("\nfor ID: " + article)
            log.write("\nwith size (in bytes): " + str(os.path.getsize(doi)))
            log.write(
                "\nscraper started at: " + str(datetime.fromtimestamp(start_time))
            )
            log.write(
                "\nscraper ended at: " + str(datetime.fromtimestamp(end_time))
            )
            log.write(
                "\ndownload time (in seconds): " + str(end_time - start_time - wait)
            )

        # upload pdf file to Google Drive
        files = {"file": open(doi, "rb")}
        data = {"articleJstorID": article}

        retry_upload_count = 0

        response = requests.post(
            "https://api-service-mrz6aygprq-oa.a.run.app/api/articles/pdf",
            files=files,
            data=data,
            verify=False,
        )

        if response.status_code == 200:

            print(
                "\nSucessfully uploaded article: "
                + article_json["title"]
                + "."
                + "\nIt will be available at "
                + response.json()["bucket_url"]
                + " in a few moments."
            )

        elif response.status_code == 404:

            print(
                "\nCould not find article: "
                + article_json["title"]
                + " in database."
            )

        elif response.status_code == 500:

            print(
                "\nCould not upload article: "
                + article_json["title"]
                + ", server error."
            )

        # delete article from local storage
        delete_files(doi)

        if article_json == Article_ID_list[-1]:
            delete_temp_storage(storage_directory)

            if system == "Windows":

                print(
                    "\n"
                    + colored(" ! ", "green", attrs=["reverse"])
                    + colored(
                        "   You have successfully uploaded your requested papers.",
                        "green",
                    )
                )

                print(
                    "\n"
                    + colored(" ! ", "green", attrs=["reverse"])
                    + colored(
                        "   You can exit/close this window." "green",
                    )
                )

            else:

                print(
                    "\n"
                    + emoji.emojize(":check_mark_button:")
                    + colored(
                        "   You have successfully uploaded your requested papers.",
                        "green",
                    )
                )

                print(
                    "\n"
                    + emoji.emojize(":check_mark_button:")
                    + colored(
                        "   You can exit/close this window.",
                        "green",
                    )
                )

            break

    # stop when all articles have downloaded, otherwise navigate to home page and restart web session
    if article_json == Article_ID_list[-1] and not restart:
        driver.close()
        os._exit(0)
    else:
        driver.get(jstor_url)

    article_index = index
    time.sleep(wait * 10)

def get_article_ids():

    global Article_ID_list, jstor_url

    if restart_count == 0:

        # Save the cookies to ensure reCAPTCHA can be solved
        # since login details are required to access the mp3 file
        pickle.dump(
            driver.get_cookies(),
            open(os.path.join(misc_directory, "cookies.pkl"), "wb"),
        )

        cookies = pickle.load(
            open(os.path.join(misc_directory, "cookies.pkl"), "rb")
        )

        for cookie in cookies:
            driver.add_cookie(cookie)

        # Save the url after user login as each url
        # will be unique to the user's institution
        jstor_url = driver.current_url

        # User select which papers they would like to download (API Call)
        if system == "Windows":

            print(
                "\n\n"
                + colored("JSTOR PDF download specification:\n", attrs=["reverse"])
            )

            print(
                "\n"
                + colored(" i ", attrs=["reverse"])
                + "   Please select your search criteria"
            )

            search_criteria_typo = True

            while search_criteria_typo == True:

                search_criteria = input(
                    colored(
                        "\n-- Type [1] to search by Author Name\n-- Type [2] to search by Journal Name\n   : ",
                    )
                )

                if search_criteria == "1":

                    print(
                        "\n"
                        + colored(" i ", attrs=["reverse"])
                        + "   You have chosen to search by Author Name.\n"
                    )

                    print(
                        "\n"
                        + colored(
                            "Please enter the Name and Surname of an Author (EXAMPLE: Rebecca Gould).\n",
                            "blue",
                        )
                    )

                    author_search = True

                    while author_search == True:

                        Author_Name = input(
                            colored(
                                "\n-- Type Author Name and Surname\n   : ",
                            )
                        )

                        Author_Name_urlenc = urllib.parse.quote(Author_Name)

                        Author_List_json = requests.get(
                            f"https://api-service-mrz6aygprq-oa.a.run.app/api/authors?authorName={Author_Name_urlenc}"
                        )

                        try:

                            Author_List_json = Author_List_json.json()

                        except:

                            print(
                                "\n\n"
                                + colored(" ! ", "yellow", attrs=["reverse"])
                                + colored(
                                    "   The requested Author could not be found.\n",
                                    "yellow",
                                )
                            )

                            author_list_not_found_typo = True

                            while author_list_not_found_typo == True:

                                author_not_found = input(
                                    colored(
                                        "\n-- Type [1] to retry Author Search\n-- Type [2] to search by a different criteria\n   : ",
                                    )
                                )

                                if author_not_found == "1":
                                    break
                                elif author_not_found == "2":
                                    author_search = False
                                    break
                                else:
                                    print(
                                        "\n\n"
                                        + colored(
                                            " ! ", "yellow", attrs=["reverse"]
                                        )
                                        + colored(
                                            "   It appears that you made a typo, please re-enter your selection.\n",
                                            "yellow",
                                        )
                                    )

                            continue

                        print(
                            "\n\n"
                            + colored(
                                "Please select an Author from the list below:\n",
                                "blue",
                            )
                        )

                        time.sleep(1)

                        author_list_number = 0

                        for Author_Name in Author_List_json:

                            author_list_number += 1

                            print(
                                "["
                                + str(author_list_number)
                                + "] "
                                + Author_Name["authorName"]
                            )

                        Author_Number_typo = True

                        while Author_Number_typo == True:

                            Author_Number = input(
                                colored(
                                    "\n\n-- Type the Number of the Author\n   : ",
                                )
                            )

                            if int(Author_Number) not in list(range(1, 11)):

                                print(
                                    "\n\n"
                                    + colored(" ! ", "yellow", attrs=["reverse"])
                                    + colored(
                                        "   It appears that you made a typo, please re-enter your selection.\n",
                                        "yellow",
                                    )
                                )

                            else:
                                Author_Number_typo = False

                        Author_Selected_urlenc = urllib.parse.quote(
                            Author_List_json[int(Author_Number) - 1]["authorName"]
                        )

                        Article_ID_list = requests.get(
                            f"https://api-service-mrz6aygprq-oa.a.run.app/api/articles?authorName={Author_Selected_urlenc}&scraped=0"
                        )

                        if Article_ID_list.status_code == 200:

                            Article_ID_list = Article_ID_list.json()

                            if len(Article_ID_list) > 0:

                                print(
                                    "\n"
                                    + colored(" ! ", "green", attrs=["reverse"])
                                    + colored(
                                        "  List of articles from selected Author found\n",
                                        "green",
                                    )
                                )

                                time.sleep(1)

                                author_search = False

                                search_criteria_typo = False

                            else:

                                # Add option to download articles by this author
                                print(
                                    "\n\n"
                                    + colored(" ! ", "yellow", attrs=["reverse"])
                                    + colored(
                                        "   It appears that all articles by this author are already available.\n",
                                        "yellow",
                                    )
                                )

                                author_list_not_found_typo = True

                                while author_list_not_found_typo == True:

                                    author_not_found = input(
                                        colored(
                                            "\n-- Type [1] to retry Author Search\n-- Type [2] to search by a different criteria\n   : ",
                                        )
                                    )

                                    if author_not_found == "1":
                                        break
                                    elif author_not_found == "2":
                                        author_search = False
                                        search_criteria_typo = True
                                        break
                                    else:
                                        print(
                                            "\n\n"
                                            + colored(
                                                " ! ", "yellow", attrs=["reverse"]
                                            )
                                            + colored(
                                                "   It appears that you made a typo, please re-enter your selection.\n",
                                                "yellow",
                                            )
                                        )
                        elif Article_ID_list.status_code == 400:

                            print(
                                "\n\n"
                                + colored(" ! ", "red", attrs=["reverse"])
                                + colored(
                                    "   An unexpected error occured.\n",
                                    "red",
                                )
                            )

                            author_list_not_found_typo = True

                            while author_list_not_found_typo == True:

                                author_not_found = input(
                                    colored(
                                        "\n-- Type [1] to retry Author Search\n-- Type [2] to search by a different criteria\n   : ",
                                    )
                                )

                                if author_not_found == "1":
                                    break
                                elif author_not_found == "2":
                                    author_search = False
                                    search_criteria_typo = True
                                    break
                                else:
                                    print(
                                        "\n\n"
                                        + colored(
                                            " ! ", "yellow", attrs=["reverse"]
                                        )
                                        + colored(
                                            "   It appears that you made a typo, please re-enter your selection.\n",
                                            "yellow",
                                        )
                                    )

                elif search_criteria == "2":

                    print(
                        "\n"
                        + colored(" i ", attrs=["reverse"])
                        + "   You have chosen to search by Journal Name.\n"
                    )

                    print(
                        "\n"
                        + colored(
                            "Please enter the Name of a Journal (EXAMPLE: Journal of Financial Education).\n",
                            "blue",
                        )
                    )

                    journal_search = True

                    while journal_search == True:

                        Journal_Name = input(
                            colored(
                                "\n-- Type Journal Name\n   : ",
                            )
                        )

                        Journal_Name_urlenc = urllib.parse.quote(Journal_Name)

                        Journal_List_json = requests.get(
                            f"https://api-service-mrz6aygprq-oa.a.run.app/api/journals?journalName={Journal_Name_urlenc}"
                        )

                        try:

                            Journal_List_json = Journal_List_json.json()

                        except:

                            print(
                                "\n\n"
                                + colored(" ! ", "yellow", attrs=["reverse"])
                                + colored(
                                    "   The requested Journal could not be found.\n",
                                    "yellow",
                                )
                            )

                            journal_list_not_found_typo = True

                            while journal_list_not_found_typo == True:

                                journal_not_found = input(
                                    colored(
                                        "\n-- Type [1] to retry Journal Search\n-- Type [2] to search by a different criteria\n   : ",
                                    )
                                )

                                if journal_not_found == "1":
                                    break
                                elif journal_not_found == "2":
                                    journal_search = False
                                    break
                                else:
                                    print(
                                        "\n\n"
                                        + colored(
                                            " ! ", "yellow", attrs=["reverse"]
                                        )
                                        + colored(
                                            "   It appears that you made a typo, please re-enter your selection.\n",
                                            "yellow",
                                        )
                                    )

                            continue

                        print(
                            "\n\n"
                            + colored(
                                "Please select a Journal from the list below:\n",
                                "blue",
                            )
                        )

                        time.sleep(1)

                        journal_list_number = 0

                        for Journal_Name in Journal_List_json:

                            journal_list_number += 1

                            print(
                                "["
                                + str(journal_list_number)
                                + "] "
                                + Journal_Name["journalName"]
                            )

                        Journal_Number_typo = True

                        while Journal_Number_typo == True:

                            Journal_Number = input(
                                colored(
                                    "\n\n-- Type the Number of the Journal\n   : ",
                                )
                            )

                            if int(Journal_Number) not in list(range(1, 11)):

                                print(
                                    "\n\n"
                                    + colored(" ! ", "yellow", attrs=["reverse"])
                                    + colored(
                                        "   It appears that you made a typo, please re-enter your selection.\n",
                                        "yellow",
                                    )
                                )

                            else:
                                Journal_Number_typo = False

                        Journal_Selected_urlenc = urllib.parse.quote(
                            Journal_List_json[int(Journal_Number) - 1][
                                "journalName"
                            ]
                        )

                        Article_ID_list = requests.get(
                            f"https://api-service-mrz6aygprq-oa.a.run.app/api/articles?journalName={Journal_Selected_urlenc}&scraped=0"
                        )

                        if Article_ID_list.status_code == 200:

                            Article_ID_list = Article_ID_list.json()

                            if len(Article_ID_list) > 0:

                                print(
                                    "\n"
                                    + colored(" ! ", "green", attrs=["reverse"])
                                    + colored(
                                        "  List of articles from selected Journal found\n",
                                        "green",
                                    )
                                )

                                time.sleep(1)

                                journal_search = False

                                search_criteria_typo = False

                            else:

                                # Add option to download articles by this author
                                print(
                                    "\n\n"
                                    + colored(" ! ", "yellow", attrs=["reverse"])
                                    + colored(
                                        "   It appears that all articles from this journal are already available.\n",
                                        "yellow",
                                    )
                                )

                                journal_list_not_found_typo = True

                                while journal_list_not_found_typo == True:

                                    journal_not_found = input(
                                        colored(
                                            "\n-- Type [1] to retry Journal Search\n-- Type [2] to search by a different criteria\n   : ",
                                        )
                                    )

                                    if journal_not_found == "1":
                                        break
                                    elif journal_not_found == "2":
                                        journal_search = False
                                        search_criteria_typo = True
                                        break
                                    else:
                                        print(
                                            "\n\n"
                                            + colored(
                                                " ! ", "yellow", attrs=["reverse"]
                                            )
                                            + colored(
                                                "   It appears that you made a typo, please re-enter your selection.\n",
                                                "yellow",
                                            )
                                        )
                        elif Article_ID_list.status_code == 200:

                            print(
                                "\n\n"
                                + colored(" ! ", "red", attrs=["reverse"])
                                + colored(
                                    "   An unexpected error occured.\n",
                                    "red",
                                )
                            )

                            journal_list_not_found_typo = True

                            while journal_list_not_found_typo == True:

                                journal_not_found = input(
                                    colored(
                                        "\n-- Type [1] to retry Journal Search\n-- Type [2] to search by a different criteria\n   : ",
                                    )
                                )

                                if journal_not_found == "1":
                                    break
                                elif journal_not_found == "2":
                                    journal_search = False
                                    search_criteria_typo = True
                                    break
                                else:
                                    print(
                                        "\n\n"
                                        + colored(
                                            " ! ", "yellow", attrs=["reverse"]
                                        )
                                        + colored(
                                            "   It appears that you made a typo, please re-enter your selection.\n",
                                            "yellow",
                                        )
                                    )

                else:

                    print(
                        "\n\n"
                        + colored(" ! ", "yellow", attrs=["reverse"])
                        + colored(
                            "   It appears that you made a typo, please re-enter your selection.\n",
                            "yellow",
                        )
                    )

            # Print End Message
            print(
                "\n\n"
                + colored(" i ", "blue", attrs=["reverse"])
                + "   PDF files located and Login process complete, the browser will run in the background."
            )

            time.sleep(1)

            print(
                "\n"
                + colored(" i ", "blue", attrs=["reverse"])
                + "   You can minimize this window and continue with other tasks on your computer while your files download."
            )

            time.sleep(1)

            print(
                "\n"
                + colored(" i ", "blue", attrs=["reverse"])
                + "   Do not exit/close this window as this will abort the download process.\n"
            )

            time.sleep(1)

        else:

            print(
                "\n\n"
                + colored(
                    "JSTOR PDF download specification:\n",
                    attrs=["bold", "underline"],
                )
            )

            print(
                "\n"
                + emoji.emojize(":information:")
                + "   Please select your search criteria"
            )

            search_criteria_typo = True

            while search_criteria_typo == True:

                search_criteria = input(
                    colored(
                        "\n-- Type [1] to search by Author Name\n-- Type [2] to search by Journal Name\n   : ",
                    )
                )

                if search_criteria == "1":

                    print(
                        "\n"
                        + emoji.emojize(":information:")
                        + "   You have chosen to search by Author Name.\n"
                    )

                    print(
                        "\n"
                        + colored(
                            "Please enter the Name and Surname of an Author (EXAMPLE: Rebecca Gould)\n",
                            attrs=["bold"],
                        )
                    )

                    author_search = True

                    while author_search == True:

                        Author_Name = input(
                            colored(
                                "\n-- Type Author Name and Surname\n   : ",
                            )
                        )

                        Author_Name_urlenc = urllib.parse.quote(Author_Name)

                        Author_List_json = requests.get(
                            f"https://api-service-mrz6aygprq-oa.a.run.app/api/authors?authorName={Author_Name_urlenc}"
                        )

                        try:

                            Author_List_json = Author_List_json.json()

                        except:

                            print(
                                "\n\n"
                                + emoji.emojize(":loudspeaker:")
                                + colored(
                                    "   The requested Author could not be found.\n",
                                    "yellow",
                                )
                            )

                            author_list_not_found_typo = True

                            while author_list_not_found_typo == True:

                                author_not_found = input(
                                    colored(
                                        "\n-- Type [1] to retry Author Search\n-- Type [2] to search by a different criteria\n   : ",
                                    )
                                )

                                if author_not_found == "1":
                                    break
                                elif author_not_found == "2":
                                    author_search = False
                                    break
                                else:
                                    print(
                                        "\n\n"
                                        + emoji.emojize(":loudspeaker:")
                                        + colored(
                                            "   It appears that you made a typo, please re-enter your selection.\n",
                                            "yellow",
                                        )
                                    )

                            continue

                        print(
                            "\n\n"
                            + colored(
                                "Please select a Author from the list below:\n",
                                attrs=["bold"],
                            )
                        )

                        time.sleep(1)

                        author_list_number = 0

                        for Author_Name in Author_List_json:

                            author_list_number += 1

                            print(
                                "["
                                + str(author_list_number)
                                + "] "
                                + Author_Name["authorName"]
                            )

                        Author_Number_typo = True

                        while Author_Number_typo == True:

                            Author_Number = input(
                                colored(
                                    "\n\n-- Type the Number of the Author\n   : ",
                                )
                            )

                            if int(Author_Number) not in list(range(1, 11)):

                                print(
                                    "\n\n"
                                    + emoji.emojize(":loudspeaker:")
                                    + colored(
                                        "   It appears that you made a typo, please re-enter your selection.\n",
                                        "yellow",
                                    )
                                )

                            else:
                                Author_Number_typo = False

                        Author_Selected_urlenc = urllib.parse.quote(
                            Author_List_json[int(Author_Number) - 1]["authorName"]
                        )

                        Article_ID_list = requests.get(
                            f"https://api-service-mrz6aygprq-oa.a.run.app/api/articles?authorName={Author_Selected_urlenc}&scraped=0"
                        )

                        if Article_ID_list.status_code == 200:

                            Article_ID_list = Article_ID_list.json()

                            if len(Article_ID_list) > 0:

                                print(
                                    "\n"
                                    + emoji.emojize(":check_mark_button:")
                                    + colored(
                                        "  List of articles from selected Author found\n",
                                        "green",
                                    )
                                )

                                time.sleep(1)

                                author_search = False

                                search_criteria_typo = False

                            else:

                                # Add option to download articles by this author
                                print(
                                    "\n\n"
                                    + emoji.emojize(":loudspeaker:")
                                    + colored(
                                        "   It appears that all articles by this author are already available.\n",
                                        "yellow",
                                    )
                                )

                                author_list_not_found_typo = True

                                while author_list_not_found_typo == True:

                                    author_not_found = input(
                                        colored(
                                            "\n-- Type [1] to retry Author Search\n-- Type [2] to search by a different criteria\n   : ",
                                        )
                                    )

                                    if author_not_found == "1":
                                        break
                                    elif author_not_found == "2":
                                        author_search = False
                                        search_criteria_typo = True
                                        break
                                    else:
                                        print(
                                            "\n\n"
                                            + emoji.emojize(":loudspeaker:")
                                            + colored(
                                                "   It appears that you made a typo, please re-enter your selection.\n",
                                                "yellow",
                                            )
                                        )
                        elif Article_ID_list.status_code == 400:

                            print(
                                "\n\n"
                                + emoji.emojize(":red_exclamation_mark:")
                                + colored(
                                    "   An unexpected error occured.\n",
                                    "red",
                                )
                            )

                            author_list_not_found_typo = True

                            while author_list_not_found_typo == True:

                                author_not_found = input(
                                    colored(
                                        "\n-- Type [1] to retry Author Search\n-- Type [2] to search by a different criteria\n   : ",
                                    )
                                )

                                if author_not_found == "1":
                                    break
                                elif author_not_found == "2":
                                    author_search = False
                                    search_criteria_typo = True
                                    break
                                else:
                                    print(
                                        "\n\n"
                                        + emoji.emojize(":loudspeaker:")
                                        + colored(
                                            "   It appears that you made a typo, please re-enter your selection.\n",
                                            "yellow",
                                        )
                                    )

                elif search_criteria == "2":

                    print(
                        "\n"
                        + emoji.emojize(":information:")
                        + "   You have chosen to search by Journal Name.\n"
                    )

                    print(
                        "\n"
                        + colored(
                            "Please enter the Name of a Journal (EXAMPLE: Journal of Financial Education).\n",
                            attrs=["bold"],
                        )
                    )

                    journal_search = True

                    while journal_search == True:

                        Journal_Name = input(
                            colored(
                                "\n-- Type Journal Name\n   : ",
                            )
                        )

                        Journal_Name_urlenc = urllib.parse.quote(Journal_Name)

                        Journal_List_json = requests.get(
                            f"https://api-service-mrz6aygprq-oa.a.run.app/api/journals?journalName={Journal_Name_urlenc}"
                        )

                        try:

                            Journal_List_json = Journal_List_json.json()

                        except:

                            print(
                                "\n\n"
                                + emoji.emojize(":loudspeaker:")
                                + colored(
                                    "   The requested Journal could not be found.\n",
                                    "yellow",
                                )
                            )

                            journal_list_not_found_typo = True

                            while journal_list_not_found_typo == True:

                                journal_not_found = input(
                                    colored(
                                        "\n-- Type [1] to retry Journal Search\n-- Type [2] to search by a different criteria\n   : ",
                                    )
                                )

                                if journal_not_found == "1":
                                    break
                                elif journal_not_found == "2":
                                    journal_search = False
                                    break
                                else:
                                    print(
                                        "\n\n"
                                        + emoji.emojize(":loudspeaker:")
                                        + colored(
                                            "   It appears that you made a typo, please re-enter your selection.\n",
                                            "yellow",
                                        )
                                    )

                            continue

                        print(
                            "\n\n"
                            + colored(
                                "Please select a Journal from the list below:\n",
                                attrs=["bold"],
                            )
                        )

                        time.sleep(1)

                        journal_list_number = 0

                        for Journal_Name in Journal_List_json:

                            journal_list_number += 1

                            print(
                                "["
                                + str(journal_list_number)
                                + "] "
                                + Journal_Name["journalName"]
                            )

                        Journal_Number_typo = True

                        while Journal_Number_typo == True:

                            Journal_Number = input(
                                colored(
                                    "\n\n-- Type the Number of the Journal\n   : ",
                                )
                            )

                            if int(Journal_Number) not in list(range(1, 11)):

                                print(
                                    "\n\n"
                                    + emoji.emojize(":loudspeaker:")
                                    + colored(
                                        "   It appears that you made a typo, please re-enter your selection.\n",
                                        "yellow",
                                    )
                                )

                            else:
                                Journal_Number_typo = False

                        Journal_Selected_urlenc = urllib.parse.quote(
                            Journal_List_json[int(Journal_Number) - 1][
                                "journalName"
                            ]
                        )

                        Article_ID_list = requests.get(
                            f"https://api-service-mrz6aygprq-oa.a.run.app/api/articles?journalName={Journal_Selected_urlenc}&scraped=0"
                        )

                        if Article_ID_list.status_code == 200:

                            Article_ID_list = Article_ID_list.json()

                            if len(Article_ID_list) > 0:

                                print(
                                    "\n"
                                    + emoji.emojize(":check_mark_button:")
                                    + colored(
                                        "  List of articles from selected Journal found\n",
                                        "green",
                                    )
                                )

                                time.sleep(1)

                                journal_search = False

                                search_criteria_typo = False

                            else:

                                # Add option to download articles by this author
                                print(
                                    "\n\n"
                                    + emoji.emojize(":loudspeaker:")
                                    + colored(
                                        "   It appears that all articles from this journal are already available.\n",
                                        "yellow",
                                    )
                                )

                                journal_list_not_found_typo = True

                                while journal_list_not_found_typo == True:

                                    journal_not_found = input(
                                        colored(
                                            "\n-- Type [1] to retry Journal Search\n-- Type [2] to search by a different criteria\n   : ",
                                        )
                                    )

                                    if journal_not_found == "1":
                                        break
                                    elif journal_not_found == "2":
                                        journal_search = False
                                        search_criteria_typo = True
                                        break
                                    else:
                                        print(
                                            "\n\n"
                                            + emoji.emojize(":loudspeaker:")
                                            + colored(
                                                "   It appears that you made a typo, please re-enter your selection.\n",
                                                "yellow",
                                            )
                                        )
                        elif Article_ID_list.status_code == 200:

                            print(
                                "\n\n"
                                + emoji.emojize(":red_exclamation_mark:")
                                + colored(
                                    "   An unexpected error occured.\n",
                                    "red",
                                )
                            )

                            journal_list_not_found_typo = True

                            while journal_list_not_found_typo == True:

                                journal_not_found = input(
                                    colored(
                                        "\n-- Type [1] to retry Journal Search\n-- Type [2] to search by a different criteria\n   : ",
                                    )
                                )

                                if journal_not_found == "1":
                                    break
                                elif journal_not_found == "2":
                                    journal_search = False
                                    search_criteria_typo = True
                                    break
                                else:
                                    print(
                                        "\n\n"
                                        + emoji.emojize(":loudspeaker:")
                                        + colored(
                                            "   It appears that you made a typo, please re-enter your selection.\n",
                                            "yellow",
                                        )
                                    )

                else:

                    print(
                        "\n\n"
                        + emoji.emojize(":loudspeaker:")
                        + colored(
                            "   It appears that you made a typo, please re-enter your selection.\n",
                            "yellow",
                        )
                    )

            # Print End Message
            print(
                "\n\n"
                + emoji.emojize(":information:")
                + "   PDF files located and Login process complete, the browser will run in the background."
            )

            time.sleep(1)

            print(
                "\n"
                + emoji.emojize(":information:")
                + "   You can minimize this window and continue with other tasks on your computer while your files download."
            )

            time.sleep(1)

            print(
                "\n"
                + emoji.emojize(":information:")
                + "   Do not exit/close this window as this will abort the download process.\n"
            )

            time.sleep(1)

    else:

        restart_driver_session(
            jstor_url,
            options(get_login_method, USER_AGENT, storage_directory),
            driver.command_executor._url,
            driver.session_id,
        )

        time.sleep(wait)

        Article_ID_list = Article_ID_list[article_index:]



