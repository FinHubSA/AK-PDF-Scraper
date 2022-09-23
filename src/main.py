import pickle
import time
import os.path
from datetime import datetime
import logging
import platform
import emoji
import os
import requests
import urllib.parse
import string
import random

from termcolor import colored
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

from recaptcha_solver import recaptcha_solver
from user_agent import user_agent
from user_login import *
from temp_storage import get_temp_storage_path, rename_file
from internet_speed import download_speed, delay

logging.getLogger().setLevel(logging.CRITICAL)


def latest_downloaded_pdf(storage_directory, src_directory):

    os.chdir(storage_directory)

    pdf_download_list = sorted(os.listdir(storage_directory), key=os.path.getmtime)

    latest_pdf = pdf_download_list[-1]

    os.chdir(src_directory)

    return latest_pdf


def create_driver_session(chrome_options):

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
    # chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
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


# Defining directories and setting up the system variable
storage_directory = get_temp_storage_path()

src_directory = os.path.dirname(__file__)

misc_directory = os.path.normpath(src_directory + os.sep + os.pardir)

system = platform.system()

if system == "Windows":
    os.system("color")

# To create an executable file we need to set the file source directory
os.chdir(src_directory)

# Aaron's Kit welcome
welcome(system)

# Calculate the internet speed and driver sleep time
internet_retry = True

while internet_retry == True:
    print("\n\n...determining internet speed")

    mbps = download_speed()

    time.sleep(2)

    if mbps == "Error":

        if system == "Windows":

            print(
                "\n\n"
                + colored(" ! ", "yellow", attrs=["reverse"])
                + colored(
                    "   It seems that your internet speed is unstable at the moment.",
                    "yellow",
                )
            )

            print(
                "\n\n"
                + colored(" i ", "blue", attrs=["reverse"])
                + "   Please check your internet connection, and then make a selection."
            )

            print(
                "\n"
                + colored(" i ", "blue", attrs=["reverse"])
                + "   Note that an unstable internet connection might interfere with the download process."
            )

            internet_typo = True

            while internet_typo:
                internet_option = input(
                    colored(
                        "\n-- Type [1] to retry speed check\n-- Type [2] to continue with an unstable connection\n   : "
                    )
                )

                if internet_option == "1":
                    internet_typo = False
                elif internet_option == "2":
                    mbps = 15
                    internet_typo = False
                    internet_retry = False
                else:
                    print(
                        "\n\n"
                        + colored(" ? ", "yellow", attrs=["reverse"])
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
                    "   It seems that your internet speed is unstable at the moment.",
                    "yellow",
                )
            )

            print(
                "\n\n"
                + emoji.emojize(":information:")
                + "   Please check your internet connection, and then make a selection."
            )

            print(
                "\n"
                + emoji.emojize(":information:")
                + "   Note that an unstable internet connection might interfere with the download process."
            )

            internet_typo = True

            while internet_typo == True:
                internet_option = input(
                    colored(
                        "\n-- Type [1] to retry speed check\n-- Type [2] to continue with an unstable connection\n   : "
                    )
                )

                if internet_option == "1":
                    internet_typo = False
                elif internet_option == "2":
                    mbps = 15
                    internet_typo = False
                    internet_retry = False
                else:
                    print(
                        "\n\n"
                        + emoji.emojize(":loudspeaker:")
                        + colored(
                            "   It appears that you made a typo, please re-enter your selection.\n",
                            "yellow",
                        )
                    )

    elif mbps <= 5:

        if system == "Windows":

            print(
                "\n\n"
                + colored(" ! ", "yellow", attrs=["reverse"])
                + colored("   Your internet speed is less than 5 mbps.", "yellow")
            )

            print(
                "\n\n"
                + colored(" i ", "blue", attrs=["reverse"])
                + "   Please check your internet connection, and then make a selection"
            )

            print(
                "\n"
                + colored(" i ", "blue", attrs=["reverse"])
                + "   Note that a slow internet connection might interfere with the download process."
            )

            internet_typo = True

            while internet_typo:
                internet_option = input(
                    colored(
                        "\n-- Type [1] to retry speed check\n-- Type [2] to continue with a slow connection\n   : "
                    )
                )

                if internet_option == "1":
                    internet_typo = False
                elif internet_option == "2":
                    mbps = 15
                    internet_typo = False
                    internet_retry = False
                else:
                    print(
                        "\n\n"
                        + colored(" ? ", "yellow", attrs=["reverse"])
                        + colored(
                            "   It appears that you made a typo, please re-enter your selection.\n",
                            "yellow",
                        )
                    )

        else:
            print(
                "\n\n"
                + emoji.emojize(":loudspeaker:")
                + colored("   Your internet speed is less than 5 mbps.", "yellow")
            )

            print(
                "\n\n"
                + emoji.emojize(":information:")
                + "   Please check your internet connection, and then make a selection"
            )

            print(
                "\n"
                + emoji.emojize(":information:")
                + "   Note that a slow internet connection might interfere with the download process."
            )

            internet_typo = True

            while internet_typo == True:
                internet_option = input(
                    colored(
                        "\n-- Type [1] to retry speed check\n-- Type [2] to continue with a slow connection\n   : "
                    )
                )

                if internet_option == "1":
                    internet_typo = False
                elif internet_option == "2":
                    mbps = 15
                    internet_typo = False
                    internet_retry = False
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
        if system == "Windows":
            print(
                "\n\n"
                + colored(" ! ", "green", attrs=["reverse"])
                + colored(
                    "   Your internet speed is: " + str(round(mbps, 2)) + " mbps",
                    "green",
                )
            )
        else:
            print(
                "\n\n"
                + emoji.emojize(":check_mark_button:")
                + colored(
                    "   Your internet speed is: " + str(round(mbps, 2)) + " mbps",
                    "green",
                )
            )

        internet_retry = False

