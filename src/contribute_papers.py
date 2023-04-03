import time
import os.path
from datetime import datetime
import logging
import emoji
import os
import string
import random
import warnings
import urllib3

from termcolor import colored
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from src.errors import MainException, TypoException

from src.recaptcha_solver import recaptcha_solver
from src.user_agent import get_user_agent
from src.temp_storage import (
    get_temp_storage_path,
    get_storage_path,
    latest_downloaded_pdf,
    misc_path,
    rename_file,
    delete_files,
    delete_temp_storage,
)

from src.helpers import (
    set_cookies,
    system,
    print_typo,
    server_response_post,
    receive_network_error_action,
)
from src.donations import print_donation_explainer, receive_donation_action
from src.internet_speed import download_speed, delay, internet_speed_retry
from src.user_login import (
    manual_login,
    receive_login_action,
    print_login_requirements,
    print_login_instructions,
    receive_end_program_action,
    receive_proceed_action,
    vpn_login,
)
from src.upload_papers import receive_upload_criteria_action

warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=UserWarning)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.getLogger().setLevel(logging.CRITICAL)


jstor_url = (
    now
) = (
    USER_AGENT
) = (
    wait
) = (
    driver
) = (
    storage_directory
) = Article_ID_list = src_directory = misc_directory = algorandAddress = None

restart_count = article_index = mbps = index = 0

is_windows = system()


def contribute_papers():

    global algorandAddress, restart_count

    setup()

    print_login_requirements()

    print_donation_explainer()

    algorandAddress = receive_donation_action()

    time.sleep(1)

    print_login_instructions()

    login()

    while True:

        try:

            get_article_ids()

            download_articles()

        except MainException:
            raise

        except Exception as e:

            if "ERR_INTERNET_DISCONNECTED" in str(e):

                receive_network_error_action()

                internet_speed_retry()

                restart_count += 1

            else:

                print(
                    "\n\n"
                    + colored(" ! ", "red", attrs=["reverse"]) * (is_windows)
                    + emoji.emojize(":red_exclamation_mark:") * (not is_windows)
                    + colored(
                        "   An unexpected error occured. Exiting, try again.\n",
                        "red",
                    )
                )

                os._exit(0)


def setup():

    global storage_directory, src_directory, misc_directory, mbps, wait, USER_AGENT, now

    storage_directory = get_temp_storage_path()

    src_directory = get_storage_path()

    misc_directory = misc_path()

    # mbps = internet_speed_retry()
    mbps = 90

    wait = delay(mbps)

    print("\n\nDetermining User Agent.")
    print(
        "\nYou may notice that a browser window opened, don't worry, we're just checking your User Agent online!"
    )

    # USER_AGENT = get_user_agent(wait)
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"

    now = datetime.now().timestamp()


def login():

    global driver

    logged_in = False

    while not logged_in:

        try:

            login_method = receive_login_action()

            if login_method == "1":

                print(
                    "\n"
                    + colored(" i ", "blue", attrs=["reverse"]) * (is_windows)
                    + emoji.emojize(":information:") * (not is_windows)
                    + "   You will be prompted to login via your university wifi or VPN."
                )

                time.sleep(1)

                cont = receive_proceed_action()

                if cont == "1":
                    driver = create_driver_session(
                        options(login_method, USER_AGENT, storage_directory)
                    )
                    logged_in = vpn_login(
                        driver,
                        "https://www.jstor.org/",
                        "query-builder-input-group",
                        "pds__access-provided-by",
                    )
                elif cont == "2":
                    return login()

            elif login_method == "2":

                print(
                    "\n"
                    + colored(" i ", "blue", attrs=["reverse"]) * (is_windows)
                    + emoji.emojize(":information:") * (not is_windows)
                    + "   You will be prompted to manually login via the JSTOR website."
                )

                time.sleep(1)

                cont = receive_proceed_action()

                if cont == "1":
                    driver = create_driver_session(
                        options(login_method, USER_AGENT, storage_directory)
                    )
                    logged_in = manual_login(
                        driver,
                        "https://www.jstor.org/",
                        "query-builder-input-group",
                        "pds__access-provided-by",
                    )
                elif cont == "2":
                    return login()

            elif login_method == "3":
                raise MainException
            else:
                print_typo()
                return login()

        except Exception as e:

            if "ERR_INTERNET_DISCONNECTED" in str(e):

                receive_network_error_action()

                internet_speed_retry()

                return login()

            else:

                print(
                    "\n\n"
                    + colored(" ! ", "red", attrs=["reverse"]) * (is_windows)
                    + emoji.emojize(":red_exclamation_mark:") * (not is_windows)
                    + colored(
                        "   An unexpected error occured. Exiting, try again.\n",
                        "red",
                    )
                )

                os._exit(0)


