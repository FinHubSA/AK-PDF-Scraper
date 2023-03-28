from termcolor import colored
import emoji
import time
import urllib
import os

from src.helpers import system, server_response_request, print_typo
from src.errors import MainException, TypoException


is_windows = system()


def receive_upload_criteria_action(driver):

    print(
        "\n"
        + colored(" i ", "blue", attrs=["reverse"]) * (is_windows)
        + emoji.emojize(":information:") * (not is_windows)
        + "   Please select your search criteria."
    )

    search_criteria = get_input(
        colored(
            "\n-- Type [1] to search by Journal Name\n-- Type [2] to search by Author Name\n   : ",
        )
    )

    try:
        return process_upload_criteria_action(driver, search_criteria)
    except TypoException:
        return receive_upload_criteria_action(driver)


def process_upload_criteria_action(driver, search_criteria):

    if search_criteria == "1":

        Article_ID_list = request_journal_upload(driver)

        if Article_ID_list == []:
            return receive_retry_search_action(driver, search_criteria, "Journal")
        else:
            print_pdf_found()
            return Article_ID_list

    elif search_criteria == "2":

        Article_ID_list = request_author_upload(driver)

        if Article_ID_list == []:
            return receive_retry_search_action(driver, search_criteria, "Author")
        else:
            print_pdf_found()
            return Article_ID_list

    else:
        print_typo()
        raise TypoException


def request_author_upload(driver):

    print(
        "\n"
        + colored(" i ", "blue", attrs=["reverse"]) * (is_windows)
        + emoji.emojize(":information:") * (not is_windows)
        + "   You have chosen to search by Author Name.\n"
    )

    print(
        colored(
            "\nPlease enter the Name and Surname of an author (EXAMPLE: Rebecca Gould)\n",
            attrs=["bold"],
        )
    )

    Author_Name = get_input(
        colored(
            "\n-- Type Author Name and Surname\n   : ",
        )
    )

    print("\nGive it a second, we are searching for the requested author.")

    time.sleep(1)

    server_error, Author_List_json = server_response_request(
        f"https://api-service-mrz6aygprq-oa.a.run.app/api/authors?authorName={urllib.parse.quote(Author_Name)}",
    )

    if server_error:
        print(
            "\n"
            + (colored(" i ", "red", attrs=["reverse"])) * (is_windows)
            + (emoji.emojize(":red_exclamation_mark:")) * (not is_windows)
            + colored(f"  A server error occured, try again later.", "red")
        )
        driver.close()
        os._exit(0)

    try:
        Author_List_json = Author_List_json.json()
        return receive_author_selection_action(driver, Author_List_json)

    except:

        print(
            "\n\n"
            + colored(" ! ", "yellow", attrs=["reverse"]) * (is_windows)
            + emoji.emojize(":loudspeaker:") * (not is_windows)
            + colored(
                "  The requested author could not be found.\n",
                "yellow",
            )
        )

        return []


def receive_author_selection_action(driver, Author_List_json):

    print(
        colored(
            "\n\nPlease select an author from the list below:\n",
            attrs=["bold"],
        )
    )

    time.sleep(1)

    author_list_number = 0

    for Author_Name in Author_List_json:

        author_list_number += 1

        print("[" + str(author_list_number) + "] " + Author_Name["authorName"])

    Author_Number = get_input(
        colored(
            "\n\n-- Type the number of the author\n   : ",
        )
    )

    try:
        return process_author_selection_action(driver, Author_Number, Author_List_json)
    except TypoException:
        return receive_author_selection_action(driver, Author_List_json)


def process_author_selection_action(driver, Author_Number, Author_List_json):

    if Author_Number in [str(x) for x in list(range(1, 11))]:

        Author_Selected_urlenc = urllib.parse.quote(
            Author_List_json[int(Author_Number) - 1]["authorName"]
        )

        server_error, Article_ID_list = server_response_request(
            f"https://api-service-mrz6aygprq-oa.a.run.app/api/articles?authorName={Author_Selected_urlenc}&scraped=0&exact=1",
        )

        if server_error:
            print(
                "\n"
                + (colored(" i ", "red", attrs=["reverse"])) * (is_windows)
                + (emoji.emojize(":red_exclamation_mark:")) * (not is_windows)
                + colored(f"  A server error occured, try again later.", "red")
            )
            driver.close()
            os._exit(0)

        if Article_ID_list.status_code == 200:

            Article_ID_list = Article_ID_list.json()

            Article_list_num = len(Article_ID_list)

            if Article_list_num > 0:

                print(
                    "\n"
                    + colored(" ! ", "green", attrs=["reverse"]) * (is_windows)
                    + emoji.emojize(":check_mark_button:") * (not is_windows)
                    + colored(
                        f"   {Article_list_num} articles from selected author found.\n",
                        "green",
                    )
                )

                return Article_ID_list

            else:

                print(
                    "\n\n"
                    + colored(" ! ", "yellow", attrs=["reverse"]) * (is_windows)
                    + emoji.emojize(":loudspeaker:") * (not is_windows)
                    + colored(
                        "  It appears that all articles by this author are already available.\n",
                        "yellow",
                    )
                )

                return []

        else:

            print(
                "\n\n"
                + colored(" ! ", "red", attrs=["reverse"]) * (is_windows)
                + emoji.emojize(":red_exclamation_mark:") * (not is_windows)
                + colored(
                    "   An unexpected error occured.\n",
                    "red",
                )
            )

            return []

    else:
        print_typo()
        raise TypoException


