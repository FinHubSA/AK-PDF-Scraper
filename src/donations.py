from termcolor import colored
import emoji
import platform
import json
from algosdk import account, encoding, mnemonic
import time
import os.path

system = platform.system()
# system = "Windows"

is_windows = False

if system == "Windows":
    is_windows = True


def donation_explainer(misc_directory):

    print("\n\nGreat! You are on your way to make a contribution!")
    print(
        "\nThe Open Access community really appreciates your work, and would like to thank you by donating ALGO to your Algorand account.\n"
    )
    print(colored("\nHow this works:", attrs=["bold", "underline"]))
    print(
        "\n• Aaron's Kit users donate ALGO. \n• After a set payout time period, the ALGO is aggregated and distributed to all Aaron's Kit contributors, like you. \n• The amount of ALGO you receive is weighted according to the number of papers you have scraped in the payout time period.\n• To receive ALGO, all you need is an Algorand account.\n"
    )

    user_address = donation_options(misc_directory)

    return user_address


def donation_options(misc_directory):

    global is_windows

    print(
        "\n"
        + (colored(" i ", "blue", attrs=["reverse"])) * (is_windows)
        + emoji.emojize(":information:") * (not is_windows)
        + "   Please read the following options carefully and make a selection"
    )

    donation_action = input(
        colored(
            "\n-- Type [1] if you want to receive donations and have an existing Algorand address"
            + "\n-- Type [2] if you want to receive donations and want to create a new Algorand account"
            + "\n-- Type [3] if you do not want to receive donations"
            + "\n   : ",
        )
    )

    if donation_action.strip() == "1":
        user_address = existing_account(misc_directory)
    elif donation_action.strip() == "2":
        user_address = create_account(misc_directory)
    elif donation_action.strip() == "3":
        user_address = ""
    else:
        print(
            "\n"
            + (colored(" ! ", "yellow", attrs=["reverse"])) * (is_windows)
            + emoji.emojize(":loudspeaker:") * (not is_windows)
            + colored("   Typo, try again.\n", "yellow")
        )
        return donation_options(misc_directory)

    return user_address


def existing_account(misc_directory):

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
            + colored(user_address, attrs=["bold"])
            + " is your current Algorand address "
            + colored("[Y/n]: ", attrs=["bold"])
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

                retry_address = "2"

            else:
                print(
                    "\n\n"
                    + colored(" ! ", "yellow", attrs=["reverse"]) * (is_windows)
                    + emoji.emojize(":loudspeaker:") * (not is_windows)
                    + colored("  This address is invalid.", "yellow")
                )

                retry_address_typo = True

                while retry_address_typo == True:

                    retry_address = input(
                        colored(
                            "\n-- Type [1] to retry"
                            + "\n-- Type [2] to create a new account"
                            + "\n   : ",
                        )
                    )

                    if retry_address.strip() == "1":

                        retry_address_typo = False

                    elif retry_address.strip() == "2":

                        time.sleep(2)

                        private_key, address = account.generate_account()

                        user_address = address

                        passphrase = mnemonic.from_private_key(private_key)

                        print(
                            colored("\n\nYour passphrase is: ", "green")
                            + colored(passphrase, "green", attrs=["bold"]),
                        )

                        print(
                            colored("\n\nYour address is: ", "green")
                            + colored(address, "green", attrs=["bold"]),
                        )

                        print(
                            "\n\n"
                            + colored(
                                "Please note the following information to keep your account details safe:",
                                attrs=["bold", "underline"],
                            )
                            + "\n\n• Make sure that you store your passphrase and address in a secure place."
                            + colored("\n• It is best practice ", attrs=["bold"])
                            + "to write your passphrase on a piece of paper and store it somewhere safe."
                            + colored("\n• It is not advised ", attrs=["bold"])
                            + "to store your passphrase on a device that has internet connectivity."
                        )

                        print(
                            "\n\n"
                            + (colored(" ! ", "green", attrs=["reverse"]))
                            * (is_windows)
                            + emoji.emojize(":check_mark_button:") * (not is_windows)
                            + colored(
                                "   You are all set up! You will receive ALGO into this address at the end of the donation period.",
                                "green",
                            )
                        )

                        retry_address_typo = False

                    else:

                        print(
                            "\n\n"
                            + colored(" ! ", "yellow", attrs=["reverse"]) * (is_windows)
                            + emoji.emojize(":loudspeaker:") * (not is_windows)
                            + colored(
                                "   It appears that you made a typo, please re-enter your selection.\n",
                                "yellow",
                            )
                        )

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
                "   You are all set up! You will receive ALGO into this address at the end of the donation period.",
                "green",
            )
        )
    else:
        print(
            "\n"
            + (colored(" ! ", "yellow", attrs=["reverse"])) * (is_windows)
            + emoji.emojize(":loudspeaker:") * (not is_windows)
            + colored("   Typo, try again.\n", "yellow")
        )

        existing_account(misc_directory)

    return user_address


def create_account(misc_directory):

    time.sleep(2)

    private_key, address = account.generate_account()

    user_address = address

    passphrase = mnemonic.from_private_key(private_key)

    print(
        colored("\n\nYour passphrase is: ", "green")
        + colored(passphrase, "green", attrs=["bold"]),
    )

    print(
        colored("\n\nYour address is: ", "green")
        + colored(address, "green", attrs=["bold"]),
    )

    print(
        "\n\n"
        + colored(
            "Please note the following information to keep your account details safe:",
            attrs=["bold", "underline"],
        )
        + "\n\n• Make sure that you store your passphrase and address in a secure place."
        + colored("\n• It is best practice ", attrs=["bold"])
        + "to write your passphrase on a piece of paper and store it somewhere safe."
        + colored("\n• It is not advised ", attrs=["bold"])
        + "to store your passphrase on a device that has internet connectivity."
    )

    print(
        "\n\n"
        + (colored(" ! ", "green", attrs=["reverse"])) * (is_windows)
        + emoji.emojize(":check_mark_button:") * (not is_windows)
        + colored(
            "   You are all set up! You will receive ALGO into this address at the end of the donation period.",
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


# misc_directory = "/Users/danaebouwer/Documents/Work/Aarons-kit/PDF_Scraper"
# algorandAddress = donation_explainer(misc_directory)
# print(algorandAddress)