def create_driver_session(chrome_options):

    global driver

    try:

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager(path=misc_directory).install()),
            options=chrome_options,
        )

        driver.minimize_window()

        return driver

    except:

        print(
            "\n"
            + colored(" i ", "red", attrs=["reverse"]) * (is_windows)
            + emoji.emojize(":red_exclamation_mark:") * (not is_windows)
            + colored(
                "  A Chromedriver exception occurred. Issue could not be resolved, exiting.",
                "red",
            )
        )

        print(
            "\n"
            + colored(" i ", "blue", attrs=["reverse"]) * (is_windows)
            + emoji.emojize(":information:") * (not is_windows)
            + colored("   Restart your device and try again.")
        )

        os._exit(0)


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


def enable_download_in_headless_chrome():

    driver.command_executor._commands["send_command"] = (
        "POST",
        "/session/$sessionId/chromium/send_command",
    )
    params = {
        "cmd": "Page.setDownloadBehavior",
        "params": {"behavior": "allow", "downloadPath": storage_directory},
    }

    driver.execute("send_command", params)


def restart_driver_session(jstor_url, chrome_options, executor_url, session_id):

    driver = webdriver.Remote(command_executor=executor_url, options=chrome_options)

    driver.close()

    driver.session_id = session_id

    driver.get(jstor_url)


def get_article_ids():

    global Article_ID_list, jstor_url

    if restart_count == 0:

        set_cookies(driver, misc_directory)

        # Save the url after user login as each url
        # will be unique to the user's institution
        jstor_url = driver.current_url

        # User select which papers they would like to download (API Call)
        print(
            "\n\n" + colored("JSTOR PDF download specification:\n", attrs=["reverse"])
        )

        Article_ID_list = receive_upload_criteria_action(driver)

    elif 0 < restart_count <= 5:

        restart_driver_session(
            jstor_url,
            options(receive_login_action, USER_AGENT, storage_directory),
            driver.command_executor._url,
            driver.session_id,
        )

        time.sleep(wait * 10)

        Article_ID_list = Article_ID_list[article_index:]

    else:
        print(
            "\n"
            + colored(" ! ", "red", attrs=["reverse"]) * (is_windows)
            + emoji.emojize(":red_exclamation_mark:") * (not is_windows)
            + colored(
                "  Unforturnately we cannot upload the requested papers at this moment. Please try again later.\n",
                "red",
            )
        )

        driver.close()
        os._exit(0)


