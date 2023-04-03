import emoji
import json
import time
import os.path

from algosdk import account, encoding, mnemonic
from termcolor import colored
from src.errors import MainException, TypoException

from src.helpers import system, print_typo, get_user_address_from_json
from src.temp_storage import misc_path

is_windows = system()
misc_directory = misc_path()


def print_donation_explainer():

    print("\n\nGreat! You are on your way to make a contribution!")

    print("\n\n" + colored("Receive donations", attrs=["reverse"]))

    print(
        "\n\nThe Open Access community really appreciates your work, and would like to thank you by donating ALGO to your Algorand account.\n"
    )
    print(
        colored("\nHow this works:", attrs=["reverse"]) * (is_windows)
        + colored("\nHow this works:", attrs=["bold", "underline"]) * (not is_windows)
    )
    print(
        "\n• Aaron's Kit users donate ALGO. \n• After a set payout time period, the ALGO is aggregated and distributed to all Aaron's Kit contributors, like you. \n• The amount of ALGO you receive is weighted according to the total number of papers you have scraped.\n• To receive ALGO, all you need is an Algorand account.\n"
    )


def receive_donation_action():

    print(
        "\n"
        + (colored(" i ", "blue", attrs=["reverse"])) * (is_windows)
        + emoji.emojize(":information:") * (not is_windows)
        + "   Please read the following options carefully and make a selection."
    )

    donation_action = get_input(
        colored(
            "\n-- Type [1] to use your existing Algorand address to receive donations"
            + "\n-- Type [2] to create a new Algorand address to receive donations"
            + "\n-- Type [3] to skip this section and receive no donations"
            + "\n-- Type [4] to return to main menu"
            + "\n   : ",
        )
    )

    try:
        user_address = process_donation_action(donation_action)
    except TypoException:
        return receive_donation_action()

    return user_address


def process_donation_action(donation_action):

    if donation_action == "1":

        try:

            user_address = check_address_on_record()

        except TypoException:
            return process_donation_action(donation_action)

    elif donation_action == "2":
        time.sleep(1)
        passphrase, user_address = create_account()
        display_account_created(passphrase, user_address)
    elif donation_action == "3":

        print(
            "\n\n"
            + (colored(" ! ", "green", attrs=["reverse"])) * (is_windows)
            + emoji.emojize(":check_mark_button:") * (not is_windows)
            + colored(
                "   You will contribute papers without receiving any ALGO donations. If you change your mind, you can create or add an account later.",
                "green",
            )
        )

        user_address = None

    elif donation_action == "4":
        raise MainException()
    else:
        print_typo()
        raise TypoException()

    return user_address


def receive_not_validated_action():

    retry_account_action = get_input(
        colored(
            "\n-- Type [1] to retry"
            + "\n-- Type [2] to create a new account"
            + "\n-- Type [3] to return to donations menu"
            + "\n   : ",
        )
    )

    try:
        user_address = process_validation_action(retry_account_action)
    except TypoException:
        return receive_not_validated_action()

    return user_address


def process_validation_action(retry_account_action):

    if retry_account_action == "1":
        user_address = validate_existing_account()
        return user_address
    elif retry_account_action == "2":
        time.sleep(1)
        passphrase, user_address = create_account()
        display_account_created(passphrase, user_address)
        return user_address
    elif retry_account_action == "3":
        receive_donation_action()
    else:
        print_typo()
        raise TypoException


def validate_existing_account():

    user_address = get_input(
        "\n\n"
        + (colored(" i ", "blue")) * (is_windows)
        + emoji.emojize(":information:") * (not is_windows)
        + "   Please enter your Algorand address: "
    )

    if encoding.is_valid_address(user_address):

        print(
            "\n\n"
            + (colored(" ! ", "green", attrs=["reverse"])) * (is_windows)
            + emoji.emojize(":check_mark_button:") * (not is_windows)
            + colored(
                "   This address is valid! We will keep it on record for future contributions.",
                "green",
            )
        )

        print(
            "\n"
            + (colored(" ! ", "green", attrs=["reverse"])) * (is_windows)
            + emoji.emojize(":check_mark_button:") * (not is_windows)
            + colored(
                "   You are all set up! You will receive ALGO into this address at the end of the donation period.",
                "green",
            )
        )

        store_address(user_address)

    else:

        print(
            "\n\n"
            + colored(" ! ", "yellow", attrs=["reverse"]) * (is_windows)
            + emoji.emojize(":loudspeaker:") * (not is_windows)
            + colored("   This address is invalid.\n", "yellow")
        )

        user_address = receive_not_validated_action()

    return user_address


