import time
from termcolor import colored
import emoji


def login():

    login_method = input(
        colored(
            "\n-- Type [1] to login via institution VPN or wifi\n-- Type [2] to manually login via the JSTOR website\n   : ",
            "magenta",
        )
    )

    return login_method


def proceed():

    proceed = input(
        colored(
            "\n-- Type [1] to continue\n-- Type [2] to restart\n   : ",
            "magenta",
        )
    )

    return proceed


def welcome(system):

    # f = Figlet(font="standard")
    # print(colored(f.renderText("Welcome to Aaron's Kit!"), "green"))

    print(colored("\n\nWelcome to Aaron's Kit!", attrs = ["reverse"]))

    print(
        colored(
            "\n\nAaron's Kit is a tool that enables the effortless liberation of academic research.\n\nBy using this tool, you are playing an active role in the open access movement! \n\nThank you for your contribution.\n"
        )
    )

    time.sleep(2)

    if system == "Windows":

        print("\n\n\n" + colored("Please note:", attrs=["reverse"]))

        print(
            "\n\n"
            + colored(" i ", "blue", attrs=["reverse"])
            + "   Valid JSTOR login credentials are a requirement to use this tool."
        )

        print(
            "\n"
            + colored(" i ", "blue", attrs=["reverse"])
            + "   You will need Google Chrome installed on your device."
        )

        print("\n\nBefore you start, " + colored("ensure that you:", attrs=["reverse"]))

        print(
            "\na) Have Google Chrome installed. To install, visit https://support.google.com/chrome/answer/95346?hl=en&ref_topic=7439538. \nb) Have a stable internet connection.\nc) Keep your device on charge and set to 'never sleep' while on battery and on charge."
        )

        print(
            "\n\nWhile your files download, "
            + colored("please do not:", attrs=["reverse"])
        )

        print(
            "\na) Close Google Chrome.\nb) Interfere with Google Chrome while your files are being downloaded."
        )

        input(
            colored("\n\n-- Press ", "magenta")
            + colored("ENTER/RETURN", "magenta", attrs=["reverse"])
            + colored(" to continue: ", "magenta")
        )

    else:
        print(colored("\n\n\nPlease note:", attrs=["bold", "underline"]))

        print(
            "\n\n"
            + emoji.emojize(":information:")
            + "   Valid JSTOR login credentials are a requirement to use this tool."
        )

        print(
            "\n"
            + emoji.emojize(":information:")
            + "   You will need Google Chrome installed on your device."
        )

        print(
            "\n\nBefore you start, "
            + colored("ensure that you:", attrs=["bold", "underline"])
        )

        print(
            "\na) Have Google Chrome installed. To install, visit https://support.google.com/chrome/answer/95346?hl=en&ref_topic=7439538. \nb) Have a stable internet connection.\nc) Keep your device on charge and set to 'never sleep' while on battery and on charge."
        )

        print(
            "\n\nWhile your files download, "
            + colored("please do not:", attrs=["bold", "underline"])
        )

        print(
            "\na) Close Google Chrome.\nb) Interfere with Google Chrome while your files are being downloaded."
        )

        input(
            colored("\n\n-- Press ", "magenta")
            + colored("ENTER/RETURN", "magenta", attrs=["bold"])
            + colored(" to continue: ", "magenta")
        )


def vpn_or_manual(system):

    time.sleep(1)

    if system == "Windows":

        print(
            "\n\n"
            + colored(" i ", "blue", attrs=["reverse"])
            + "   To continue, a JSTOR user login is required, either via institution VPN/wifi or manually via the JSTOR website."
        )

        time.sleep(1)

        print(
            "\n"
            + colored(" i ", "blue", attrs=["reverse"])
            + "   No login information will be recorded in the process."
        )

        time.sleep(1)

        print("\n\n" + colored("JSTOR Login Instructions:", attrs=["reverse"]) + "\n")

        print(
            "\n"
            + colored(" i ", "blue", attrs=["reverse"])
            + "   Please follow the prompts below to login"
        )

    else:

        print(
            "\n\n"
            + emoji.emojize(":information:")
            + "   To continue, a JSTOR user login is required, either via institution VPN/wifi or manually via the JSTOR website."
        )

        time.sleep(1)

        print(
            "\n"
            + emoji.emojize(":information:")
            + "   No login information will be recorded in the process."
        )

        time.sleep(1)

        print(
            "\n\n"
            + colored("JSTOR Login Instructions:", attrs=["bold", "underline"])
            + "\n"
        )

        print(
            "\n"
            + emoji.emojize(":information:")
            + "   Please follow the prompts below to login"
        )

    login_method = login()

    return login_method


def main_menu(system):

    if system == "Windows":

        print(
            "\n"
            + colored(" i ", "blue", attrs=["reverse"])
            + "   To Choose a login method, enter [1]"
        )

        print(
            "\n"
            + colored(" i ", "blue", attrs=["reverse"])
            + "   To exit the program, enter [2]"
        )

    else:

        print(
            "\n"
            + emoji.emojize(":information:")
            + "   To Choose a login method, enter "
            + colored("[1]", attrs=["bold"])
        )

        print(
            "\n"
            + emoji.emojize(":information:")
            + "   To exit the program, enter "
            + colored("[2]", attrs=["bold"])
        )

    select = input(colored("\n-- Please enter your selection: ", "magenta"))

    return select


def typo(system):

    if system == "Windows":

        print(
            "\n"
            + colored(" ? ", "yellow", attrs=["reverse"])
            + colored(
                "  It appears that you made a typo, you are being directed to the main selection menu",
                "yellow",
            )
        )

    else:

        print(
            "\n"
            + emoji.emojize(":loudspeaker:")
            + colored(
                "  It appears that you made a typo, you are being directed to the main selection menu",
                "yellow",
            )
        )

    time.sleep(1)

    main = main_menu(system)

    return main