def request_journal_upload(driver):

    print(
        "\n"
        + colored(" i ", "blue", attrs=["reverse"]) * (is_windows)
        + emoji.emojize(":information:") * (not is_windows)
        + "   You have chosen to search by Journal Name.\n"
    )

    print(
        colored(
            "\nPlease enter the Name of a journal (EXAMPLE: Journal of Financial Education).\n",
            attrs=["bold"],
        )
    )

    Journal_Name = get_input(
        colored(
            "\n-- Type Journal Name\n   : ",
        )
    )

    print("\nGive it a second, we are searching for the requested journal.")

    time.sleep(1)

    server_error, Journal_List_json = server_response_request(
        f"https://api-service-mrz6aygprq-oa.a.run.app/api/journals?journalName={urllib.parse.quote(Journal_Name)}",
    )

    if server_error:
        print(
            "\n"
            + (colored(" i ", "red", attrs=["reverse"])) * (is_windows)
            + (emoji.emojize(":red_exclamation_mark:")) * (not is_windows)
            + colored(f"  A server error occured, try again later.", "red")
        )
        driver.close()
        os._exit(0)

    try:

        Journal_List_json = Journal_List_json.json()
        return receive_journal_selection_action(driver, Journal_List_json)

    except:

        print(
            "\n\n"
            + colored(" ! ", "yellow", attrs=["reverse"]) * (is_windows)
            + emoji.emojize(":loudspeaker:") * (not is_windows)
            + colored(
                "  The requested journal could not be found.\n",
                "yellow",
            )
        )

        return []


def receive_journal_selection_action(driver, Journal_List_json):

    print(
        colored(
            "\n\nPlease select a journal from the list below:\n",
            attrs=["bold"],
        )
    )

    time.sleep(1)

    journal_list_number = 0

    for Journal_Name in Journal_List_json:

        journal_list_number += 1

        print("[" + str(journal_list_number) + "] " + Journal_Name["journalName"])

    Journal_Number = get_input(
        colored(
            "\n\n-- Type the Number of the Journal\n   : ",
        )
    )

    try:
        return process_journal_selection_action(
            driver, Journal_Number, Journal_List_json
        )
    except TypoException:
        return receive_journal_selection_action(driver, Journal_List_json)


def process_journal_selection_action(driver, Journal_Number, Journal_List_json):

    if Journal_Number in [str(x) for x in list(range(1, 11))]:

        Journal_Selected_urlenc = urllib.parse.quote(
            Journal_List_json[int(Journal_Number) - 1]["journalName"]
        )

        server_error, Article_ID_list = server_response_request(
            f"https://api-service-mrz6aygprq-oa.a.run.app/api/articles?journalName={Journal_Selected_urlenc}&scraped=0&exact=1",
        )

        if server_error:
            print(
                "\n"
                + (colored(" i ", "red", attrs=["reverse"])) * (is_windows)
                + (emoji.emojize(":red_exclamation_mark:")) * (not is_windows)
                + colored(f"  A server error occured, try again later.", "red")
            )
            driver.close()
            os._exit(0)

        if Article_ID_list.status_code == 200:

            Article_ID_list = Article_ID_list.json()

            if len(Article_ID_list) > 0:

                print(
                    "\n"
                    + colored(" ! ", "green", attrs=["reverse"]) * (is_windows)
                    + emoji.emojize(":check_mark_button:") * (not is_windows)
                    + colored(
                        "   List of articles from selected journal found.\n",
                        "green",
                    )
                )

                time.sleep(1)

                return Article_ID_list

            else:

                print(
                    "\n\n"
                    + colored(" ! ", "yellow", attrs=["reverse"]) * (is_windows)
                    + emoji.emojize(":loudspeaker:") * (not is_windows)
                    + colored(
                        "   It appears that all articles from this journal are already available.\n",
                        "yellow",
                    )
                )

                return []

        else:

            print(
                "\n\n"
                + colored(" ! ", "red", attrs=["reverse"]) * (is_windows)
                + emoji.emojize(":red_exclamation_mark:") * (not is_windows)
                + colored(
                    "   An unexpected error occured.\n",
                    "red",
                )
            )

            return []

    else:
        print_typo()
        raise TypoException


def receive_retry_search_action(driver, search_criteria, type):

    not_found = get_input(
        colored(
            f"\n-- Type [1] to retry {type} Search\n-- Type [2] to return to upload menu\n-- Type [3] to return to main menu\n   : ",
        )
    )

    try:
        return process_retry_search_action(driver, not_found, search_criteria)
    except TypoException:
        return receive_retry_search_action(driver, search_criteria, type)


def process_retry_search_action(driver, not_found, search_criteria):

    if not_found == "1":
        return process_upload_criteria_action(driver, search_criteria)
    elif not_found == "2":
        return receive_upload_criteria_action(driver)
    elif not_found == "3":
        driver.close()
        raise MainException
    else:
        print_typo()
        raise TypoException


def print_pdf_found():

    print(
        "\n\n"
        + colored(" i ", "blue", attrs=["reverse"]) * (is_windows)
        + emoji.emojize(":information:") * (not is_windows)
        + "   PDF files located and login process complete, the browser will run in the background."
    )

    time.sleep(1)

    print(
        "\n"
        + colored(" i ", "blue", attrs=["reverse"]) * (is_windows)
        + emoji.emojize(":information:") * (not is_windows)
        + "   You can minimize this window and continue with other tasks on your computer while your files upload."
    )

    time.sleep(1)

    print(
        "\n"
        + colored(" i ", "blue", attrs=["reverse"]) * (is_windows)
        + emoji.emojize(":information:") * (not is_windows)
        + "   Do not exit/close this window as this will abort the upload process.\n"
    )

    time.sleep(1)


def get_input(text):
    return input(text).strip()
