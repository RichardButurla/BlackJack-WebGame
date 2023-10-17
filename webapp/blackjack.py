import random
import time

## import data  # Makes sure you put data. in front of all function calls.

from model.data import make_deck, init_deck_values
## from calcs import calc_total, determine_ace_value
## from view.ui import display_cards


deck_values = init_deck_values()


def draw():
    """Select a random card from the deck. The deck shrinks by 1."""
    selection = random.choice(deck)
    deck.remove(selection)
    return selection, deck_values[selection]


def display_status():
    return f"""
    Here are your cards: {display_cards(player)}

    Here is your current score: {calc_total(player)}

    Here is the dealer's card: {dealer[0][0]}

    What's next?  Hit or Stand? 
    """


def add_card(who):
    """Given a player or dealer list, add another card to the list."""
    selection = draw()
    if isinstance(selection[-1], list):
        who.append((selection[0], determine_ace_value(who)))  # We have an Ace.
    else:
        who.append(selection)


deck = make_deck()


player = []
dealer = []

player.append(draw())
dealer.append(draw())
player.append(draw())
dealer.append(draw())


if __name__ == "__main__":  # Is Python running directly (or imported)?
    while True:
        print(display_status())
        choice = input("Press 'h' or 's' to continue")

        if choice in ["h", "H"]:
            add_card(player)
            if calc_total(player) >= 21:
                break
        elif choice in ["s", "S"]:
            break
        else:
            print("Whoops! That's not an option here. Please choose 'h' or 's'.")

    keep_playing = True
    if calc_total(player) > 21:
        print(display_status())
        print("Your score is over 21. You're busted!")
        keep_playing = False
    elif calc_total(player) == 21:
        print(display_status())
        print("Congrats! You have a score of 21.")
    else:
        print("Current state of game:")
        print(display_status())

    if keep_playing:
        while True:
            if calc_total(dealer) >= 17:
                break
            print("Here are the dealer's cards:")
            print(display_cards(dealer))
            add_card(dealer)
            if calc_total(dealer) > 21:
                print("The player wins, dealer loses.")
                break
            elif calc_total(dealer) >= 17:
                break
            time.sleep(1)
    else:
        print("Dealer wins.")

    print("\nDealer:", display_cards(dealer), "worth ", calc_total(dealer))
    print("\nPlayer:", display_cards(player), "worth ", calc_total(player))
