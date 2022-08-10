import time
import os

import emoji
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By


def login():

    login_method = input(
        color.PURPLE
        + "\n-- Type "
        + color.BOLD
        + "[1]"
        + color.END
        + color.PURPLE
        + " to login via VPN\n-- Type "
        + color.BOLD
        + "[2]"
        + color.END
        + color.PURPLE
        + " to manually login via the JSTOR website\n   : "
        + color.END
    )

    return login_method


def proceed():

    proceed = input(
        color.PURPLE
        + "\n-- Type "
        + color.BOLD
        + "[1]"
        + color.END
        + color.PURPLE
        + " to continue\n-- Type "
        + color.END
        + color.PURPLE
        + color.BOLD
        + "[2]"
        + color.END
        + color.PURPLE
        + " to restart\n   : "
        + color.END
    )

    return proceed


def welcome():
    print("\n" + color.BOLD + color.UNDERLINE + "Welcome to Aaron's Kit!" + color.END)
    print("\nSome words here about Aaron's Kit and what the tool does")
    print("\nSome words here about requirements to use the tool:")
    print(
        "\na) stable internet connection\nb) set computer to never sleep and keep on charge\nc) do not close the browser while program is running\nd) JSTOR login is required"
    )
    input(
        color.PURPLE
        + "\n-- Press "
        + color.BOLD
        + "ENTER/RETURN"
        + color.END
        + color.PURPLE
        + " to continue: "
        + color.END
    )


def main_menu():
    print(
        "\n"
        + emoji.emojize(":information:")
        + "   To Choose a login method, enter"
        + color.BOLD
        + " [1]"
        + color.END
    )

    print(
        "\n"
        + emoji.emojize(":information:")
        + "   To exit the program, enter"
        + color.BOLD
        + " [2]"
        + color.END
    )

    select = input(color.PURPLE + "\n-- Please enter your selection: " + color.END)

    return select


def typo():
    print(
        "\n"
        + emoji.emojize(":loudspeaker:")
        + color.YELLOW
        + "  It appears that you made a typo, you are being directed to the main selection menu"
        + color.END
    )

    time.sleep(1)

    main = main_menu()
    return main


class color:
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[95m"
    LIGHT_BLUE = "\033[1;34m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    ITALIC = "\x1B[3m"
    END = "\033[0m"
    LIGHT_GRAY = "\033[37m"
    DARK_GRAY = "\033[1;30m"


