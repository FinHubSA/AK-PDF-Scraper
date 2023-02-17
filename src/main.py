import os.path
import logging
import emoji
import os
import warnings
import multiprocessing

from termcolor import colored
from src.errors import MainException, TypoException

from src.helpers import typo
from src.download_papers import get_download_criteria_action
from src.contribute_papers import contribute_papers

logging.getLogger().setLevel(logging.CRITICAL)
warnings.filterwarnings("ignore", category=RuntimeWarning)


def welcome_message():

    print(colored("\n\nWelcome to Aaron's Kit!", attrs=["reverse"]))

    print(
        colored(
            "\n\nAaron's Kit is a tool that enables the effortless liberation of academic research.\n\nBy using this tool, you are playing an active role in the Open Access movement! \n\nThank you for your contribution.\n"
        )
    )


def main_menu_action():

    print("\n" + emoji.emojize(":information:") + "   Please make a selection below.")

    action = input(
        colored(
            "\n-- Type [1] to download papers"
            + "\n-- Type [2] to contribute papers"
            + "\n-- Type [3] to exit"
            + "\n   : ",
        )
    ).strip()

    try:
        process_main_menu_action(action)
    except (MainException, TypoException):
        main_menu_action()


def process_main_menu_action(action):

    if action == "1":
        get_download_criteria_action()
    elif action == "2":
        contribute_papers()
    elif action == "3":
        os._exit(0)
    else:
        typo()
        raise TypoException()


if __name__ == "__main__":

    # Add freeze support to make sure that the executable does not bug out when the program uses multiprocessing
    multiprocessing.freeze_support()

    welcome_message()

    main_menu_action()