def download_articles():

    global article_index, now, restart_count, wait

    restart = t_c_accepted = False

    t_c_try_accept = 0

    # loop through user requested article ID's
    # if error occurs, restart the web session and start at last indexed ID
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

        # construct a random name for the pdf file
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

        # check if pdf file already exists in user directory
        # delete if download pending or file exist to circumvent malicious actors
        if os.path.exists(url):

            os.remove(url)

        elif os.path.exists(url_pending):

            os.remove(url_pending)

        driver.get(jstor_url + "stable/pdf/" + article + ".pdf")

        # to avoid chromedriver status code: -9
        enable_download_in_headless_chrome()

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

                print("[INF] cookies accepted")

            except:

                print("[INF] no cookies")

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

                print("[INF] t&c's accepted")

                start_time = datetime.now().timestamp()

                success = True

                t_c_accepted = True

            # check for reCAPTCHA
            except:

                if not (os.path.exists(url) or os.path.exists(url_pending)):

                    success, start_time = recaptcha_solver(
                        driver, url, url_pending, wait, misc_directory, jstor_url
                    )

                    if success:

                        print("[INF] reCAPTCHA solved")

                        continue

                    elif success == None:

                        print(
                            "[ERR] Your institution does not have access to this article, skipping to next article"
                        )

                        driver.get(jstor_url)

                        break

                    else:

                        print(
                            "[ERR] reCAPTCHA could not be solved, restarting driver session"
                        )

                        restart = True

                        break

                else:

                    print("[INF] no t&c's")

                    success = True

                    t_c_accepted = True

        if restart:

            restart_count += 1

            break

        if success == None:

            continue

        time.sleep(wait)

        # check for reCAPTCHA
        if not (os.path.exists(url) or os.path.exists(url_pending)):

            success, start_time = recaptcha_solver(
                driver, url, url_pending, wait, misc_directory, jstor_url
            )

            if success:

                print("[INF] reCAPTCHA solved")

            elif success == None:

                print(
                    "[ERR] Your institution does not have access to this article, skipping to next article"
                )

                driver.get(jstor_url)

                continue

            else:

                print(
                    "[ERR] ReCAPTCHA could not be solved or pdf could not be found, restarting driver session."
                )

                restart = True

                restart_count = +1

                break

        # check for no access via institution
        if not (os.path.exists(url) or os.path.exists(url_pending)):

            print(
                "[ERR] Your institution does not have access to this article, skipping to next article"
            )

            driver.get(jstor_url)

            continue

        # check if download is complete
        file = url_pending

        count = 0

        while file == url_pending and count <= 120:

            time.sleep(1)

            count += 1

            latest_file = latest_downloaded_pdf(storage_directory)

            if latest_file == article.split("/")[-1] + ".pdf":

                file = url

            else:

                file = url_pending

        end_time = datetime.now().timestamp()

        # rename the pdf
        try:

            rename_file(url, doi)

        except:

            print("[ERR] Could not download pdf file, restarting driver session")

            restart_count += 1

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
            log.write("\nscraper ended at: " + str(datetime.fromtimestamp(end_time)))
            log.write(
                "\ndownload time (in seconds): " + str(end_time - start_time - wait)
            )

        # upload pdf file to Google Drive
        files = {"file": open(doi, "rb")}
        data = {"articleJstorID": article, "algorandAddress": algorandAddress}

        server_response_post(
            driver,
            "https://api-service-mrz6aygprq-oa.a.run.app/api/articles/pdf",
            files,
            data,
            article_json,
            storage_directory,
        )

        # delete article from local storage
        try:
            delete_files(doi)
        except:
            print(f"[INF]: Could not delete pdf locally.")

        if article_json == Article_ID_list[-1]:

            # delete the entire Aaron's Kit folder
            try:

                delete_temp_storage(storage_directory)

            except:

                print("[INF]: Could not delete AaronsKit_PDF_Downloads folder.")

            print(
                "\n"
                + colored(" ! ", "green", attrs=["reverse"]) * (is_windows)
                + emoji.emojize(":check_mark_button:") * (not is_windows)
                + colored(
                    "  You have successfully uploaded your requested papers.",
                    "green",
                )
            )

            break

    # stop when all articles have downloaded or when server error, otherwise navigate to home page and restart web session
    if article_json == Article_ID_list[-1] and not restart:

        # user message after scraping complete
        restart_count = receive_end_program_action(driver)

    else:
        driver.get(jstor_url)

    article_index = index
