import requests
import requests.exceptions
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


def server_response_post(driver, post_request_url, files, data, article_json):

    is_windows = system()

    response = None

    retry_upload_count = 0

    while retry_upload_count <= 3:

        try:

            response = requests.post(
                post_request_url,
                files=files,
                data=data,
                verify=False,
            )

            response.raise_for_status()  # Raises a HTTPError if the status is 4xx, 5xx

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):

            print(
                "\n"
                + colored(" ! ", "red", attrs=["reverse"]) * (is_windows)
                + emoji.emojize(":red_exclamation_mark:") * (not is_windows)
                + colored(
                    "   Could not process request, server is down. Try again later.",
                    "red",
                )
            )

            driver.close()
            os._exit(0)

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
                + " in a few moments."
            )

            break

    if retry_upload_count > 3:

        print(
            "\n"
            + colored(" ! ", "red", attrs=["reverse"]) * (is_windows)
            + emoji.emojize(":red_exclamation_mark:") * (not is_windows)
            + colored(
                "  Could not process request, server is not responding. Try again later.",
                "red",
            )
        )

        driver.close()
        os._exit(0)


def server_response_request(url):

    is_windows = system()

    server_error = False

    response = None

    retry_upload_count = 0

    while retry_upload_count <= 3:

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

            print_error()

        except requests.exceptions.HTTPError:

            retry_upload_count += 1

            print("\n[ERR] Could not process request, server error. Retrying.")

        else:

            break

    if retry_upload_count > 3:

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
