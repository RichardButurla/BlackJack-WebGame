from calcs import calc_total


def test_not_busted():
    cards = [
        ("10 of Clubs", [10, "10_of_clubs.png"]),
        ("10 of Hearts", [10, "10_of_hearts.png"]),
        ("Ace of Spades", [[1, 11], "ace_of_spades.png"]),
    ]
    assert calc_total(cards) == 21


def test_busted():
    cards = [
        ("10 of Clubs", [10, "10_of_clubs.png"]),
        ("Jack of Hearts", [10, "jack_of_hearts.png"]),
        ("2 of Spades", [2, "2_of_hearts.png"]),
    ]
    assert calc_total(cards) > 21


def test_dealer_wins():
    dealer = [
        ("10 of Clubs", [10, "10_of_clubs.png"]),
        ("10 of Hearts", [10, "10_of_hearts.png"]),
        ("Ace of Spades", [[1, 11], "ace_of_spades.png"]),
    ]
    player = [
        ("3 of Spaces", [3, "3_of_spades.png"]),
        ("Queen of Hearts", [10, "10_of_hearts.png"]),
        ("2 of Diamonds", [2, "2_of_diamonds.png"]),
    ]
    assert calc_total(dealer) > calc_total(player)


def test_dealer_loses():  # i.e., player wins
    player = [
        ("10 of Clubs", [10, "10_of_clubs.png"]),
        ("10 of Hearts", [10, "10_of_hearts.png"]),
        ("Ace of Spades", [[1, 11], "ace_of_spades.png"]),
    ]
    dealer = [
        ("3 of Spaces", [3, "3_of_spades.png"]),
        ("Queen of Hearts", [10, "10_of_hearts.png"]),
        ("2 of Diamonds", [2, "2_of_diamonds.png"]),
    ]
    assert calc_total(dealer) < calc_total(player)


def test_drawn_game():
    dealer = [
        ("10 of Clubs", [10, "10_of_clubs.png"]),
        ("10 of Hearts", [10, "10_of_hearts.png"]),
        ("Ace of Spades", [[1, 11], "ace_of_spades.png"]),
    ]
    player = [
        ("Ace of Hearts", [[1, 11], "ace_of_hearts.png"]),
        ("10 of Spades", [10, "10_of_spades.png"]),
    ]
    assert calc_total(dealer) == calc_total(player)


def test_two_aces():
    cards = [
        ("10 of Clubs", [10, "10_of_clubs.png"]),
        ("Ace of Hearts", [[1, 11], "ace_of_hearts.png"]),
        ("Ace of Spades", [[1, 11], "ace_of_spades.png"]),
    ]
    assert calc_total(cards) == 12
