import time
import os

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By


def login(method):

    if method == 1:
        message = "\n-- Select a login method"
    else:
        message = "\n-- Select an alternative login method"

    login_method = input(
        color.PURPLE + message + color.BOLD + " (VPN,JSTOR): " + color.END
    )

    return login_method


def proceed():

    proceed = input(
        color.PURPLE
        + "\n-- Would you like to proceed?"
        + color.BOLD
        + " (Y/n): "
        + color.END
    )

    return proceed


def exit():

    exit = input(
        color.PURPLE
        + "\n-- Would you like to exit?"
        + color.BOLD
        + " (Y/n): "
        + color.END
    )

    return exit


class color:
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[95m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    ITALIC = "\x1B[3m"
    END = "\033[0m"


def user_login_guide(driver, host, wait):

    print(color.BOLD + color.UNDERLINE + "\nLogin Instructions\n" + color.END)
    print(
        color.BOLD
        + "\nFollow the prompts below to ensure a successful login\n"
        + color.END
    )

    login_method = login(1)

    while True:
        if login_method == "VPN" or login_method == "vpn" or login_method == "Vpn":

            time.sleep(1)

            print(
                color.YELLOW
                + "\n[INFO] Ensure that you are within your institution's network to use this method"
                + "\n[INFO] To continue to login instructions, enter: Y"
                + "\n[INFO] To select an alternative login method or to exit, enter: n"
                + color.END
            )

            time.sleep(1)

            cont = proceed()

            if cont == "Y":

                time.sleep(1)

                print(
                    color.GREEN
                    + "\n[INFO] You have chosen to log in via VPN"
                    + "\n[INFO] Follow the instructions below"
                    + color.END
                )

                time.sleep(1)

                print(
                    color.BOLD
                    + "\n\nPlease connect to your institution's wifi or VPN and then proceed\n"
                    + color.END
                )

                time.sleep(1)

                cont = proceed()

                if cont == "Y":

                    print(
                        color.ITALIC
                        + "\n...you are now being routed to JSTOR home page"
                        + color.END
                    )

                    time.sleep(2)

                    print(
                        color.ITALIC
                        + "\n...sit tight and wait for the browser to load"
                        + color.END
                    )

                    driver.get(host)

                    try:

                        WebDriverWait(driver, 60).until(
                            expected_conditions.element_to_be_clickable(
                                (By.XPATH, r"//input[@id='query-builder-input']")
                            )
                        )

                    except:
                        print(
                            color.RED + "\n[ERR] Unable to load JSTOR page" + color.END
                        )
                        print(
                            color.YELLOW
                            + "[INFO] Check your internet connection and try again"
                            + color.END
                        )
                        login_method = login(2)
                        continue

                    print(
                        color.BOLD
                        + "\n\nPlease accept the cookies and then proceed\n"
                        + color.END
                    )

                    time.sleep(2)

                    driver.maximize_window()

                    cont = proceed()

                    if cont == "Y":

                        print(
                            color.ITALIC
                            + "\n...checking for succesful login"
                            + color.END
                        )

                        time.sleep(2)

                        try:
                            driver.find_element(
                                By.CLASS_NAME, "pds__access-provided-by"
                            )
                            time.sleep(1)
                            print(
                                color.GREEN
                                + "\n[INFO] Login was successful\n"
                                + color.END
                            )

                            time.sleep(wait)
                            break

                        except:
                            time.sleep(1)
                            print(
                                color.RED
                                + "\n[ERR] Login was unsuccessful\n"
                                + color.END
                            )
                            login_method = login(2)
                            continue

                    elif cont == "n":
                        x = exit()
                        if x == "Y":
                            os._exit(0)
                        else:
                            login_method = login(2)
                        continue

                elif cont == "n":
                    x = exit()
                    if x == "Y":
                        os._exit(0)
                    else:
                        login_method = login(2)
                    continue

            elif cont == "n":
                x = exit()
                if x == "Y":
                    os._exit(0)
                else:
                    login_method = login(2)
                continue

        elif (
            login_method == "JSTOR"
            or login_method == "jstor"
            or login_method == "Jstor"
        ):

            time.sleep(1)

            print(
                color.YELLOW
                + "\n[INFO] You will be promped to login via the JSTOR website"
                + "\n[INFO] To continue to login instructions, enter: Y"
                + "\n[INFO] To select an alternative login method or to exit, enter: n"
                + color.END
            )

            time.sleep(1)

            cont = proceed()

            if cont == "Y":
                print(
                    color.GREEN
                    + "\n[INFO] You have selected to login via JSTOR"
                    + color.END
                )

                print(color.ITALIC + "\n...you are now being routed to JSTOR home page")

                time.sleep(2)

                print("\n...sit tight and wait for Google Chrome to open")

                time.sleep(2)

                print(
                    "\n...while the browser opens, read the following instructions"
                    + color.END
                )

                time.sleep(1)

                print(
                    color.BOLD
                    + "\n\nPlease log in to JSTOR by using your institution's credentials and then proceed:\n"
                    + color.END
                )

                print(
                    color.BOLD
                    + "\nStep 1: Navigate to the top of the JSTOR home page, and click on the link: "
                    + color.UNDERLINE
                    + "Log in through your library"
                    + color.END
                    + color.BOLD
                    + "\nStep 2: Search for your institution by using the search box"
                    + "\nStep 3: Log in using your institution's login credentials"
                    + color.END
                )

                driver.get(host)

                try:

                    WebDriverWait(driver, 60).until(
                        expected_conditions.element_to_be_clickable(
                            (By.XPATH, r"//input[@id='query-builder-input']")
                        )
                    )
                except:
                    print(color.RED + "\n[INFO] Unable to load JSTOR page" + color.END)
                    # print(
                    #     color.YELLOW
                    #     + "\n[INFO] Check your internet connection and try again"
                    #     + color.END
                    # )
                    # login_method = login(2)

                driver.maximize_window()

                cont = proceed()

                if cont == "Y":

                    try:

                        WebDriverWait(driver, 60).until(
                            expected_conditions.element_to_be_clickable(
                                (By.XPATH, r"//input[@id='query-builder-input']")
                            )
                        )

                    except:
                        print(
                            color.RED + "\n[INFO] Unable to load JSTOR page" + color.END
                        )
                        # print(
                        #     color.YELLOW
                        #     + "\n[INFO] Check your internet connection and try again"
                        #     + color.END
                        # )
                        # login_method = login(2)

                    print(
                        color.ITALIC + "\n...checking for succesful login" + color.END
                    )
                    time.sleep(1)

                    try:
                        driver.find_element(By.CLASS_NAME, "pds__access-provided-by")
                        time.sleep(1)
                        print(
                            color.GREEN + "\n[INFO] Login was successful\n" + color.END
                        )

                        time.sleep(wait)
                        break

                    except:
                        time.sleep(1)
                        print(
                            color.RED + "\n[INFO] Login was unsuccessful\n" + color.END
                        )
                        break

                elif cont == "n":
                    x = exit()
                    if x == "Y":
                        os._exit(0)
                    else:
                        login_method = login(2)
                    continue

            elif cont == "n":
                x = exit()
                if x == "Y":
                    os._exit(0)
                else:
                    login_method = login(2)
                continue

        else:
            print(
                color.YELLOW
                + "\n[INFO] It appears that you have made a typo"
                + color.END
            )

            time.sleep(1)

            print(color.YELLOW + "\n[INFO] Please retry" + color.END)

            login(1)
