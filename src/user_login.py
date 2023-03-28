import time
import emoji
import os

from termcolor import colored
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from src.errors import MainException, TypoException

from src.helpers import system, print_typo

is_windows = system()


def print_login_requirements():

    print(colored("\n\n\nSet-up and Dependencies", attrs=["reverse"]))

    print(colored("\n\nPlease note:", attrs=["reverse"]) * (is_windows))
    print(colored("\n\nPlease note:", attrs=["bold", "underline"]) * (not is_windows))

    print(
        "\n"
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
        "\n• Have Google Chrome installed. To install, visit https://support.google.com/chrome/answer/95346?hl=en&ref_topic=7439538. \n• Have ffmpeg and ffprobe installed. For installation instructions, visit https://www.wikihow.com/Install-FFmpeg-on-Windows. \n• Have a stable internet connection.\n• Keep your device on charge and set to 'never sleep' while on battery and on charge."
        * (is_windows)
    )

    print(
        "\n• Have Google Chrome installed. To install, visit https://support.google.com/chrome/answer/95346?hl=en&ref_topic=7439538. \n• Have ffmpeg and ffprobe installed. For installation instructions, visit https://bbc.github.io/bbcat-orchestration-docs/installation-mac-manual/. \n• Have a stable internet connection.\n• Keep your device on charge and set to 'never sleep' while on battery and on charge."
        * (not is_windows)
    )

    print(
        "\n\nWhile the program runs, "
        + colored("please do not:", attrs=["reverse"]) * (is_windows)
        + colored("please do not:", attrs=["bold", "underline"]) * (not is_windows)
    )

    print(
        "\n• Close the Google Chrome window that will be opened in the next steps.\n• Interfere with the Google Chrome window unless prompted to do so."
    )

    get_input(
        colored("\n\n-- Press ")
        + colored("ENTER/RETURN", attrs=["reverse"]) * (is_windows)
        + colored("ENTER/RETURN", attrs=["bold"]) * (not is_windows)
        + colored(" to continue: ")
    )


def print_login_instructions():

    print("\n\n\n" + colored("JSTOR Login", attrs=["reverse"]))

    print(
        "\n\n"
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

    print(
        "\n\n"
        + colored("User credential security information:", attrs=["reverse"])
        * (is_windows)
        + colored("User credential security information:", attrs=["bold", "underline"])
        * (not is_windows)
    )

    print(
        "\n\n• If you choose to login via VPN or wifi, your credentials will already be authenticated and you won't need to provide\n  any login details.\n• If you choose to login via the JSTOR website, you will be prompted to enter your login details via your university\n  portal on JSTOR."
    )

    time.sleep(2)

    print(
        "\n\n"
        + colored("JSTOR Login Instructions:", attrs=["reverse"]) * (is_windows)
        + colored("JSTOR Login Instructions:", attrs=["bold", "underline"])
        * (not is_windows)
        + "\n"
    )


def receive_login_action():

    print(
        "\n"
        + colored(" i ", "blue", attrs=["reverse"]) * (is_windows)
        + emoji.emojize(":information:") * (not is_windows)
        + "   Please follow the prompts below to login."
    )

    login_method = get_input(
        colored(
            "\n-- Type [1] to login via institution VPN or wifi"
            + "\n-- Type [2] to manually login via the JSTOR website"
            + "\n-- Type [3] to return to main menu"
            + "\n   : ",
        )
    )

    return login_method


def vpn_login(driver, url, html_load, html_login):

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

    cont = receive_proceed_action()

    if cont == "1":

        print("\nGive it a second, we are checking for successful login.\n")

        driver.get(url)

        if validate_page_load(driver, html_load) == False:
            return False

        time.sleep(2)

        if validate_login(driver, html_login) == True:

            driver.maximize_window()

            return True

        else:

            return False

    elif cont == "2":

        driver.close()

        return False


def manual_login(driver, url, html_load, html_login):

    print("\nYou are now being routed to JSTOR home page.")

    time.sleep(2)

    print("\nSit tight and wait for Google Chrome to open on your screen.\n")

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

    print("\nGive it a second, we are checking if the page has loaded successfully.")

    driver.get(url)

    if validate_page_load(driver, html_load) == False:

        return False

    driver.maximize_window()

    print(
        "\n"
        + colored(" i ", "blue", attrs=["reverse"]) * (is_windows)
        + emoji.emojize(":information:") * (not is_windows)
        + "   Once you have completed the steps, continue:"
    )

    cont = receive_proceed_action()

    if cont == "1":

        if validate_page_load(driver, html_load) == False:

            return False

        print("\nChecking for successful login.\n")

        time.sleep(1)

        if validate_login(driver, html_login) == True:

            driver.maximize_window()

            driver.set_window_position(-2024, 2024)

            return True

        else:

            return False

    else:

        driver.close()

        return False


def validate_page_load(driver, html_load):

    try:

        WebDriverWait(driver, 60).until(
            expected_conditions.element_to_be_clickable(
                (
                    By.CLASS_NAME,
                    html_load,
                )
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
            + "  Check your internet connection and try again.\n"
        )

        driver.close()

        return False

    "pds__access-provided-by"


def validate_login(driver, html_login):

    try:
        driver.find_element(By.CLASS_NAME, html_login)

        time.sleep(1)

        print(
            "\n"
            + colored(" ! ", "green", attrs=["reverse"]) * (is_windows)
            + emoji.emojize(":check_mark_button:") * (not is_windows)
            + colored("   Login was successful!\n", "green")
        )

        time.sleep(1)

        return True

    except:

        time.sleep(1)

        print_unsuccessful()

        return False


def print_unsuccessful():

    print(
        "\n"
        + colored(" ! ", "red", attrs=["reverse"]) * (is_windows)
        + emoji.emojize(":red_exclamation_mark:") * (not is_windows)
        + colored("   Login was unsuccessful\n", "red")
    )

    print(
        "\n"
        + colored(" i ", "blue", attrs=["reverse"]) * (is_windows)
        + emoji.emojize(":information:") * (not is_windows)
        + "   Try again, make sure you follow the instructions carefully.\n"
    )


def receive_proceed_action():

    proceed_input = get_input(
        colored(
            "\n-- Type [1] to continue\n-- Type [2] to return to contributions menu\n   : "
        )
    )
    if proceed_input != "1" and proceed_input != "2":

        print_typo()

        return receive_proceed_action()

    return proceed_input


def receive_end_program_action(driver):

    exit_program = get_input(
        colored(
            "\n-- Type [1] to make another contribution\n-- Type [2] to go back to main menu\n-- Type [3] to exit\n   : "
        )
    )

    try:
        return process_end_program_action(driver, exit_program)
    except TypoException:
        return receive_end_program_action(driver)


def process_end_program_action(driver, exit_program):

    if exit_program == "1":
        return 0
    elif exit_program == "2":
        driver.close()
        raise MainException
    elif exit_program == "3":
        driver.close()
        os._exit(0)

    else:
        print_typo()
        raise TypoException


def get_input(text):
    return input(text).strip()
