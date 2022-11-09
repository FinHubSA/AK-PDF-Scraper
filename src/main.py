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
            +"\n-- Type [2] to contribute papers"
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