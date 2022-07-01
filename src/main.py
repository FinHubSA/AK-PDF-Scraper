import pickle
import time
import os.path
import json
from datetime import datetime
import logging

import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

from recaptcha_solver import recaptcha_solver
from user_agent import user_agent
from user_login import user_login_guide
from temp_storage import get_temp_storage_path, rename_file
from internet_speed import download_speed, delay


def latest_downloaded_pdf(storage_directory, src_directory):

    os.chdir(storage_directory)

    pdf_download_list = sorted(os.listdir(storage_directory), key=os.path.getmtime)

    latest_pdf = pdf_download_list[-1]

    os.chdir(src_directory)

    return latest_pdf


def create_driver_session(chrome_options):

    logging.getLogger("WDM").setLevel(logging.NOTSET)

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options,
    )

    driver.minimize_window()

    return driver


def restart_driver_session(jstor_url, chrome_options, executor_url, session_id):

    capabilities = chrome_options.to_capabilities()

    driver = webdriver.Remote(
        command_executor=executor_url, desired_capabilities=capabilities
    )

    driver.close()

    driver.session_id = session_id

    driver.get(jstor_url)


storage_directory = get_temp_storage_path()

src_directory = os.path.dirname(__file__)

misc_directory = os.path.normpath(src_directory + os.sep + os.pardir)

# To create an executable file we need to set the file source directory
os.chdir(src_directory)

# Set chrome options to mimic a real user, User Agent is crucial
USER_AGENT = user_agent()
chrome_options = webdriver.ChromeOptions()

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

# Calculate the driver sleep time
mbps = download_speed()

wait = delay(mbps)

now = datetime.now().timestamp()

# Start the driver session
driver = create_driver_session(chrome_options)

restart_count = 0

jstor_url = None

while True:

    # User will login when program starts
    # after each restart, reload the web session
    if restart_count == 0:

        web_session = user_login_guide(driver, "https://www.jstor.org", wait)

        # Save the cookies to ensure reCAPTCHA can be solved
        # since login details are required to access the mp3 file
        pickle.dump(
            driver.get_cookies(),
            open(os.path.join(misc_directory, "cookies.pkl"), "wb"),
        )

        cookies = pickle.load(open(os.path.join(misc_directory, "cookies.pkl"), "rb"))

        for cookie in cookies:
            driver.add_cookie(cookie)

        # Save the url after user login as each url
        # will be unique to the user's institution
        jstor_url = driver.current_url

    else:

        restart_driver_session(
            jstor_url, chrome_options, driver.command_executor._url, driver.session_id
        )

        time.sleep(wait)

    # define the jstor landing page window
    win_1 = driver.window_handles[0]

    t_c_accepted = False

    t_c_try_accept = 0

    with open(os.path.join(misc_directory, "start.json"), "r") as input_file:
        scraper_startpoint = json.load(input_file)

    bookmark = scraper_startpoint["start"]

    # Retrieve user requested article ID's
    # This is temporary
    # We will need to get data from a database in the future.
    article_ID = pd.read_csv(os.path.join(misc_directory, "Metadata.csv"))["ID"]

    # Loop through article ID's
    for article in article_ID[bookmark : len(article_ID)]:

        # wait = delay(end_time, start_time, download_time_list)
        # Calculate the waiting time every 30 mins
        # to adjust wait according to user internet speed
        if datetime.now().timestamp() >= now + 1200:

            mbps = download_speed()

            wait = delay(mbps)

            now = datetime.now().timestamp()

        url = os.path.join(storage_directory, article.split("/")[-1] + ".pdf")

        url_pending = os.path.join(
            storage_directory, article.split("/")[-1] + ".pdf.crdownload"
        )

        doi = os.path.join(
            storage_directory,
            article.split("/")[0] + "." + article.split("/")[-1] + ".pdf",
        )

        # Check if pdf file already exists in user directory
        # Delete if download pending, rename and skip iteration if file exists
        if os.path.exists(url):

            rename_file(url, doi)

            continue

        elif os.path.exists(url_pending):

            os.remove(url_pending)

        # navigate to the pdf download page (win_2)
        driver.execute_script(
            "window.open('" + jstor_url + "stable/pdf/" + article + ".pdf','_blank')"
        )

        start_time = datetime.now().timestamp()

        # The driver switches between two windows
        # win_1 is the jstor home page and win_2 is either the t&c's,
        # recaptcha or download page (which is hidden)
        win_2 = driver.window_handles[1]

        driver.switch_to.window(win_2)

        # Check for cookies, t&c's and reCAPTCHA
        # The t&c's only pop up each time you restart the browser session

        while not t_c_accepted and t_c_try_accept <= 3:

            restart = None

            t_c_try_accept = +1

            # Accept cookies
            try:

                WebDriverWait(driver, wait).until(
                    expected_conditions.element_to_be_clickable(
                        (By.XPATH, r"//button[@id='onetrust-accept-btn-handler']")
                    )
                ).click()

                print("cookies accepted")

            except:

                print("no cookies")

            # Accept t&c's
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

            # Check for reCAPTCHA
            except:

                try:

                    driver.switch_to.window(win_2)

                    success, start_time = recaptcha_solver(
                        driver, url, url_pending, wait, misc_directory
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

                except:

                    print("no t&c's")

                    t_c_accepted = True

        if restart:

            restart_count = +1

            break

        time.sleep(wait)

        # Check for reCAPTCHA

        if not (os.path.exists(url) or os.path.exists(url_pending)):

            success, start_time = recaptcha_solver(
                driver, url, url_pending, wait, misc_directory
            )

            if not success:

                print(
                    "[ERR] reCAPTCHA could not be solved or pdf could not be downloaded, restarting driver session"
                )

                restart_count = +1

                break

        # Check if download is complete
        file = url_pending

        count = 0

        while file == url_pending and count <= 120:

            time.sleep(1)

            count += 1

            newest_file = latest_downloaded_pdf(storage_directory, src_directory)

            if newest_file == article.split("/")[-1] + ".pdf":

                file = url

            else:

                file = url_pending

        end_time = datetime.now().timestamp()

        # Rename the pdf
        try:

            rename_file(url, doi)

        except Exception as e:

            print(e)

            print("[ERR] Could not download pdf file, restarting driver session")

            restart_count = +1

            break

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

        # Append the tracker file
        bookmark = bookmark + 1

        scraper_startpoint["start"] = bookmark

        with open(os.path.join(misc_directory, "start.json"), "w") as input_file:
            json.dump(scraper_startpoint, input_file)

        try:

            driver.close()

            driver.switch_to.window(win_1)

        except:

            driver.switch_to.window(win_1)

    try:

        driver.close()

        driver.switch_to.window(win_1)

    except:

        driver.switch_to.window(win_1)

    time.sleep(wait)
