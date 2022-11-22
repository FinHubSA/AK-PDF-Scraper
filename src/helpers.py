import requests
import urllib.parse
import time
import platform
import emoji

from termcolor import colored

system = platform.system()

is_windows = False

if system == "Windows":
    is_windows = True

def select_author():
    global is_windows

    print(
        "\n"
        + (colored(" i ", attrs=["reverse"])) * (is_windows)
        + (emoji.emojize(":information:")) * (not is_windows)
        + "   You have chosen to search by Author Name.\n"
    )

    print(
        "\n"
        + colored("Please enter the Name and Surname of an Author (EXAMPLE: Rebecca Gould).\n","blue") * (is_windows)
        + colored("Please enter the Name and Surname of an Author (EXAMPLE: Rebecca Gould)\n", attrs=["bold"]) * (not is_windows)
    )

    author_search = True

    while author_search == True:

        Author_Name = input(
            colored(
                "\n-- Type Author Name and Surname\n   : ",
            )
        )

        Author_Name_urlenc = urllib.parse.quote(Author_Name)

        Author_List_json = requests.get(
            f"https://api-service-mrz6aygprq-oa.a.run.app/api/authors?authorName={Author_Name_urlenc}"
        )

        try:

            Author_List_json = Author_List_json.json()

        except:

            print(
                "\n\n"
                + (colored(" ! ", "yellow", attrs=["reverse"])) * (is_windows)
                + (emoji.emojize(":loudspeaker:")) * (not is_windows)
                + colored(
                    "   The requested Author could not be found.\n",
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
                        + (colored(" ! ", "yellow", attrs=["reverse"])) * (is_windows)
                        + (emoji.emojize(":loudspeaker:")) * (not is_windows)
                        + colored(
                            "   It appears that you made a typo, please re-enter your selection.\n",
                            "yellow",
                        )
                    )
            continue
        
        print(
            "\n\n"
            + (colored(
                "Please select an Author from the list below:\n",
                "blue",
            )) * (is_windows)
            + (colored(
                "Please select an Author from the list below:\n",
                attrs=["bold"],
            )) * (not is_windows)
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

            if int(Author_Number) not in list(range(1, 11)):

                print(
                    "\n\n"
                    + (colored(" ! ", "yellow", attrs=["reverse"])) * (is_windows)
                    + (emoji.emojize(":loudspeaker:")) * (not is_windows)
                    + colored(
                        "   It appears that you made a typo, please re-enter your selection.\n",
                        "yellow",
                    )
                )

            else:
                Author_Number_typo = False

        return Author_List_json[int(Author_Number) - 1]

def select_journal():
    global is_windows

    print(
        "\n"
        + (colored(" i ", attrs=["reverse"])) * (is_windows)
        + (emoji.emojize(":information:")) * (not is_windows)
        + "   You have chosen to search by Journal Name.\n"
    )

    print(
        "\n"
        + (colored(
            "Please enter the Name of a Journal (EXAMPLE: Journal of Financial Education).\n",
            "blue",
        )) * (is_windows)
        + (colored(
            "Please enter the Name of a Journal (EXAMPLE: Journal of Financial Education).\n",
            attrs=["bold"],
        )) * (not is_windows)
    )

    Journal_Name = input(
        colored(
            "\n-- Type Journal Name\n   : ",
        )
    )

    Journal_Name_urlenc = urllib.parse.quote(Journal_Name)

    Journal_List_json = requests.get(
        f"https://api-service-mrz6aygprq-oa.a.run.app/api/journals?journalName={Journal_Name_urlenc}"
    )

    try:

        Journal_List_json = Journal_List_json.json()

    except:

        if system == "Windows":
            print(
                "\n\n"
                + colored(" ! ", "yellow", attrs=["reverse"])
                + colored(
                    "   The requested Journal could not be found.\n",
                    "yellow",
                )
            )
        else:
            print(
                "\n\n"
                + emoji.emojize(":loudspeaker:")
                + colored(
                    "   The requested Journal could not be found.\n",
                    "yellow",
                )
            )

        return {}

    if system == "Windows":
        print(
            "\n\n"
            + (colored(" ! ", "yellow", attrs=["reverse"])) * (is_windows)
            + (emoji.emojize(":loudspeaker:")) * (not is_windows)
            + colored(
                "Please select a Journal from the list below:\n",
                "blue",
            )
        )

        return {}

    print(
        "\n\n"
        + (colored(
            "Please select a Journal from the list below:\n",
            "blue",
        )) * (is_windows)
        + (colored(
            "Please select a Journal from the list below:\n",
            attrs=["bold"],
        )) * (not is_windows)
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

        if int(Journal_Number) not in list(range(1, 11)):

            print(
                "\n\n"
                + (colored(" ! ", "yellow", attrs=["reverse"])) * (is_windows)
                + (emoji.emojize(":loudspeaker:")) * (not is_windows)
                + colored(
                    "   It appears that you made a typo, please re-enter your selection.\n",
                    "yellow",
                )
            )

        else:
            Journal_Number_typo = False

    return Journal_List_json[int(Journal_Number) - 1]


def select_issue(journal_id):
    global is_windows

    issue_list_json = requests.get(
        f"https://api-service-mrz6aygprq-oa.a.run.app/api/issues?journalID={journal_id}"
    )

    try:

        issue_list_json = issue_list_json.json()

    except:

        if system == "Windows":
            print(
                "\n\n"
                + colored(" ! ", "yellow", attrs=["reverse"])
                + colored(
                    "   The requested Journal could not be found.\n",
                    "yellow",
                )
            )
        else:
            print(
                "\n\n"
                + emoji.emojize(":loudspeaker:")
                + colored(
                    "   The requested Journal could not be found.\n",
                    "yellow",
                )
            )

        return {}

    if system == "windows":
        print(
            "\n\n"
            + (colored(" ! ", "yellow", attrs=["reverse"])) * (is_windows)
            + (emoji.emojize(":loudspeaker:")) * (not is_windows)
            + colored(
                "   The Journal has no contributed Issues. Please contribute to the repository.\n",
                "yellow",
            )
        )

        return {}

    print(
        "\n\n"
        + (colored(
            "Please select an Issue from the list below:\n",
            "blue",
        )) * (is_windows)
        + (colored(
            "Please select an Issue from the list below:\n",
            attrs=["bold"],
        )) * (not is_windows)
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

        if int(issue_number) not in list(range(1, issue_list_number)):

            print(
                "\n\n"
                + (colored(" ! ", "yellow", attrs=["reverse"])) * (is_windows)
                + (emoji.emojize(":loudspeaker:")) * (not is_windows)
                + colored(
                    "   It appears that you made a typo, please re-enter your selection.\n",
                    "yellow",
                )
            )

        else:
            issue_number_typo = False

    return issue_list_json[int(issue_number) - 1]