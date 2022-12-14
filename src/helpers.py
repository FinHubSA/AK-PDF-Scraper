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
    # is_windows = True

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


def select_author():

    is_windows = system()

    print(
        "\n"
        + (colored(" i ", attrs=["reverse"])) * (is_windows)
        + (emoji.emojize(":information:")) * (not is_windows)
        + "   You have chosen to search by Author Name.\n"
    )

    print(
        "\n"
        + colored(
            "Please enter the Name and Surname of an Author (EXAMPLE: Rebecca Gould).",
            "blue",
        )
        * (is_windows)
        + colored(
            "Please enter the Name and Surname of an Author (EXAMPLE: Rebecca Gould).",
            attrs=["bold"],
        )
        * (not is_windows)
    )

    author_search = True

    while author_search == True:

        Author_Name = input(
            colored(
                "\n-- Type Author Name and Surname\n   : ",
            )
        )

        Author_Name_urlenc = urllib.parse.quote(Author_Name.strip())

        try:

            Author_List_json = requests.get(
                f"https://api-service-mrz6aygprq-oa.a.run.app/api/authors?authorName={Author_Name_urlenc}"
            )

        except:

            print_error()

            return select_author()

        try:

            Author_List_json = Author_List_json.json()

        except:

            return {}

        print(
            "\n\n"
            + (
                colored(
                    "Please select an Author from the list below:\n",
                    "blue",
                )
            )
            * (is_windows)
            + (
                colored(
                    "Please select an Author from the list below:\n",
                    attrs=["bold"],
                )
            )
            * (not is_windows)
        )

        time.sleep(1)

        author_list_number = 0

        for Author_Name in Author_List_json:

            author_list_number += 1

            print("[" + str(author_list_number) + "] " + Author_Name["authorName"])

        Author_Number_typo = True

        while Author_Number_typo == True:

            Author_Number = input(
                colored(
                    "\n\n-- Type the Number of the Author\n   : ",
                )
            )

            if Author_Number.strip() not in [str(x) for x in list(range(1, 11))]:

                print(
                    "\n\n"
                    + (colored(" ! ", "yellow", attrs=["reverse"])) * (is_windows)
                    + (emoji.emojize(":loudspeaker:")) * (not is_windows)
                    + colored(
                        "  It appears that you made a typo, please re-enter your selection.",
                        "yellow",
                    )
                )

            else:
                Author_Number_typo = False

        return Author_List_json[int(Author_Number) - 1]


def select_journal():

    is_windows = system()

    print(
        "\n"
        + (colored(" i ", attrs=["reverse"])) * (is_windows)
        + (emoji.emojize(":information:")) * (not is_windows)
        + "   You have chosen to search by Journal Name.\n"
    )

    print(
        "\n"
        + (
            colored(
                "Please enter the Name of a Journal (EXAMPLE: Journal of Financial Education).\n",
                "blue",
            )
        )
        * (is_windows)
        + (
            colored(
                "Please enter the Name of a Journal (EXAMPLE: Journal of Financial Education).\n",
                attrs=["bold"],
            )
        )
        * (not is_windows)
    )

    Journal_Name = input(
        colored(
            "-- Type Journal Name\n   : ",
        )
    )

    Journal_Name_urlenc = urllib.parse.quote(Journal_Name)

    try:

        Journal_List_json = requests.get(
            f"https://api-service-mrz6aygprq-oa.a.run.app/api/journals?journalName={Journal_Name_urlenc}"
        )

    except:

        print_error()

        return select_journal()

    try:

        Journal_List_json = Journal_List_json.json()

    except:

        return {}

    print(
        "\n\n"
        + (
            colored(
                "Please select a Journal from the list below:\n",
                "blue",
            )
        )
        * (is_windows)
        + (
            colored(
                "Please select a Journal from the list below:\n",
                attrs=["bold"],
            )
        )
        * (not is_windows)
    )

    time.sleep(1)

    journal_list_number = 0

    for Journal_Name in Journal_List_json:

        journal_list_number += 1

        print("[" + str(journal_list_number) + "] " + Journal_Name["journalName"])

    Journal_Number_typo = True

    while Journal_Number_typo == True:

        Journal_Number = input(
            colored(
                "\n\n-- Type the Number of the Journal\n   : ",
            )
        )

        if Journal_Number.strip() not in [
            str(x) for x in list(range(1, journal_list_number + 1))
        ]:

            print(
                "\n\n"
                + (colored(" ! ", "yellow", attrs=["reverse"])) * (is_windows)
                + (emoji.emojize(":loudspeaker:")) * (not is_windows)
                + colored(
                    "  It appears that you made a typo, please re-enter your selection.",
                    "yellow",
                )
            )

        else:

            Journal_Number_typo = False

    return Journal_List_json[int(Journal_Number) - 1]


def select_issue(journal_name, journal_id):

    is_windows = system()

    print("\n\nSearching for issues in " + journal_name + "...")

    try:

        issue_list_json = requests.get(
            f"https://api-service-mrz6aygprq-oa.a.run.app/api/issues?journalID={journal_id}"
        )

    except:

        print_error()

        return select_issue(journal_id)

    try:

        issue_list_json = issue_list_json.json()

    except:

        return {}

    print(
        "\n\n"
        + (
            colored(
                "Please select an Issue from the list below:\n",
                "blue",
            )
        )
        * (is_windows)
        + (
            colored(
                "Please select an Issue from the list below:\n",
                attrs=["bold"],
            )
        )
        * (not is_windows)
    )

    time.sleep(1)

    issue_list_number = 0

    for issue in issue_list_json:

        issue_list_number += 1

        print(
            "["
            + str(issue_list_number)
            + "] "
            + "Vol. "
            + str(issue["volume"])
            + ", "
            + "No. "
            + str(issue["number"])
            + ", "
            + "Year. "
            + str(issue["year"])
        )

    issue_number_typo = True

    while issue_number_typo == True:

        issue_number = input(
            colored(
                "\n\n-- Type the Number of the Issue\n   : ",
            )
        )

        if issue_number.strip() not in [
            str(x) for x in list(range(1, issue_list_number + 1))
        ]:

            print(
                "\n\n"
                + (colored(" ! ", "yellow", attrs=["reverse"])) * (is_windows)
                + (emoji.emojize(":loudspeaker:")) * (not is_windows)
                + colored(
                    "  It appears that you made a typo, please re-enter your selection.",
                    "yellow",
                )
            )

        else:

            issue_number_typo = False

    return issue_list_json[int(issue_number) - 1]
