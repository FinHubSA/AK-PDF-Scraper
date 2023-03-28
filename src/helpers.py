import requests
import requests.exceptions
import time
import os
import platform
import emoji
import json
import pickle

from termcolor import colored
from src.errors import TypoException

from src.temp_storage import delete_temp_storage


def system():

    system = platform.system()

    is_windows = False

    if system == "Windows":
        os.system("color")
        is_windows = True

    return is_windows


is_windows = system()


def print_typo():

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


def get_user_address_from_json(misc_directory):

    # save the address to a dictionary from the .json file
    with open(os.path.join(misc_directory, "address.json"), "r") as f:

        user_address_dict = json.load(f)

    f.close()

    return user_address_dict


def receive_network_error_action():

    print(
        "\n"
        + colored(" ! ", "yellow", attrs=["reverse"]) * (is_windows)
        + emoji.emojize(":loudspeaker:") * (not is_windows)
        + colored(
            "  Network error. Please check your internet connection and then continue.\n",
            "yellow",
        )
    )

    check_internet = input(
        colored(
            "\n-- Type [1] to continue" + "\n-- Type [2] to exit" + "\n   : ",
        )
    ).strip()

    try:
        return process_network_error_action(check_internet)
    except TypoException:
        return receive_network_error_action()


def process_network_error_action(check_internet):

    if check_internet == "1":
        return
    elif check_internet == "2":
        os._exit(0)
    else:
        print_typo()
        raise TypoException


def server_response_post(driver, url, files, data, article_json, storage_directory):

    response = None

    retry_upload_count = 0

    while retry_upload_count < 3:

        try:

            response = requests.post(
                url,
                files=files,
                data=data,
                verify=False,
            )

            response.raise_for_status()  # Raises a HTTPError if the status is 4xx, 5xx

        except requests.exceptions.Timeout:

            print(
                "\n"
                + colored(" ! ", "red", attrs=["reverse"]) * (is_windows)
                + emoji.emojize(":red_exclamation_mark:") * (not is_windows)
                + colored(
                    "   Could not process request, server is down. Try again later.",
                    "red",
                )
            )

            try:
                delete_temp_storage(storage_directory)
            except Exception as e:
                print(e)

            driver.close()
            os._exit(0)

        except requests.exceptions.ConnectionError:

            retry_upload_count += 1

            receive_network_error_action()

        except requests.exceptions.HTTPError:
            if response.status_code == 500:

                retry_upload_count += 1

                print(
                    "\n[ERR] Could not process request: "
                    + article_json["title"]
                    + ", server error. Retrying."
                )

            elif response.status_code == 404:

                print(
                    "\n[ERR] Could not find article: "
                    + article_json["title"]
                    + " in database, moving on to next article."
                )

                break
        else:

            print(
                "\nSucessfully uploaded article: "
                + article_json["title"]
                + "."
                + "\nIt will be available at "
                + response.json()["bucket_url"]
                + " after it's been scanned. \nCheck back later if it's not available immediately."
            )

            break

    if retry_upload_count >= 3:

        print(
            "\n"
            + colored(" ! ", "red", attrs=["reverse"]) * (is_windows)
            + emoji.emojize(":red_exclamation_mark:") * (not is_windows)
            + colored(
                "  Could not process request, server is not responding. Try again later.",
                "red",
            )
        )

        try:
            delete_temp_storage(storage_directory)
        except Exception as e:
            print(e)

        driver.close()
        os._exit(0)


def server_response_request(url):

    server_error = False

    response = None

    retry_upload_count = 0

    while retry_upload_count < 3:

        try:

            response = requests.get(url)

            response.raise_for_status()

        except requests.exceptions.Timeout:

            print(
                "\n"
                + colored(" ! ", "red", attrs=["reverse"]) * (is_windows)
                + emoji.emojize(":red_exclamation_mark:") * (not is_windows)
                + colored(
                    "   Could not process request, server is down. Please try again later.",
                    "red",
                )
            )

            server_error = True

            break

        except requests.exceptions.ConnectionError:

            retry_upload_count += 1

            receive_network_error_action()

        except requests.exceptions.HTTPError:

            retry_upload_count += 1

            print("\n[ERR] Could not process request, server error. Retrying.")

        else:

            break

    if retry_upload_count >= 3:

        print(
            "\n"
            + colored(" ! ", "red", attrs=["reverse"]) * (is_windows)
            + emoji.emojize(":red_exclamation_mark:") * (not is_windows)
            + colored(
                "  Could not process request, server is not responding. Please try again later.",
                "red",
            )
        )

        server_error = True

    return server_error, response


def set_cookies(driver, misc_directory):

    # Save the cookies to ensure reCAPTCHA can be solved
    # since login details are required to access the mp3 file
    pickle.dump(
        driver.get_cookies(),
        open(os.path.join(misc_directory, "cookies.pkl"), "wb"),
    )

    cookies = pickle.load(open(os.path.join(misc_directory, "cookies.pkl"), "rb"))

    for cookie in cookies:
        driver.add_cookie(cookie)
