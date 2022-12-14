import time
import os
import emoji

from termcolor import colored
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

from helpers import system


def login(driver, login_method):

    if login_method == "1":
        return vpn_login(driver)

    if login_method == "2":
        return manual_login(driver)


def vpn_login(driver):

    is_windows = system()

    print(
        "\n"
        + (colored(" i ", "blue", attrs=["reverse"])) * (is_windows)
        + (emoji.emojize(":information:")) * (not is_windows)
        + "   You have chosen to login via VPN/wifi."
    )

    time.sleep(1)

    print(
        "\n"
        + colored(" i ", "blue", attrs=["reverse"]) * (is_windows)
        + emoji.emojize(":information:") * (not is_windows)
        + "   Follow the steps below:"
    )

    time.sleep(1)

    print(
        colored(
            "\n\nStep 1/1: Please connect to your institution's VPN or wifi, then continue.\n",
            "blue",
        )
    )

    time.sleep(1)

    cont = proceed()

    if cont == "1":

        print("\nyou are now being routed to JSTOR home page...")

        time.sleep(2)

        print(
            "\ngive it a second, we are checking if the page has loaded successfully..."
        )

        driver.get("https://www.jstor.org/")

        try:

            WebDriverWait(driver, 60).until(
                expected_conditions.element_to_be_clickable(
                    (
                        By.CLASS_NAME,
                        "query-builder-input-group",
                    )
                )
            )

        except:
            print(
                "\n"
                + colored(" ! ", "red", attrs=["reverse"])
                + colored(" Unable to load JSTOR page.\n", "red") * (is_windows)
                + emoji.emojize(":red_exclamation_mark:") * (not is_windows)
            )

            print(
                "\n"
                + colored(" i ", "blue", attrs=["reverse"]) * (is_windows)
                + emoji.emojize(":information:") * (not is_windows)
                + "  Check your internet connection and try again.\n"
            )

            driver.close()

            return False

        print("\nchecking for successful login...\n")

        time.sleep(2)

        try:
            driver.find_element(By.CLASS_NAME, "pds__access-provided-by")

            time.sleep(1)

            print(
                "\n"
                + colored(" ! ", "green", attrs=["reverse"]) * (is_windows)
                + emoji.emojize(":check_mark_button:") * (not is_windows)
                + colored("  Login was successful!\n", "green")
            )

            time.sleep(1)

            driver.maximize_window()

        except:

            time.sleep(1)

            print(
                "\n"
                + colored(" ! ", "red", attrs=["reverse"]) * (is_windows)
                + emoji.emojize(":red_exclamation_mark:") * (not is_windows)
                + colored("  Login was unsuccessful\n", "red")
            )

            return False
    else:

        return False

    return True


