import pickle
import time
import os.path
import json
from datetime import datetime
import logging
import re

import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

from recaptcha_solver import recaptcha_solver
from user_agent import user_agent_fixed

# from user_agent import user_agent
from user_login import *
from user_login import welcome
from temp_storage import get_temp_storage_path, rename_file
from internet_speed import download_speed, delay

# from digital_ocean_upload import pdf_upload


def latest_downloaded_pdf(storage_directory, src_directory):

    os.chdir(storage_directory)

    pdf_download_list = sorted(os.listdir(storage_directory), key=os.path.getmtime)

    latest_pdf = pdf_download_list[-1]

    os.chdir(src_directory)

    return latest_pdf


def create_driver_session(chrome_options):

    logging.getLogger("WDM").setLevel(logging.NOTSET)
    os.environ["WDM_LOG"] = "false"
    os.environ['WDM_LOG_LEVEL'] = '0'

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options,
    )

    driver.minimize_window()

    return driver


def restart_driver_session(jstor_url, chrome_options, executor_url, session_id):

    driver = webdriver.Remote(command_executor=executor_url, options=chrome_options)

    driver.close()

    driver.session_id = session_id

    driver.get(jstor_url)


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


storage_directory = get_temp_storage_path()

src_directory = os.path.dirname(__file__)

misc_directory = os.path.normpath(src_directory + os.sep + os.pardir)

# To create an executable file we need to set the file source directory
os.chdir(src_directory)

# Aaron's Kit welcome
welcome()

# def User Agent
USER_AGENT = user_agent_fixed()

# Calculate the driver sleep time
print("\x1B[3m" + "\n...determining internet speed" + "\033[0m")

mbps = download_speed()

print(
    color.GREEN
    + "\nYour internet speed is: "
    + str(round(mbps, 2))
    + " mbps"
    + color.END
)

wait = delay(mbps)

now = datetime.now().timestamp()

restart_count = 0

jstor_url = None

