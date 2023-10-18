def calc_total(who):
    """Work out the player's total (dealer/player) taking Aces into account.
    The assumption is that the value of 'who' is a list of cards."""
    other_cards_total = 0
    aces_count = 0

    # Shape of card looks like this now: ('Ace of Diamonds', [[1, 11], 'ace_of_diamonds.png'])
    # or like this: ('10 of Spades', [10, '10_of_spades.png']).

    for card in who:
        if isinstance(card[-1][0], list):  # Do we have a list in a list?
            aces_count = aces_count + 1
        else:
            other_cards_total = other_cards_total + card[-1][0]

    if aces_count:
        # We have AT LEAST one Ace.
        if other_cards_total <= 10:
            if aces_count == 1:
                return other_cards_total + 11
            if aces_count == 2:
                if other_cards_total < 10:
                    return other_cards_total + 11 + 1
                else:
                    return other_cards_total + aces_count
            if aces_count == 3:
                if other_cards_total < 9:
                    return other_cards_total + 11 + 1 + 1
                else:
                    return other_cards_total + aces_count
            if aces_count == 4:
                if other_cards_total < 8:
                    return other_cards_total + 11 + 1 + 1 + 1
                else:
                    return other_cards_total + aces_count
        else:
            return other_cards_total + (aces_count)
    else:
        return other_cards_total