def manual_login(driver):

    is_windows = system()

    print(
        "\n"
        + colored(" i ", "blue", attrs=["reverse"]) * (is_windows)
        + emoji.emojize(":information:") * (not is_windows)
        + "   You will be prompted to manually login via the JSTOR website."
    )

    time.sleep(1)

    cont = proceed()

    if cont == "1":

        print("\nYou are now being routed to JSTOR home page...")

        time.sleep(2)

        print("\nSit tight and wait for Google Chrome to open on your screen...\n")

        time.sleep(2)

        print(
            "\n"
            + (colored(" i ", "blue", attrs=["reverse"])) * (is_windows)
            + (emoji.emojize(":information:")) * (not is_windows)
            + "   While the browser opens, read through the login steps:"
        )

        time.sleep(1)

        print(
            colored(
                "\nStep 1/4: Navigate to the top of the JSTOR home page, and click on the link: ",
                "blue",
            )
            + colored(
                "Log in through your library.",
                "blue",
                attrs=["reverse"],
            )
            * (is_windows)
            + colored(
                "Log in through your library.",
                "blue",
                attrs=["bold"],
            )
            * (not is_windows)
            + colored(
                "\nStep 2/4: Search for your institution by using the search box.\nStep 3/4: Log in using your institution's login credentials.\nStep 4/4: Accept the cookies.",
                "blue",
            )
        )

        time.sleep(1)

        print(
            "\nGive it a second, we are checking if the page has loaded successfully..."
        )

        driver.get("https://www.jstor.org/")

        try:

            WebDriverWait(driver, 60).until(
                expected_conditions.element_to_be_clickable(
                    (By.CLASS_NAME, "query-builder-input-group")
                )
            )
        except:
            print(
                "\n"
                + colored(" ! ", "red", attrs=["reverse"]) * (is_windows)
                + emoji.emojize(":red_exclamation_mark:") * (not is_windows)
                + colored("  Unable to load JSTOR page.\n", "red")
            )

            print(
                "\n"
                + colored(" i ", "blue", attrs=["reverse"]) * (is_windows)
                + emoji.emojize(":information:") * (not is_windows)
                + "   Check your internet connection and try again.\n"
            )

            driver.close()

            return False

        driver.maximize_window()

        print(
            "\n"
            + colored(" i ", "blue", attrs=["reverse"]) * (is_windows)
            + emoji.emojize(":information:") * (not is_windows)
            + "   Once you have completed the steps, continue:"
        )

        cont = proceed()

        if cont == "1":

            try:

                WebDriverWait(driver, 60).until(
                    expected_conditions.element_to_be_clickable(
                        (By.CLASS_NAME, "query-builder-input-group")
                    )
                )

            except:
                print(
                    "\n"
                    + colored(" ! ", "red", attrs=["reverse"]) * (is_windows)
                    + emoji.emojize(":red_exclamation_mark:") * (not is_windows)
                    + colored("  Unable to load JSTOR page.\n", "red")
                )

            print("\nchecking for successful login...\n")

            time.sleep(1)

            try:
                driver.find_element(By.CLASS_NAME, "pds__access-provided-by")
                time.sleep(1)
                print(
                    "\n"
                    + colored(" ! ", "green", attrs=["reverse"]) * (is_windows)
                    + emoji.emojize(":check_mark_button:") * (not is_windows)
                    + colored("  Login was successful!\n", "green")
                )

                time.sleep(1)

                driver.maximize_window()

                driver.set_window_position(-2024, 2024)

            except:
                time.sleep(1)
                print(
                    "\n"
                    + colored(" ! ", "red", attrs=["reverse"]) * (is_windows)
                    + emoji.emojize(":red_exclamation_mark:") * (not is_windows)
                    + colored("  Login was unsuccessful\n", "red")
                )

                return False
        else:
            return False
    else:
        return False

    return True


def get_login_method():

    login_method = input(
        colored(
            "\n-- Type [1] to login via institution VPN or wifi"
            + "\n-- Type [2] to manually login via the JSTOR website"
            + "\n-- Type [3] to exit"
            + "\n   : ",
        )
    )

    if login_method == "1" or login_method == "2":
        return login_method

    if login_method == "3":
        os._exit(0)

    return get_login_method()


def proceed():

    proceed_input = input(
        colored("\n-- Type [1] to continue\n-- Type [2] to restart\n   : ")
    )

    if proceed_input != "1" and proceed_input != "2":
        return proceed()

    return proceed_input


