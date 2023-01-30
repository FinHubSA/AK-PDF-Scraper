import requests
import urllib.parse
import time
import os
import platform
import emoji

from termcolor import colored


def system():

    system = platform.system()

    is_windows = False

    if system == "Windows":
        os.system("color")
        is_windows = True

    return is_windows


def typo():

    is_windows = system()

    print(
        "\n\n"
        + colored(" ? ", "yellow", attrs=["reverse"]) * (is_windows)
        + emoji.emojize(":loudspeaker:") * (not is_windows)
        + colored(
            "  It appears that you made a typo, please re-enter your selection.\n",
            "yellow",
        )
    )

    time.sleep(1)


def print_error():

    is_windows = system()

    # Error occured, try to check internet and try again.
    print(
        "\n"
        + colored(" ! ", "yellow", attrs=["reverse"]) * (is_windows)
        + emoji.emojize(":loudspeaker:") * (not is_windows)
        + colored(
            "   Something went wrong, you might have an unstable internet connection",
            "yellow",
        )
    )

    input(
        colored("\n\n-- Please check your connection and then press ")
        + colored("ENTER/RETURN", attrs=["reverse"]) * (is_windows)
        + colored("ENTER/RETURN", attrs=["bold"]) * (not is_windows)
        + colored(" to continue: ")
    )
