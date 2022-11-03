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
from contribute_papers import contribute_papers
from user_login import *

warnings.filterwarnings("ignore")
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

def welcome():

    print(colored("\n\nWelcome to Aaron's Kit!", attrs=["reverse"]))

    print(
        colored(
            "\n\nAaron's Kit is a tool that enables the effortless liberation of academic research.\n\nBy using this tool, you are playing an active role in the open access movement! \n\nThank you for your contribution.\n"
        )
    )

def select_action():

    action = input(
        colored(
            "\n-- Type [1] to download papers"
            +"\n-- Type [2] contribute papers"
            +"\n-- Type [3] to exit"
            +"\n   : ",
        )
    )

    if action == "1":
        download_papers()
    elif action == "2":
        contribute_papers()
    elif action == "3":
        os._exit(0)
    else:
        return select_action()

welcome()

select_action()