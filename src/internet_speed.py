import speedtest
import time
import platform
import emoji

from termcolor import colored

# returns the user download speed
def download_speed():

    retry = 0
    speed = False
    while speed == False and retry <= 3:

        try:

            time.sleep(1)

            speed_test = speedtest.Speedtest()

            download_speed = speed_test.download()

            mbps = download_speed / (1024 * 1024)

            speed = True

        except:

            mbps = "Error"

            retry += 1

    return mbps


# returns the waiting time
def delay(mbps):

    if mbps <= 10:

        wait = 30

    elif mbps <= 25:

        wait = 20

    elif mbps <= 75:

        wait = 15

    else:

        wait = 10

    return wait


def internet_speed_retry(system):
    internet_retry = True

    while internet_retry == True:

        print("\n\ndetermining internet speed...")

        mbps = download_speed()

        time.sleep(1)

        if mbps == "Error":

            if system == "Windows":

                print(
                    "\n\n"
                    + colored(" ! ", "yellow", attrs=["reverse"])
                    + colored(
                        "   It seems that your internet speed is unstable at the moment.",
                        "yellow",
                    )
                )

                print(
                    "\n\n"
                    + colored(" i ", "blue", attrs=["reverse"])
                    + "   Please check your internet connection, and then make a selection."
                )

                print(
                    "\n"
                    + colored(" i ", "blue", attrs=["reverse"])
                    + "   Note that an unstable internet connection might interfere with the download process."
                )

                internet_typo = True

                while internet_typo:
                    internet_option = input(
                        colored(
                            "\n-- Type [1] to retry speed check\n-- Type [2] to continue with an unstable connection\n   : "
                        )
                    )

                    if internet_option == "1":
                        internet_typo = False
                    elif internet_option == "2":
                        mbps = 15
                        internet_typo = False
                        internet_retry = False
                    else:
                        print(
                            "\n\n"
                            + colored(" ? ", "yellow", attrs=["reverse"])
                            + colored(
                                "   It appears that you made a typo, please re-enter your selection.\n",
                                "yellow",
                            )
                        )

            else:

                print(
                    "\n\n"
                    + emoji.emojize(":loudspeaker:")
                    + colored(
                        "   It seems that your internet speed is unstable at the moment.",
                        "yellow",
                    )
                )

                print(
                    "\n\n"
                    + emoji.emojize(":information:")
                    + "   Please check your internet connection, and then make a selection."
                )

                print(
                    "\n"
                    + emoji.emojize(":information:")
                    + "   Note that an unstable internet connection might interfere with the download process."
                )

                internet_typo = True

                while internet_typo == True:
                    internet_option = input(
                        colored(
                            "\n-- Type [1] to retry speed check\n-- Type [2] to continue with an unstable connection\n   : "
                        )
                    )

                    if internet_option == "1":
                        internet_typo = False
                    elif internet_option == "2":
                        mbps = 15
                        internet_typo = False
                        internet_retry = False
                    else:
                        print(
                            "\n\n"
                            + emoji.emojize(":loudspeaker:")
                            + colored(
                                "   It appears that you made a typo, please re-enter your selection.\n",
                                "yellow",
                            )
                        )

        elif mbps <= 5:

            if system == "Windows":

                print(
                    "\n\n"
                    + colored(" ! ", "yellow", attrs=["reverse"])
                    + colored("   Your internet speed is less than 5 mbps.", "yellow")
                )

                print(
                    "\n\n"
                    + colored(" i ", "blue", attrs=["reverse"])
                    + "   Please check your internet connection, and then make a selection"
                )

                print(
                    "\n"
                    + colored(" i ", "blue", attrs=["reverse"])
                    + "   Note that a slow internet connection might interfere with the download process."
                )

                internet_typo = True

                while internet_typo:
                    internet_option = input(
                        colored(
                            "\n-- Type [1] to retry speed check\n-- Type [2] to continue with a slow connection\n   : "
                        )
                    )

                    if internet_option == "1":
                        internet_typo = False
                    elif internet_option == "2":
                        mbps = 15
                        internet_typo = False
                        internet_retry = False
                    else:
                        print(
                            "\n\n"
                            + colored(" ? ", "yellow", attrs=["reverse"])
                            + colored(
                                "   It appears that you made a typo, please re-enter your selection.\n",
                                "yellow",
                            )
                        )

            else:
                print(
                    "\n\n"
                    + emoji.emojize(":loudspeaker:")
                    + colored("   Your internet speed is less than 5 mbps.", "yellow")
                )

                print(
                    "\n\n"
                    + emoji.emojize(":information:")
                    + "   Please check your internet connection, and then make a selection"
                )

                print(
                    "\n"
                    + emoji.emojize(":information:")
                    + "   Note that a slow internet connection might interfere with the download process."
                )

                internet_typo = True

                while internet_typo == True:
                    internet_option = input(
                        colored(
                            "\n-- Type [1] to retry speed check\n-- Type [2] to continue with a slow connection\n   : "
                        )
                    )

                    if internet_option == "1":
                        internet_typo = False
                    elif internet_option == "2":
                        mbps = 15
                        internet_typo = False
                        internet_retry = False
                    else:
                        print(
                            "\n\n"
                            + emoji.emojize(":loudspeaker:")
                            + colored(
                                "   It appears that you made a typo, please re-enter your selection.\n",
                                "yellow",
                            )
                        )

        else:
            if system == "Windows":
                print(
                    "\n\n"
                    + colored(" ! ", "green", attrs=["reverse"])
                    + colored(
                        "   Your internet speed is: " + str(round(mbps, 2)) + " mbps",
                        "green",
                    )
                )
            else:
                print(
                    "\n\n"
                    + emoji.emojize(":check_mark_button:")
                    + colored(
                        "   Your internet speed is: " + str(round(mbps, 2)) + " mbps",
                        "green",
                    )
                )

            internet_retry = False

    return mbps
