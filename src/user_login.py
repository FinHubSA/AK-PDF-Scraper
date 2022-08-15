import time

import emoji


def login():

    login_method = input(
        color.PURPLE
        + "\n-- Type "
        + color.BOLD
        + "[1]"
        + color.END
        + color.PURPLE
        + " to login via institution VPN/wifi\n-- Type "
        + color.BOLD
        + "[2]"
        + color.END
        + color.PURPLE
        + " to manually login via the JSTOR website\n   : "
        + color.END
    )

    return login_method


def proceed():

    proceed = input(
        color.PURPLE
        + "\n-- Type "
        + color.BOLD
        + "[1]"
        + color.END
        + color.PURPLE
        + " to continue\n-- Type "
        + color.END
        + color.PURPLE
        + color.BOLD
        + "[2]"
        + color.END
        + color.PURPLE
        + " to restart\n   : "
        + color.END
    )

    return proceed


def welcome():

    print(
        "\n\n\n" + color.BOLD + color.UNDERLINE + "Welcome to Aaron’s Kit!" + color.END
    )

    print(
        "\n"
        + color.ITALIC
        + "A tool that enables the effortless liberation of academic research."
        + color.END
    )

    time.sleep(2)

    print(
        "\nThe Aaron’s Kit Team understands that Open Access is not about competition \n- instead, it’s about coordination and driving a community corporation. \nThe key idea of Aaron’s Kit is accessibility in the highest order, and here \nwe hope to democratise knowledge by freely providing access to academic journals."
    )

    time.sleep(2)

    print(
        "\n"
        + color.ITALIC
        + "By using this tool, you are playing an active role in the open access movement! \nThank you for your contribution."
        + color.END
    )

    time.sleep(2)

    print(
        "\n\n\n"
        + emoji.emojize(":information:")
        + "   Please note that valid JSTOR login credentials are a requirement to use this tool."
        + color.END
    )

    print(
        "\n"
        + color.GREEN
        + color.UNDERLINE
        + "Before you start, ensure that you:"
        + color.END
    )

    print(
        "\n"
        + color.GREEN
        + "a) Have Google Chrome installed\nb) Have a stable internet connection\nc) Set your computer to never sleep and keep on charge\nd) Do not close the browser while the program is running\ne) Do not interfere with the browser while the program is running"
        + color.END
    )

    input(
        color.PURPLE
        + "\n-- Press "
        + color.BOLD
        + "ENTER/RETURN"
        + color.END
        + color.PURPLE
        + " to continue: "
        + color.END
    )


def main_menu():
    print(
        "\n"
        + emoji.emojize(":information:")
        + "   To Choose a login method, enter"
        + color.BOLD
        + " [1]"
        + color.END
    )

    print(
        "\n"
        + emoji.emojize(":information:")
        + "   To exit the program, enter"
        + color.BOLD
        + " [2]"
        + color.END
    )

    select = input(color.PURPLE + "\n-- Please enter your selection: " + color.END)

    return select


def typo():
    print(
        "\n"
        + emoji.emojize(":loudspeaker:")
        + color.YELLOW
        + "  It appears that you made a typo, you are being directed to the main selection menu"
        + color.END
    )

    time.sleep(1)

    main = main_menu()
    return main


class color:
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[95m"
    LIGHT_BLUE = "\033[1;34m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    ITALIC = "\x1B[3m"
    END = "\033[0m"
    LIGHT_GRAY = "\033[37m"
    DARK_GRAY = "\033[1;30m"
