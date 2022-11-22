from termcolor import colored
import emoji
import platform
import json

system = platform.system()
# system = "Windows"

is_windows = False

if system == "Windows":
    is_windows = True


def donation_explainer():

    print("\n\nGreat! You are on your way to make a contribution!")
    print(
        "\nThe Open Access community really appreciates your work, and would like to thank you by donating ALGO to your Algorand account.\n"
    )
    print(colored("\nHow this works:", attrs=["bold", "underline"]))
    print(
        "\n• Aaron's Kit users donate ALGO. \n• After a set payout time period, the ALGO is aggregated and distributed to all Aaron's Kit contributors, like you. \n• The amount of ALGO you receive is weighted according to the number of papers you have scraped in the payout time period.\n• To receive ALGO, all you need is an Algorand account.\n"
    )

    donation_options()


def donation_options():
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
        existing_account()
    elif donation_action.strip() == "2":
        create_account()
    elif donation_action.strip() == "3":
        return
    else:
        print(
            "\n"
            + (colored(" ! ", "yellow", attrs=["reverse"])) * (is_windows)
            + emoji.emojize(":loudspeaker:") * (not is_windows)
            + colored("   Typo, try again.\n", "yellow")
        )
        return donation_options()


def existing_account():

    with open("address.json", "r") as f:

        user_address_dict = json.load(f)

    f.close()

    have_address = "n"

    if user_address_dict != "{}":

        user_address = user_address_dict["address"]

        have_address = input(
            "\n\nWe have your existing address on record, please confirm that "
            + colored(user_address, attrs=["bold"])
            + " is your current Algorand address "
            + colored("[Y/n]: ", attrs=["bold"])
        )

        if have_address.strip() == "n":

            user_address = input("\n\nPlease enter your Algorand address: ")

            # confirm that address is valid

            user_address_dict["address"] = user_address

            # store the address
            with open("address.json", "w") as f:
                json.dump(user_address_dict, f, indent=4, sort_keys=True)

            f.close()


def create_account():

    # guide user to create an account
    print("works")

    # return user account and passphrase

    # store the address


donation_explainer()