def check_address_on_record():

    user_address_dict = get_user_address_from_json(misc_directory)

    if user_address_dict["address"] != "":

        user_address = user_address_dict["address"]

        correct_address = get_input(
            "\n\n"
            + (colored(" i ", "blue", attrs=["reverse"])) * (is_windows)
            + emoji.emojize(":information:") * (not is_windows)
            + "   We have an existing address on record for you."
            + "\n\n\nPlease confirm that "
            + colored(user_address, attrs=["reverse"]) * (is_windows)
            + colored(user_address, attrs=["bold"]) * (not is_windows)
            + " is your current Algorand address "
            + colored("[y/n]: ") * (is_windows)
            + colored("[y/n]: ", attrs=["bold"]) * (not is_windows)
        )

        if correct_address == "y" or correct_address == "Y":
            print(
                "\n\n"
                + (colored(" ! ", "green", attrs=["reverse"])) * (is_windows)
                + emoji.emojize(":check_mark_button:") * (not is_windows)
                + colored(
                    "   You are all set up! You will receive ALGO into this address at the end of the donation period.",
                    "green",
                )
            )

        else:
            user_address = validate_correct_address(correct_address)

    else:
        user_address = validate_correct_address("n")

    return user_address


def validate_correct_address(correct_address):

    if correct_address == "n" or correct_address == "N":
        user_address = validate_existing_account()
    else:
        print_typo()
        raise TypoException

    return user_address


def create_account():

    private_key, user_address = account.generate_account()

    passphrase = mnemonic.from_private_key(private_key)

    store_address(user_address)

    return passphrase, user_address


def store_address(user_address):

    user_address_dict = get_user_address_from_json(misc_directory)

    user_address_dict["address"] = user_address

    # store the address
    with open(os.path.join(misc_directory, "address.json"), "w") as f:
        json.dump(user_address_dict, f, indent=4, sort_keys=True)

    f.close()


def display_account_created(passphrase, user_address):

    print(
        "\n\n"
        + (colored(" i ", "blue", attrs=["reverse"])) * (is_windows)
        + emoji.emojize(":information:") * (not is_windows)
        + colored("   We are creating your Algorand account.")
    )

    time.sleep(1)

    print(
        "\n\n"
        + colored(
            "Please note the following information to keep your account details safe:",
            attrs=["reverse"],
        )
        * (is_windows)
        + colored(
            "Please note the following information to keep your account details safe:",
            attrs=["bold", "underline"],
        )
        * (not is_windows)
        + "\n\n• Make sure that you store your passphrase and address in a secure place."
        + "\n• It is best practice to write your passphrase on a piece of paper and store it somewhere safe."
        + "\n• It is not advised to store your passphrase on a device that has internet connectivity."
    )

    get_input(
        colored("\n\n-- Press ")
        + colored("ENTER/RETURN", attrs=["reverse"]) * (is_windows)
        + colored("ENTER/RETURN", attrs=["bold"]) * (not is_windows)
        + colored(" to view your passphrase and address: ")
    )

    print(
        colored("\n\nYour address is: ") + user_address,
    )

    print(
        colored("\n\nYour passphrase is: ") + passphrase,
    )

    print(
        "\n\n"
        + (colored(" i ", "blue", attrs=["reverse"])) * (is_windows)
        + emoji.emojize(":information:") * (not is_windows)
        + "   Remember to store this address and passphrase in a secure place."
    )

    print(
        "\n"
        + (colored(" ! ", "green", attrs=["reverse"])) * (is_windows)
        + emoji.emojize(":check_mark_button:") * (not is_windows)
        + colored(
            "   You are all set up! You will receive ALGO into this address at the end of the donation period.",
            "green",
        )
    )


def get_input(text):
    return input(text).strip()
