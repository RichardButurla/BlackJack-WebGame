import random
from flask import Flask, render_template, request, session
from model.data import make_deck, init_deck_values
from calcs import calc_total

app = Flask(__name__)
app.secret_key = "kfke hrt'oerj erterutv'rtjv 'oieqrut0345uv 0'34qutv0rutv 'eqrutv equeqtr' u"
deck_values = init_deck_values()


class SessionManager:
    """Handles session operations for the game."""

    @staticmethod
    def set(key, value):
        session[key] = value

    @staticmethod
    def get(key):
        return session.get(key)


class BlackjackGame:
    """Represents the core game logic of Blackjack."""

    @staticmethod
    def draw():
        selection = random.choice(SessionManager.get("deck"))
        SessionManager.get("deck").remove(selection)
        session.modified = True
        return selection, deck_values[selection]

    @classmethod
    def dealer_action(self):
        while calc_total(SessionManager.get("dealer")) < 17:
            SessionManager.get("dealer").append(self.draw())

    @classmethod
    def dealer_hit(self):
        while calc_total(SessionManager.get("dealer")) < 17:
            SessionManager.get("dealer").append(self.draw())
        self.check_end_game_logic()

    @classmethod
    def check_start_game_logic(self, player_total, dealer_total):
        if player_total == 21:
            SessionManager.set("dealer_card_is_hidden", False)
            if dealer_total == 21:
                SessionManager.set("game_status", "It's a BlackJack Tie!")
            elif dealer_total < 17:
                self.dealer_hit()
                self.check_end_game_logic()
            elif dealer_total < player_total:
                SessionManager.set("game_status", "Player hit BlackJack!")
                SessionManager.set("is_game_over", True)

    @classmethod
    def check_end_game_logic(self):
        player_total = calc_total(SessionManager.get("player"))
        dealer_total = calc_total(SessionManager.get("dealer"))

        SessionManager.set("dealer_card_is_hidden", False)  # Reveal dealer card

        # If player hits BlackJack
        if player_total == 21:
            if dealer_total == 21:
                SessionManager.set("game_status", "Black Jack Tie!")
            elif dealer_total < 17:
                self.dealer_hit()
            else:
                SessionManager.set("game_status", "Player hit BlackJack!")
                SessionManager.set("is_game_over", True)

        # If dealer hits BlackJack but player doesn't
        elif dealer_total == 21:
            SessionManager.set("game_status", "Dealer hit BlackJack!")
            SessionManager.set("is_game_over", True)

        # If player or dealer goes bust
        elif player_total > 21:
            SessionManager.set("dealer_hidden_card", SessionManager.get("dealer")[1][-1][-1])
            SessionManager.set("game_status", "Player Bust!")
            SessionManager.set("is_game_over", True)

        elif dealer_total > 21:
            SessionManager.set("dealer_hidden_card", SessionManager.get("dealer")[1][-1][-1])
            SessionManager.set("game_status", "Dealer Bust!")
            SessionManager.set("is_game_over", True)

        # If neither busts nor gets BlackJack, compare the totals
        else:
            if player_total > dealer_total:
                SessionManager.set("game_status", "Player Wins!")
            elif dealer_total > player_total:
                SessionManager.set("game_status", "Dealer Wins!")
            else:
                SessionManager.set("game_status", "It's a Tie!")
            SessionManager.set("is_game_over", True)

    @classmethod
    def player_hit(self):
        if not SessionManager.get("is_game_over"):
            SessionManager.get("player").append(self.draw())
            if calc_total(SessionManager.get("player")) < 21:
                SessionManager.set("game_status", "Hit or Stand?")
            else:
                self.check_end_game_logic()

    @classmethod
    def start_game(self):
        SessionManager.set("deck", make_deck())
        SessionManager.set("player", [self.draw() for _ in range(2)])
        SessionManager.set("dealer", [self.draw() for _ in range(2)])
        SessionManager.set("dealer_card_is_hidden", True)
        SessionManager.set("game_status", "")
        SessionManager.set("is_game_over", False)
        self.check_start_game_logic(calc_total(SessionManager.get("player")), calc_total(SessionManager.get("dealer")))
        
    @classmethod
    def get_dealer_hidden_total(self, dealer_hidden_total):
        if isinstance(dealer_hidden_total,list):
            return dealer_hidden_total[1]
        else:
            return dealer_hidden_total


def render_game_template():
    """Render the game template with the required context."""
    dealer_cards = SessionManager.get("dealer")
    dealer_hidden_total = BlackjackGame.get_dealer_hidden_total(dealer_cards[0][1][0])
    return render_template(
        "start.html",
        player_cards=SessionManager.get("player"),
        player_total=calc_total(SessionManager.get("player")),
        dealer_cards=SessionManager.get("dealer"),
        dealer_card_is_hidden=SessionManager.get("dealer_card_is_hidden"),
        dealer_total=calc_total(SessionManager.get("dealer")),
        dealer_hidden_total=dealer_hidden_total,
        title="",
        header="",
        footer="",
        number_of_cards=len(SessionManager.get("deck")),
        game_status=SessionManager.get("game_status"),
        is_game_over=SessionManager.get("is_game_over")
    )


@app.get("/")
@app.get("/start")
def display_opening_state():
    BlackjackGame.start_game()
    return render_game_template()


@app.post("/stand")
def over_to_the_dealer():
    BlackjackGame.dealer_hit()
    return render_game_template()


@app.post("/hit")
def select_another_card():
    BlackjackGame.player_hit()
    return render_game_template()


@app.post("/restart")
def restart():
    BlackjackGame.start_game()
    return render_game_template()


if __name__ == "__main__":
    app.run(debug=True)