wait = delay(mbps)

# def User Agent
print("\n\n...determining User Agent")

USER_AGENT = user_agent(system)

if system == "Windows":
    print(
        "\n"
        + colored(" ! ", "green", attrs=["reverse"])
        + colored(
            "   User Agent found",
            "green",
        )
    )
else:
    print(
        "\n"
        + emoji.emojize(":check_mark_button:")
        + colored(
            "   User Agent found",
            "green",
        )
    )


now = datetime.now().timestamp()

restart_count = 0

jstor_url = None

while True:

    # User will login when program starts
    # after each restart, reload the web session
    if restart_count == 0:

        login_method = vpn_or_manual(system)

        while True:
            if login_method == "1":

                # Start the driver session
                driver = create_driver_session(
                    options(login_method, USER_AGENT, storage_directory)
                )

                time.sleep(1)

                if system == "Windows":

                    print(
                        "\n"
                        + colored(" i ", "blue", attrs=["reverse"])
                        + "   You have chosen to login via VPN/wifi."
                    )

                    # "\n[INFO] Follow the instructions below"
                    time.sleep(1)

                    print(
                        "\n"
                        + colored(" i ", "blue", attrs=["reverse"])
                        + "   Follow the steps below:"
                    )

                    time.sleep(1)

                    print(
                        colored(
                            "\n\nStep 1/1: Please connect to your institution's VPN or wifi, then continue.\n",
                            "blue",
                        )
                    )

                    time.sleep(1)

                    cont = proceed()

                    if cont == "1":

                        print("\n...you are now being routed to JSTOR home page")

                        time.sleep(2)

                        print(
                            "\n...give it a second, we are checking if the page has loaded successfully"
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
                                + colored(" ! ", "red", attrs=["reverse"])
                                + colored(" Unable to load JSTOR page.\n", "red")
                            )

                            print(
                                "\n"
                                + colored(" i ", "blue", attrs=["reverse"])
                                + "  Check your internet connection and try again.\n"
                            )

                            driver.close()
                            login_method = login()

                        print("\n...checking for successful login\n")

                        time.sleep(2)

                        try:
                            driver.find_element(
                                By.CLASS_NAME, "pds__access-provided-by"
                            )

                            time.sleep(1)

                            print(
                                "\n"
                                + colored(" ! ", "green", attrs=["reverse"])
                                + colored("  Login was successful!\n", "green")
                            )

                            time.sleep(1)

                            driver.maximize_window()

                            break

                        except:

                            time.sleep(1)

                            print(
                                "\n"
                                + colored(" ! ", "red", attrs=["reverse"])
                                + colored("  Login was unsuccessful\n", "red")
                            )

                            x = main_menu(system)

                            if x == "1":
                                driver.close()
                                login_method = login()
                            elif x == "2":
                                os._exit(0)
                            continue

                    elif cont == "2":

                        x = main_menu(system)
                        if x == "1":
                            driver.close()
                            login_method = login()
                        elif x == "2":
                            os._exit(0)
                    else:

                        x = typo(system)
                        if x == "1":
                            driver.close()
                            login_method = login()
                        elif x == "2":
                            os._exit(0)

                else:
                    print(
                        "\n"
                        + emoji.emojize(":information:")
                        + "   You have chosen to login via VPN/wifi."
                    )

                    # "\n[INFO] Follow the instructions below"
                    time.sleep(1)

                    print(
                        "\n"
                        + emoji.emojize(":information:")
                        + "   Follow the steps below:"
                    )

                    time.sleep(1)

                    print(
                        colored(
                            "\n\nStep 1/1: Please connect to your institution's VPN or wifi, then continue.\n",
                            attrs=["bold"],
                        )
                    )

                    time.sleep(1)

                    cont = proceed()

                    if cont == "1":

                        print("\n...you are now being routed to JSTOR home page")

                        time.sleep(2)

                        print(
                            "\n...give it a second, we are checking if the page has loaded successfully"
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
                                + colored(" Unable to load JSTOR page.\n", "red")
                            )

                            print(
                                "\n"
                                + emoji.emojize(":information:")
                                + "  Check your internet connection and try again.\n"
                            )

                            driver.close()
                            login_method = login()

                        print("\n...checking for successful login\n")

                        time.sleep(2)

                        try:
                            driver.find_element(
                                By.CLASS_NAME, "pds__access-provided-by"
                            )

                            time.sleep(1)

                            print(
                                "\n"
                                + emoji.emojize(":check_mark_button:")
                                + colored("  Login was successful!\n", "green")
                            )

                            time.sleep(1)

                            driver.maximize_window()

                            break

                        except:
                            time.sleep(1)
                            print(
                                "\n"
                                + emoji.emojize(":red_exclamation_mark:")
                                + colored("  Login was unsuccessful\n", "red")
                            )

                            x = main_menu(system)

                            if x == "1":
                                driver.close()
                                login_method = login()
                            elif x == "2":
                                os._exit(0)
                            continue

                    elif cont == "2":

                        x = main_menu(system)
                        if x == "1":
                            driver.close()
                            login_method = login()
                        elif x == "2":
                            os._exit(0)

                    else:

                        x = typo(system)
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

                if system == "Windows":

                    print(
                        "\n"
                        + colored(" i ", "blue", attrs=["reverse"])
                        + "   You will be prompted to manually login via the JSTOR website."
                    )

                    time.sleep(1)

                    cont = proceed()

                    if cont == "1":

                        print("\n...you are now being routed to JSTOR home page")

                        time.sleep(2)

                        print(
                            "\n...sit tight and wait for Google Chrome to open on your screen\n"
                        )

                        time.sleep(2)

                        print(
                            "\n"
                            + colored(" i ", "blue", attrs=["reverse"])
                            + "   While the browser opens, read through the login steps:"
                        )

                        time.sleep(1)

                        print(
                            colored(
                                "\nStep 1/4: Navigate to the top of the JSTOR home page, and click on the link: ",
                                "blue",
                            )
                            + colored(
                                "Log in through your library.",
                                "blue",
                                attrs=["reverse"],
                            )
                            + colored(
                                "\nStep 2/4: Search for your institution by using the search box.\nStep 3/4: Log in using your institution's login credentials.\nStep 4/4: Accept the cookies.",
                                "blue",
                            )
                        )

                        time.sleep(1)

                        print(
                            "\n...give it a second, we are checking if the page has loaded successfully\n"
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
                                + colored(" ! ", "red", attrs=["reverse"])
                                + colored(" Unable to load JSTOR page.\n", "red")
                            )

                            print(
                                "\n"
                                + colored(" i ", "blue", attrs=["reverse"])
                                + "  Check your internet connection and try again.\n"
                            )

                            driver.close()
                            login_method = login()

                        driver.maximize_window()

                        print(
                            "\n"
                            + colored(" i ", "blue", attrs=["reverse"])
                            + "   Once you have completed the steps, continue:"
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
                                    "\n"
                                    + colored(" ! ", "red", attrs=["reverse"])
                                    + colored(" Unable to load JSTOR page.\n", "red")
                                )

                            print("\n...checking for successful login\n")

                            time.sleep(1)

                            try:
                                driver.find_element(
                                    By.CLASS_NAME, "pds__access-provided-by"
                                )
                                time.sleep(1)
                                print(
                                    "\n"
                                    + colored(" ! ", "green", attrs=["reverse"])
                                    + colored("  Login was successful!\n", "green")
                                )

                                time.sleep(1)

                                driver.maximize_window()

                                driver.set_window_position(-2024, 2024)

                                break

                            except:
                                time.sleep(1)
                                print(
                                    "\n"
                                    + colored(" ! ", "red", attrs=["reverse"])
                                    + colored(" Login was unsuccessful\n", "red")
                                )

                                x = main_menu(system)
                                if x == "1":
                                    driver.close()
                                    login_method = login()
                                elif x == "2":
                                    os._exit(0)
                                continue

                        elif cont == "2":
                            x = main_menu(system)
                            if x == "1":
                                driver.close()
                                login_method = login()
                            elif x == "2":
                                os._exit(0)
                        else:
                            x = typo(system)
                            if x == "1":
                                driver.close()
                                login_method = login()
                            elif x == "2":
                                os._exit(0)

                    elif cont == "2":
                        x = main_menu(system)
                        if x == "1":
                            driver.close()
                            login_method = login()
                        elif x == "2":
                            os._exit(0)
                    else:
                        x = typo(system)
                        if x == "1":
                            driver.close()
                            login_method = login()
                        elif x == "2":
                            os._exit(0)

                else:

                    print(
                        "\n"
                        + emoji.emojize(":information:")
                        + "   You will be prompted to manually login via the JSTOR website."
                    )

                    time.sleep(1)

                    cont = proceed()

                    if cont == "1":

                        print("\n...you are now being routed to JSTOR home page")

                        time.sleep(2)

                        print(
                            "\n...sit tight and wait for Google Chrome to open on your screen\n"
                        )

                        time.sleep(2)

                        print(
                            "\n"
                            + emoji.emojize(":information:")
                            + "   While the browser opens, read through the login steps:"
                        )

                        time.sleep(1)

                        print(
                            colored(
                                "\nStep 1/4: Navigate to the top of the JSTOR home page, and click on the link: ",
                                attrs=["bold"],
                            )
                            + colored(
                                "Log in through your library.", attrs=["underline"]
                            )
                            + colored(
                                "\nStep 2/4: Search for your institution by using the search box.\nStep 3/4: Log in using your institution's login credentials.\nStep 4/4: Accept the cookies.",
                                attrs=["bold"],
                            )
                        )

                        time.sleep(1)

                        print(
                            "\n...give it a second, we are checking if the page has loaded successfully\n"
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
                                + colored(" Unable to load JSTOR page.\n", "red")
                            )

                            print(
                                "\n"
                                + emoji.emojize(":information:")
                                + "  Check your internet connection and try again.\n"
                            )

                            driver.close()
                            login_method = login()

                        driver.maximize_window()

                        print(
                            "\n"
                            + emoji.emojize(":information:")
                            + "   Once you have completed the steps, continue:"
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
                                    "\n"
                                    + emoji.emojize(":red_exclamation_mark:")
                                    + colored(" Unable to load JSTOR page.\n", "red")
                                )

                            print("\n...checking for successful login\n")

                            time.sleep(1)

                            try:
                                driver.find_element(
                                    By.CLASS_NAME, "pds__access-provided-by"
                                )
                                time.sleep(1)
                                print(
                                    "\n"
                                    + emoji.emojize(":check_mark_button:")
                                    + colored("  Login was successful!\n", "green")
                                )

                                time.sleep(1)

                                driver.maximize_window()

                                driver.set_window_position(-2024, 2024)

                                print(
                                    "\n"
                                    + emoji.emojize(":information:")
                                    + "   Login process complete, the browser will run in the background."
                                )

                                break

                            except:
                                time.sleep(1)
                                print(
                                    "\n"
                                    + emoji.emojize(":red_exclamation_mark:")
                                    + colored(" Login was unsuccessful\n", "red")
                                )

                                x = main_menu(system)
                                if x == "1":
                                    driver.close()
                                    login_method = login()
                                elif x == "2":
                                    os._exit(0)
                                continue

                        elif cont == "2":
                            x = main_menu(system)
                            if x == "1":
                                driver.close()
                                login_method = login()
                            elif x == "2":
                                os._exit(0)
                        else:
                            x = typo(system)
                            if x == "1":
                                driver.close()
                                login_method = login()
                            elif x == "2":
                                os._exit(0)

                    elif cont == "2":
                        x = main_menu(system)
                        if x == "1":
                            driver.close()
                            login_method = login()
                        elif x == "2":
                            os._exit(0)
                    else:
                        x = typo(system)
                        if x == "1":
                            driver.close()
                            login_method = login()
                        elif x == "2":
                            os._exit(0)

            else:
                x = typo(system)
                if x == "1":
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
                            "Please enter the Name and Surname of an Author (EXAMPLE: Aaron Swartz).\n",
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

                        try:

                            Author_List_json = requests.get(
                                f"https://api-service-mrz6aygprq-oa.a.run.app/api/authors?authorName={Author_Name_urlenc}&format=json"
                            ).json()

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

                                if int(Author_Number) > 10:

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

                            try:

                                Article_ID_list = requests.get(
                                    f"https://api-service-mrz6aygprq-oa.a.run.app/api/articles?authorName={Author_Selected_urlenc}&format=json&scraping=1"
                                ).json()

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

                            except:

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

                        except:

                            print(
                                "\n"
                                + colored(" ! ", "yellow", attrs=["reverse"])
                                + colored(
                                    "   The requested Author could not be found.",
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
                                        + colored(" ! ", "yellow", attrs=["reverse"])
                                        + colored(
                                            "   It appears that you made a typo, please re-enter your selection.\n",
                                            "yellow",
                                        )
                                    )

                elif search_criteria == "2":

                    print(
                        "\n"
                        + colored(" i ", "blue", attrs=["reverse"])
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

                        try:

                            Journal_List_json = requests.get(
                                f"https://api-service-mrz6aygprq-oa.a.run.app/api/journals?journalName={Journal_Name_urlenc}&format=json"
                            ).json()

                            print(
                                "\n\n"
                                + colored(
                                    "Please select an Journal from the list below:\n",
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

                                if int(Journal_Number) > 10:

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

                            try:

                                Article_ID_list = requests.get(
                                    f"https://api-service-mrz6aygprq-oa.a.run.app/api/articles?journalName={Journal_Selected_urlenc}&format=json&scraping=1"
                                ).json()

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

                            except:

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

                        except:

                            print(
                                "\n"
                                + colored(" ! ", "yellow", attrs=["reverse"])
                                + colored(
                                    "   The requested Journal could not be found.",
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
                                        + colored(" ! ", "yellow", attrs=["reverse"])
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
                + "   Do not exit/close this window as this will abort the download process."
            )

            time.sleep(1)

        else:

            print(
                "\n\n"
                + colored(
                    "JSTOR PDF download specification:\n", attrs=["bold", "underline"]
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
                            "Please enter the Name and Surname of an Author (EXAMPLE: Aaron Swartz).\n",
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

                        try:

                            Author_List_json = requests.get(
                                f"https://api-service-mrz6aygprq-oa.a.run.app/api/authors?authorName={Author_Name_urlenc}&format=json"
                            ).json()

                            print(
                                "\n\n"
                                + colored(
                                    "Please select an Author from the list below:\n",
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

                                if int(Author_Number) > 10:

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

                            try:

                                Article_ID_list = requests.get(
                                    f"https://api-service-mrz6aygprq-oa.a.run.app/api/articles?authorName={Author_Selected_urlenc}&format=json&scraping=1"
                                ).json()

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

                            except:

                                print(
                                    "\n\n"
                                    + emoji.emojize(":red_exclamation_mark:")
                                    + colored(
                                        "   An Unexpected error has occured.\n",
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

                        except:

                            print(
                                "\n"
                                + emoji.emojize(":loudspeaker:")
                                + colored(
                                    "   The requested Author could not be found.",
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

                        try:

                            Journal_List_json = requests.get(
                                f"https://api-service-mrz6aygprq-oa.a.run.app/api/journals?journalName={Journal_Name_urlenc}&format=json"
                            ).json()

                            print(
                                "\n\n"
                                + colored(
                                    "Please select an Journal from the list below:\n",
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

                                if int(Journal_Number) > 10:

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

                            try:

                                Article_ID_list = requests.get(
                                    f"https://api-service-mrz6aygprq-oa.a.run.app/api/articles?journalName={Journal_Selected_urlenc}&format=json&scraping=1"
                                ).json()

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

                            except:

                                # Add option to download articles by this author
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

                        except:

                            print(
                                "\n"
                                + emoji.emojize(":loudspeaker:")
                                + colored(
                                    "   The requested Journal could not be found.",
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
                + "   Do not exit/close this window as this will abort the download process."
            )

            time.sleep(1)

    else:

        restart_driver_session(
            jstor_url,
            options(login_method, USER_AGENT, storage_directory),
            driver.command_executor._url,
            driver.session_id,
        )

        time.sleep(wait)

        Article_ID_list = Article_ID_list[article_index:]

    restart = False

    t_c_accepted = False

    t_c_try_accept = 0

    # Loop through article ID's
    for index, article_json in enumerate(Article_ID_list):

        print(Article_ID_list)
        article = article_json["articleJstorID"]
        print(article)

        # Calculate the waiting time every 30 mins to adjust wait according to user internet speed
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

        s = string.ascii_lowercase + string.digits

        doi = os.path.join(
            storage_directory,
            article.split("/")[0]
            + "-"
            + article.split("/")[-1]
            + "-"
            + "".join(random.sample(s, 12))
            + ".pdf",
        )

        # Check if pdf file already exists in user directory
        # Delete if download pending or file exist to circumvent malicious actors
        if os.path.exists(url):

            os.remove(url)

            # rename_file(url, doi)

            # continue

        elif os.path.exists(url_pending):

            os.remove(url_pending)

        driver.get(jstor_url + "stable/pdf/" + article + ".pdf")

        start_time = datetime.now().timestamp()

        # Check for cookies, t&c's and reCAPTCHA
        # The t&c's only pop up each time you restart the browser session

        while not t_c_accepted and t_c_try_accept <= 3:

            t_c_try_accept += 1

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

            restart_count = +1

            break

        time.sleep(wait)

        # Check for reCAPTCHA

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

        # Upload pdf file to Google Drive
        files = {"file": open(doi, "rb")}
        data = {"articleJstorID": article}
        response = requests.post(
            "https://api-service-mrz6aygprq-oa.a.run.app/api/articles/pdf",
            files=files,
            data=data,
            verify=False,
        )

        # Navigate to home page
        driver.get(jstor_url)

        if article_json == Article_ID_list[-1]:

            if system == "Windows":

                print(
                    "\n"
                    + colored(" ! ", "green", attrs=["reverse"])
                    + colored(
                        "   You have successfully uploaded your requested papers they can also be found here: "
                        + storage_directory,
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
                        "   You have successfully uploaded your requested papers they can also be found here: "
                        + storage_directory
                        + ".",
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

        else:
            continue

    if article_json == Article_ID_list[-1] and not restart:
        driver.close()
        break
    else:
        driver.get(jstor_url)

    article_index = index
    time.sleep(wait * 10)
