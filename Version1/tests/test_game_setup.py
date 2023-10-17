from blackjack import player, dealer
from calcs import calc_total
from model.data import init_deck_values, make_deck


def test_two_cards_each():
    assert len(player) == 2
    assert len(dealer) == 2


def test_nobody_bust():
    assert calc_total(player) <= 21
    assert calc_total(dealer) <= 21


def test_decks_correct_types():
    assert isinstance(init_deck_values(), dict)
    assert isinstance(make_deck(), list)


def test_decks_size_ok():
    assert len(init_deck_values()) == 52
    assert len(make_deck()) == 52


def test_first_and_last():
    keys = list(init_deck_values().keys())
    values = list(init_deck_values().values())
    list_deck = make_deck()
    assert keys[0] == list_deck[0]
    assert keys[-1] == list_deck[-1]
    assert values[0][0] > 0
    assert values[-1][0] > 0
