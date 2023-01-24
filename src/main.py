import os.path
import logging
import emoji
import os
import warnings

from termcolor import colored

from src.helpers import system
from src.download_papers import download_papers
from src.contribute_papers import contribute_papers
from src.user_login import *

logging.getLogger().setLevel(logging.CRITICAL)
warnings.filterwarnings("ignore", category=RuntimeWarning)


def welcome():

    print(colored("\n\nWelcome to Aaron's Kit!", attrs=["reverse"]))

    print(
        colored(
            "\n\nAaron's Kit is a tool that enables the effortless liberation of academic research.\n\nBy using this tool, you are playing an active role in the Open Access movement! \n\nThank you for your contribution.\n"
        )
    )


def select_action():

    is_windows = system()

    print("\n" + emoji.emojize(":information:") + "   Please make a selection below")

    action = input(
        colored(
            "\n-- Type [1] to download papers"
            + "\n-- Type [2] to contribute papers"
            + "\n-- Type [3] to exit"
            + "\n   : ",
        )
    )

    if action == "1":
        download_papers()
    elif action == "2":
        contribute_papers()
    elif action == "3":
        os._exit(0)
    else:

        print(
            "\n\n"
            + (colored(" ! ", "yellow", attrs=["reverse"])) * (is_windows)
            + (emoji.emojize(":loudspeaker:")) * (not is_windows)
            + colored(
                "  It appears that you made a typo, please re-enter your selection.\n",
                "yellow",
            )
        )

        return select_action()


# welcome()

# select_action()