def login_requirements():

    is_windows = system()

    print(colored("\n\nPlease note:", attrs=["reverse"]) * (is_windows))
    print(colored("\n\nPlease note:", attrs=["bold", "underline"]) * (not is_windows))

    print(
        "\n\n"
        + colored(" i ", "blue", attrs=["reverse"]) * (is_windows)
        + emoji.emojize(":information:") * (not is_windows)
        + "   Valid JSTOR login credentials are a requirement to use this tool."
    )

    print(
        "\n"
        + colored(" i ", "blue", attrs=["reverse"]) * (is_windows)
        + emoji.emojize(":information:") * (not is_windows)
        + "   You will need Google Chrome installed on your device."
    )

    print(
        "\n"
        + colored(" i ", "blue", attrs=["reverse"]) * (is_windows)
        + emoji.emojize(":information:") * (not is_windows)
        + "   You will need ffmpeg and ffprobe installed on your device."
    )

    print(
        "\n\nBefore you start, "
        + colored("ensure that you:", attrs=["reverse"]) * (is_windows)
        + colored("ensure that you:", attrs=["bold", "underline"]) * (not is_windows)
    )

    print(
        "\na) Have Google Chrome installed. To install, visit https://support.google.com/chrome/answer/95346?hl=en&ref_topic=7439538. \nb) Have ffmpeg and ffprobe installed. For installation instructions, visit https://www.wikihow.com/Install-FFmpeg-on-Windows. \nc) Have a stable internet connection.\nd) Keep your device on charge and set to 'never sleep' while on battery and on charge."
        * (is_windows)
    )

    print(
        "\na) Have Google Chrome installed. To install, visit https://support.google.com/chrome/answer/95346?hl=en&ref_topic=7439538. \nb) Have ffmpeg and ffprobe installed. For installation instructions, visit https://bbc.github.io/bbcat-orchestration-docs/installation-mac-manual/. \nc) Have a stable internet connection.\nd) Keep your device on charge and set to 'never sleep' while on battery and on charge."
        * (not is_windows)
    )

    print(
        "\n\nWhile the program runs "
        + colored("please do not:", attrs=["reverse"]) * (is_windows)
        + colored("please do not:", attrs=["bold", "underline"]) * (not is_windows)
    )

    print(
        "\na) Close the Google Chrome window that will be opened in the next steps.\nb) Interfere with the Google Chrome window unless prompted to do so."
    )

    input(
        colored("\n\n-- Press ")
        + colored("ENTER/RETURN", attrs=["reverse"]) * (is_windows)
        + colored("ENTER/RETURN", attrs=["bold"]) * (not is_windows)
        + colored(" to continue: ")
    )


def login_instructions():

    is_windows = system()

    time.sleep(1)

    print(
        "\n\n\n"
        + colored(" i ", "blue", attrs=["reverse"]) * (is_windows)
        + emoji.emojize(":information:") * (not is_windows)
        + "   To continue, a JSTOR user login is required, either via institution VPN/wifi or manually via the JSTOR website."
    )

    time.sleep(1)

    print(
        "\n"
        + colored(" i ", "blue", attrs=["reverse"]) * (is_windows)
        + emoji.emojize(":information:") * (not is_windows)
        + "   No login information will be recorded in the process."
    )

    time.sleep(1)

    print("\n\n" + colored("User credential security information", attrs=["reverse"]))

    print(
        "\n\nIf you choose to login via the JSTOR website, you will be prompted to enter your login details via your university portal on JSTOR."
    )

    print(
        "\nIf you choose to login via VPN or wifi, your credentials will already be authenticated and you won't need to provide any login details."
    )

    time.sleep(2)

    print(
        "\n\n\n"
        + colored("JSTOR Login Instructions:", attrs=["reverse"]) * (is_windows)
        + colored("JSTOR Login Instructions:", attrs=["bold", "underline"])
        * (not is_windows)
        + "\n"
    )

    print(
        "\n"
        + colored(" i ", "blue", attrs=["reverse"]) * (is_windows)
        + emoji.emojize(":information:") * (not is_windows)
        + "   Please follow the prompts below to login"
    )


def main_menu():

    is_windows = system()

    print(
        "\n"
        + colored(" i ", "blue", attrs=["reverse"]) * (is_windows)
        + emoji.emojize(":information:") * (not is_windows)
        + "   To Choose a login method, enter [1]" * (is_windows)
        + "   To Choose a login method, enter " * (not is_windows)
        + colored("[1]", attrs=["bold"]) * (not is_windows)
    )

    print(
        "\n"
        + colored(" i ", "blue", attrs=["reverse"]) * (is_windows)
        + emoji.emojize(":information:") * (not is_windows)
        + "   To exit the program, enter [2]" * (is_windows)
        + "   To exit the program, enter " * (not is_windows)
        + colored("[2]", attrs=["bold"]) * (not is_windows)
    )

    select = input(colored("\n-- Please enter your selection: ")).strip()

    return select
