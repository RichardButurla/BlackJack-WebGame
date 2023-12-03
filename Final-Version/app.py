import random
import DBcm
from flask import Flask, render_template, request, session
from model.data import make_deck, init_deck_values
from calcs import calc_total

app = Flask(__name__)
app.secret_key = "kfke hrt'oerj erterutv'rtjv 'oieqrut0345uv 0'34qutv0rutv 'eqrutv equeqtr' u"
deck_values = init_deck_values()

credentials = {
    "host": "localhost",
    "database": "BlackjackDB",
    "user": "richard",
    "password": "richpassword"
}

class DatabaseManager:
    """Handles the update and insertion of our data"""
    @staticmethod
    def insert_game_data(user, game_outcome):

        DatabaseManager.check_valid_user(user)

        with DBcm.UseDatabase(credentials) as database:
            SQL = """ 
                insert into user_game_statistics
                (user, outcomes)
                values
                (%s , %s)
            """
            database.execute(SQL,(user,game_outcome,))

        DatabaseManager.update_database(user)

    @staticmethod
    def check_valid_user(user):
        with DBcm.UseDatabase(credentials) as database:
            SQL = """
                select distinct user from user_statistics 
                where user = %s
            """
            database.execute(SQL, (user,))
            returned_user = database.fetchone()

            # If the user doesn't exist, insert a default record
            if returned_user == None:
                default_insert_SQL = """
                    insert into user_statistics (user, win_rate, bust_rate, highest_win_streak)
                    values (%s, 0, 0, 0)
                """
                database.execute(default_insert_SQL, (user,))

    @staticmethod
    def update_database(user):
        with DBcm.UseDatabase(credentials) as database:

            SQL = """
                update user_statistics
                set win_rate = %s,
                    bust_rate = %s,
                    highest_win_streak = %s
                where user = %s
            """

            wins = DatabaseManager.get_numbered_user_data_from_table(user, "Win", "user_game_statistics")
            losses = DatabaseManager.get_numbered_user_data_from_table(user, "Loss", "user_game_statistics")
            busts = DatabaseManager.get_numbered_user_data_from_table(user, "Bust", "user_game_statistics")
            draws = DatabaseManager.get_numbered_user_data_from_table(user, "Draw", "user_game_statistics")

            total_games = wins + losses + busts + draws
            win_rate = wins / total_games
            bust_rate = busts / total_games
            highest_win_streak = DatabaseManager.get_highest_win_streak(user)

            database.execute(SQL,(win_rate,bust_rate,highest_win_streak,user,))

    @staticmethod
    def get_highest_win_streak(user):
        results = []
        highest_win_streak = 0
        current_streak_count = 0

        with DBcm.UseDatabase(credentials) as database:
            
            SQL = """
                select * from user_game_statistics 
                where user = %s
            """
            database.execute(SQL,(user,))
            results = database.fetchall()

        for result in results:
            if result[1] == "Win":
                current_streak_count = current_streak_count + 1
            else:
                if current_streak_count > highest_win_streak: 
                    highest_win_streak = current_streak_count
                current_streak_count = 0 

        # Check after the loop for any ongoing winning streak
        if current_streak_count > highest_win_streak:
            highest_win_streak = current_streak_count
        
        return highest_win_streak
            
    @staticmethod
    def get_detailed_user_data_from_table(user, data, table):
        with DBcm.UseDatabase(credentials) as database:
            SQL = f"""
                select {data} from {table}
                where user = '{user}'
            """
            database.execute(SQL)
            results = database.fetchone()
            return results[0]
        
    @staticmethod
    def get_numbered_user_data_from_table(user, data, table):
        with DBcm.UseDatabase(credentials) as database:
            SQL = f"""
                select count(*) from {table}
                where user = '{user}' and outcomes = '{data}'
            """
            database.execute(SQL)
            results = database.fetchone()
            return results[0]



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
        if not SessionManager.get("is_game_over"):
            while calc_total(SessionManager.get("dealer")) < 17:
                SessionManager.get("dealer").append(self.draw())
            self.check_end_game_logic()

    @classmethod
    def check_start_game_logic(self, player_total, dealer_total):
        if player_total == 21:
            SessionManager.set("dealer_card_is_hidden", False)
            if dealer_total == 21:
                SessionManager.set("game_status", "It's a BlackJack Tie!")
                SessionManager.set("is_game_over", True)
                DatabaseManager.insert_game_data(SessionManager.get("user"), "Draw")
            else:
                SessionManager.set("game_status", "Player hit BlackJack!")
                SessionManager.set("is_game_over", True)
                DatabaseManager.insert_game_data(SessionManager.get("user"), "Win")

    @classmethod
    def check_end_game_logic(self):
        player_total = calc_total(SessionManager.get("player"))
        dealer_total = calc_total(SessionManager.get("dealer"))

        SessionManager.set("dealer_card_is_hidden", False)  # Reveal dealer card


        if dealer_total == 21 and len(SessionManager.get("dealer")) == 2:
            SessionManager.set("game_status", "Dealer has BlackJack!")
            SessionManager.set("is_game_over", True)
            DatabaseManager.insert_game_data(SessionManager.get("user"), "Loss")
        elif dealer_total < 17:
            self.dealer_hit()
        elif dealer_total > 21:
            SessionManager.set("dealer_hidden_card", SessionManager.get("dealer")[1][-1][-1])
            SessionManager.set("game_status", "Dealer Bust!")
            SessionManager.set("is_game_over", True)
            DatabaseManager.insert_game_data(SessionManager.get("user"), "Win")
        # If neither busts nor gets BlackJack, compare the totals
        else:
            if player_total > dealer_total:
                SessionManager.set("game_status", "Player Wins!")
                DatabaseManager.insert_game_data(SessionManager.get("user"), "Win")
            elif dealer_total > player_total:
                SessionManager.set("game_status", "Dealer Wins!")
                DatabaseManager.insert_game_data(SessionManager.get("user"), "Loss")
            else:
                SessionManager.set("game_status", "It's a Tie!")
                DatabaseManager.insert_game_data(SessionManager.get("user"), "Draw")
            SessionManager.set("is_game_over", True)


    @classmethod
    def player_hit(self):
        if not SessionManager.get("is_game_over"):
            SessionManager.get("player").append(self.draw())
            if calc_total(SessionManager.get("player")) <= 21:
                SessionManager.set("game_status", "Hit or Stand?")
            else:
                SessionManager.set("game_status", "Player Bust!")
                SessionManager.set("is_game_over", True)
                DatabaseManager.insert_game_data(SessionManager.get("user"), "Bust")

    @classmethod
    def start_game(self):
        SessionManager.set("user", "Reacu")
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


def render_game_template(templateName):
    """Render the game template with the required context."""
    dealer_cards = SessionManager.get("dealer")
    dealer_hidden_total = BlackjackGame.get_dealer_hidden_total(dealer_cards[0][1][0])
    return render_template(
        templateName,
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
    return render_game_template("start.html")


@app.post("/stand")
def over_to_the_dealer():
    BlackjackGame.dealer_hit()
    return render_game_template("start.html")


@app.post("/hit")
def select_another_card():
    BlackjackGame.player_hit()
    return render_game_template("start.html")


@app.post("/restart")
def restart():
    BlackjackGame.start_game()
    return render_game_template("start.html")


if __name__ == "__main__":
    app.run(debug=True)
