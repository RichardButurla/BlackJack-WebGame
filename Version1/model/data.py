suits = ["Clubs", "Spades", "Hearts", "Diamonds"]  # List.
faces = ["Jack", "Queen", "King", "Ace"]
numbers = [2, 3, 4, 5, 6, 7, 8, 9, 10]


def init_deck_values():
    deck_values = {}  # Empty dictionary.

    for suit in suits:
        for face in faces + numbers:
            key = f"{face} of {suit}"
            png = key.lower().replace(" ", "_") + ".png"
            if face == "Ace":
                value = [1, 11]
            elif face in numbers:
                value = face
            else:
                value = 10
            deck_values[key] = [value, png]
    return deck_values


def make_deck():
    """Reset the deck of cards, returning a list
    which contains the 52 cards."""
    deck = []  # Empty list.
    for suit in suits:
        for face in faces + numbers:
            deck.append(f"{face} of {suit}")  # f-string.
    return deck