while True:

    # User will login when program starts
    # after each restart, reload the web session
    if restart_count == 0:

        time.sleep(1)

        print(
            "\n"
            + emoji.emojize(":information:")
            + "   To continue, a JSTOR user login is required, either via institution VPN/wifi or manually via the JSTOR website"
        )

        time.sleep(1)

        print(
            "\n"
            + emoji.emojize(":information:")
            + "   No login information will be recorded in the process"
        )

        time.sleep(1)

        print(
            color.BOLD + color.UNDERLINE + "\n\nJSTOR Login Instructions\n" + color.END
        )

        print(
            "\n"
            + emoji.emojize(":information:")
            + "   Please follow the prompts below to login"
        )

        login_method = login()

        while True:
            if login_method == "1":
                # Start the driver session
                driver = create_driver_session(
                    options(login_method, USER_AGENT, storage_directory)
                )

                print(
                    "\n"
                    + emoji.emojize(":information:")
                    + "   You have chosen to login via VPN/wifi"
                )

                # "\n[INFO] Follow the instructions below"
                time.sleep(1)

                print(
                    "\n" + emoji.emojize(":information:") + "   Follow the steps below"
                )

                time.sleep(1)

                print(
                    color.BOLD
                    + "\n\nStep 1/1: Please connect to your institution's VPN or wifi, then continue\n"
                    + color.END
                )

                time.sleep(1)

                cont = proceed()

                if cont == "1":

                    print(
                        color.ITALIC
                        + "\n...you are now being routed to JSTOR home page"
                        + color.END
                    )

                    time.sleep(2)

                    print(
                        color.ITALIC
                        + "\n...give it a second, we are checking if the page has loaded successfully"
                        + color.END
                    )

                    driver.get("https://www.jstor.org/")

                    try:

                        WebDriverWait(driver, 60).until(
                            expected_conditions.element_to_be_clickable(
                                (
                                    By.CLASS_NAME,
                                    "query-builder-input-group",
                                )
                            )
                        )

                    except:
                        print(
                            "\n"
                            + emoji.emojize(":red_exclamation_mark:")
                            + color.RED
                            + " Unable to load JSTOR page\n"
                            + color.END
                        )

                        print(
                            "\n"
                            + emoji.emojize(":information:")
                            + "  Check your internet connection and try again\n"
                        )

                        driver.close()
                        login_method = login()

                    print(
                        color.ITALIC + "\n...checking for successful login" + color.END
                    )

                    time.sleep(2)

                    try:
                        driver.find_element(By.CLASS_NAME, "pds__access-provided-by")
                        time.sleep(1)
                        print(
                            "\n"
                            + emoji.emojize(":check_mark_button:")
                            + color.GREEN
                            + "  Login was successful!\n"
                            + color.END
                        )

                        time.sleep(1)

                        driver.maximize_window()

                        driver.set_window_position(-2024, 2024)

                        print(
                            "\n"
                            + emoji.emojize(":information:")
                            + "   Login process complete, the browser will run in the background"
                        )

                        time.sleep(1)

                        print(
                            "\n"
                            + emoji.emojize(":information:")
                            + "   You can continue with other tasks on your computer while your files download"
                        )

                        time.sleep(wait)
                        break

                    except:
                        time.sleep(1)
                        print(
                            "\n"
                            + emoji.emojize(":red_exclamation_mark:")
                            + color.RED
                            + "  Login was unsuccessful\n"
                            + color.END
                        )
                        x = main_menu()
                        if x == "1":
                            driver.close()
                            login_method = login()
                        elif x == "2":
                            os._exit(0)
                        continue

                elif cont == "2":
                    x = main_menu()
                    if x == "1":
                        driver.close()
                        login_method = login()
                    elif x == "2":
                        os._exit(0)
                else:
                    x = typo()
                    if x == "1":
                        driver.close()
                        login_method = login()
                    elif x == "2":
                        os._exit(0)

            elif login_method == "2":
                # Start the driver session
                driver = create_driver_session(
                    options(login_method, USER_AGENT, storage_directory)
                )

                time.sleep(1)

                print(
                    "\n"
                    + emoji.emojize(":information:")
                    + "   You will be prompted to manually login via the JSTOR website"
                )

                time.sleep(1)

                cont = proceed()

                if cont == "1":

                    print(
                        color.ITALIC
                        + "\n...you are now being routed to JSTOR home page"
                    )

                    time.sleep(2)

                    print(
                        "\n...sit tight and wait for Google Chrome to open on your screen"
                        + color.END
                    )

                    time.sleep(2)

                    print(
                        "\n"
                        + emoji.emojize(":information:")
                        + "   While the browser opens, read through the login steps"
                    )

                    time.sleep(1)

                    print(
                        color.BOLD
                        + "\nStep 1/4: Navigate to the top of the JSTOR home page, and click on the link: "
                        + color.UNDERLINE
                        + "Log in through your library"
                        + color.END
                        + color.BOLD
                        + "\nStep 2/4: Search for your institution by using the search box"
                        + "\nStep 3/4: Log in using your institution's login credentials"
                        + "\nStep 4/4: Accept the cookies"
                        + color.END
                    )

                    time.sleep(1)

                    print(
                        color.ITALIC
                        + "\n...give it a second, we are checking if the page has loaded successfully"
                        + color.END
                    )

                    driver.get("https://www.jstor.org/")

                    try:

                        WebDriverWait(driver, 60).until(
                            expected_conditions.element_to_be_clickable(
                                (By.CLASS_NAME, "query-builder-input-group")
                            )
                        )
                    except:
                        print(
                            "\n"
                            + emoji.emojize(":red_exclamation_mark:")
                            + color.RED
                            + " Unable to load JSTOR page\n"
                            + color.END
                        )

                        print(
                            "\n"
                            + emoji.emojize(":information:")
                            + "  Check your internet connection and try again\n"
                        )

                        driver.close()
                        login_method = login()

                    driver.maximize_window()

                    print(
                        "\n"
                        + emoji.emojize(":information:")
                        + "   Once you have completed the steps, continue"
                    )

                    cont = proceed()

                    if cont == "1":

                        try:

                            WebDriverWait(driver, 60).until(
                                expected_conditions.element_to_be_clickable(
                                    (By.CLASS_NAME, "query-builder-input-group")
                                )
                            )

                        except:
                            print(
                                color.RED
                                + "\n[INFO] Unable to load JSTOR page"
                                + color.END
                            )
                            # print(
                            #     color.YELLOW
                            #     + "\n[INFO] Check your internet connection and try again"
                            #     + color.END
                            # )
                            # login_method = login(2)

                        print(
                            color.ITALIC
                            + "\n...checking for successful login"
                            + color.END
                        )
                        time.sleep(1)

                        try:
                            driver.find_element(
                                By.CLASS_NAME, "pds__access-provided-by"
                            )
                            time.sleep(1)
                            print(
                                "\n"
                                + emoji.emojize(":check_mark_button:")
                                + color.GREEN
                                + "  Login was successful!\n"
                                + color.END
                            )

                            time.sleep(1)

                            driver.maximize_window()

                            driver.set_window_position(-2024, 2024)

                            print(
                                "\n"
                                + emoji.emojize(":information:")
                                + "   Login process complete, the browser will run in the background"
                            )

                            time.sleep(1)

                            print(
                                "\n"
                                + emoji.emojize(":information:")
                                + "   You can continue with other tasks while your files download"
                            )

                            time.sleep(wait)
                            break

                        except:
                            time.sleep(1)
                            print(
                                "\n"
                                + emoji.emojize(":red_exclamation_mark:")
                                + color.RED
                                + " Login was unsuccessful\n"
                                + color.END
                            )
                            x = main_menu()
                            if x == "1":
                                driver.close()
                                login_method = login()
                            elif x == "2":
                                os._exit(0)
                            continue

                    elif cont == "2":
                        x = main_menu()
                        if x == "1":
                            driver.close()
                            login_method = login()
                        elif x == "2":
                            os._exit(0)
                    else:
                        x = typo()
                        if x == "1":
                            driver.close()
                            login_method = login()
                        elif x == "2":
                            os._exit(0)

                elif cont == "2":
                    x = main_menu()
                    if x == "1":
                        driver.close()
                        login_method = login()
                    elif x == "2":
                        os._exit(0)
                else:
                    x = typo()
                    if x == "1":
                        driver.close()
                        login_method = login()
                    elif x == "2":
                        os._exit(0)

            else:
                x = typo()
                if x == "1":
                    driver.close()
                    login_method = login()
                elif x == "2":
                    os._exit(0)

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
            jstor_url,
            options(login_method, USER_AGENT, storage_directory),
            driver.command_executor._url,
            driver.session_id,
        )

        time.sleep(wait)

    # define the jstor landing page window

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

        driver.get(jstor_url + "stable/pdf/" + article + ".pdf")

        start_time = datetime.now().timestamp()

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

                    frames = driver.find_elements(By.TAG_NAME, "iframe")

                    time.sleep(wait)

                    # Find the reCAPTCHA checkbox
                    for index, frame in enumerate(frames):
                        if re.search("reCAPTCHA", frame.get_attribute("title")):

                            # driver.switch_to.window(win_2)

                            success, start_time = recaptcha_solver(
                                driver, url, url_pending, wait, src_directory
                            )

                            if success:

                                # print("solved")
                                continue

                            else:

                                # print(
                                #     "[ERR] reCAPTCHA could not be solved, restarting driver session"
                                # )
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

        # upload file to digital ocean
        # try:
        #     name = article.split("/")[0] + "." + article.split("/")[-1] + ".pdf"
        #     pdf_upload(doi, name)
        # except:
        #     print("[ERR] failed to upload file, retry")

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

    time.sleep(wait * 10)
