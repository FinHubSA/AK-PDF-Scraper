from termcolor import colored
import emoji
import json
from algosdk import account, encoding, mnemonic
import time
import os.path

from src.helpers import system, typo
from src.temp_storage import misc_path

is_windows = system()


def donation_explainer():

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

    user_address = donation_options()

    return user_address


def donation_options():

    print(
        "\n"
        + (colored(" i ", "blue", attrs=["reverse"])) * (is_windows)
        + emoji.emojize(":information:") * (not is_windows)
        + "   Please read the following options carefully and make a selection"
    )

    donation_action = input(
        colored(
            "\n-- Type [1] if you want to receive donations and have an existing Algorand address"
            + "\n-- Type [2] if you want to receive donations and want to create a new Algorand address"
            + "\n-- Type [3] if you do not want to receive donations"
            + "\n-- Type [4] to return to main menu"
            + "\n   : ",
        )
    )

    if donation_action.strip() == "1":
        user_address = existing_account()
    elif donation_action.strip() == "2":
        user_address = create_account()
    elif donation_action.strip() == "3":

        print(
            "\n\n"
            + (colored(" ! ", "green", attrs=["reverse"])) * (is_windows)
            + emoji.emojize(":check_mark_button:") * (not is_windows)
            + colored(
                "  You will contribute papers without receiving any ALGO donations. If you change your mind, you can create or add an account later.",
                "green",
            )
        )

        user_address = None
    elif donation_action.strip() == "4":
        user_address = ""
    else:

        typo()

        return donation_options()

    return user_address


def existing_account():

    is_windows = system()

    misc_directory = misc_path()

    with open(os.path.join(misc_directory, "address.json"), "r") as f:

        user_address_dict = json.load(f)

    f.close()

    if user_address_dict != {}:

        user_address = user_address_dict["address"]

        have_address = input(
            "\n\n"
            + (colored(" i ", "blue", attrs=["reverse"])) * (is_windows)
            + emoji.emojize(":information:") * (not is_windows)
            + "   We have an existing address on record for you."
            + "\n\n\nPlease confirm that "
            + colored(user_address, attrs=["reverse"]) * (is_windows)
            + colored(user_address, attrs=["bold"]) * (not is_windows)
            + " is your current Algorand address "
            + colored("[Y/n]: ") * (is_windows)
            + colored("[Y/n]: ", attrs=["bold"]) * (not is_windows)
        )

    else:
        have_address = "n"

    if have_address.strip() == "n":

        retry_address = "1"

        while retry_address.strip() == "1":

            user_address = input(
                "\n\n"
                + (colored(" i ", "blue", attrs=["reverse"])) * (is_windows)
                + emoji.emojize(":information:") * (not is_windows)
                + "   Please enter your Algorand address: "
            ).strip()

            if encoding.is_valid_address(user_address):
                print(
                    "\n\n"
                    + (colored(" ! ", "green", attrs=["reverse"])) * (is_windows)
                    + emoji.emojize(":check_mark_button:") * (not is_windows)
                    + colored(
                        "  This address is valid! We will keep it on record for future contributions.",
                        "green",
                    )
                )

                print(
                    "\n"
                    + (colored(" ! ", "green", attrs=["reverse"])) * (is_windows)
                    + emoji.emojize(":check_mark_button:") * (not is_windows)
                    + colored(
                        "  You are all set up! You will receive ALGO into this address at the end of the donation period.",
                        "green",
                    )
                )

                retry_address = "2"

            else:
                print(
                    "\n\n"
                    + colored(" ! ", "yellow", attrs=["reverse"]) * (is_windows)
                    + emoji.emojize(":loudspeaker:") * (not is_windows)
                    + colored("  This address is invalid.\n", "yellow")
                )

                retry_address_typo = True

                while retry_address_typo == True:

                    retry_address = input(
                        colored(
                            "\n-- Type [1] to retry"
                            + "\n-- Type [2] to create a new account"
                            + "\n-- Type [3] to go back to donations menu"
                            + "\n   : ",
                        )
                    )

                    if retry_address.strip() == "1":

                        retry_address_typo = False

                    elif retry_address.strip() == "2":

                        user_address = create_account()

                        retry_address_typo = False

                    elif retry_address.strip() == "3":

                        donation_options()

                        retry_address_typo = False

                    else:

                        typo()

        user_address_dict["address"] = user_address

        # store the address
        with open(os.path.join(misc_directory, "address.json"), "w") as f:
            json.dump(user_address_dict, f, indent=4, sort_keys=True)

        f.close()

        return user_address

    elif have_address.strip() == "Y":
        print(
            "\n\n"
            + (colored(" ! ", "green", attrs=["reverse"])) * (is_windows)
            + emoji.emojize(":check_mark_button:") * (not is_windows)
            + colored(
                "  You are all set up! You will receive ALGO into this address at the end of the donation period.",
                "green",
            )
        )

    else:

        typo()

        existing_account()

    return user_address


def create_account():

    is_windows = system()

    misc_directory = misc_path()

    time.sleep(2)

    private_key, address = account.generate_account()

    user_address = address

    passphrase = mnemonic.from_private_key(private_key)

    print(
        "\n\n"
        + (colored(" i ", "blue", attrs=["reverse"])) * (is_windows)
        + emoji.emojize(":information:") * (not is_windows)
        + colored("   We are creating your Algorand account.")
    )

    time.sleep(2)

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
        + colored("\n• It is best practice ")
        + "to write your passphrase on a piece of paper and store it somewhere safe."
        + colored("\n• It is not advised ")
        + "to store your passphrase on a device that has internet connectivity."
    )

    input(
        colored("\n\n-- Press ")
        + colored("ENTER/RETURN", attrs=["reverse"]) * (is_windows)
        + colored("ENTER/RETURN", attrs=["bold"]) * (not is_windows)
        + colored(" to view your passphrase and address: ")
    )

    print(
        colored("\n\nYour passphrase is: ") + passphrase,
    )

    print(
        colored("\n\nYour address is: ") + address,
    )

    print(
        "\n\n"
        + (colored(" ! ", "green", attrs=["reverse"])) * (is_windows)
        + emoji.emojize(":check_mark_button:") * (not is_windows)
        + colored(
            "  You are all set up! You will receive ALGO into this address at the end of the donation period.",
            "green",
        )
    )

    with open(os.path.join(misc_directory, "address.json"), "r") as f:

        user_address_dict = json.load(f)

    user_address_dict["address"] = user_address

    # store the address
    with open(os.path.join(misc_directory, "address.json"), "w") as f:
        json.dump(user_address_dict, f, indent=4, sort_keys=True)

    f.close()

    return user_address
