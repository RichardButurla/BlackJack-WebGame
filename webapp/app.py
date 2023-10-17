import random

from model.data import make_deck, init_deck_values
from calcs import calc_total

from flask import Flask, render_template, request, session

app = Flask(__name__)


app.secret_key = (
    "kfke hrt'oerj erterutv'rtjv 'oieqrut0345uv 0'34qutv0rutv 'eqrutv equeqtr' u"
)

# Global data.
deck_values = init_deck_values()


def draw():
    """Select a random card from the deck. The deck shrinks by 1."""
    selection = random.choice(session["deck"])
    session["deck"].remove(selection)
    session.modified = True
    return selection, deck_values[selection]

def dealer_action():
    while calc_total(session["dealer"]) < 17:
        session["dealer"].append(draw())

    player_total = calc_total(session["player"])
    dealer_total = calc_total(session["dealer"])    
    

def check_start_game_logic(player_total,dealer_total,dealer_hidden_card):

    if player_total == 21:
        #Blackjack
        dealer_hidden_card = "dealer[1][-1][-1]"
        #now check dealer total
        if(dealer_total == 21):
            session["game_status"] = "Its a BlackJack Tie!"
            pass
        elif(dealer_total < 17):
            dealer_hit()
            pass

def check_end_game_logic():

    if calc_total(session["player"]) == 21:
        #check if dealer is still less than 17
        if(calc_total(session["dealer"]) < 17):
            dealer_hit()
        elif calc_total(session["dealer"]) == 21:
            session["game_status"] = "Black Jack Tie!"
    if calc_total(session["dealer"]) == 21:
        session["game_status"] = "Dealer hit BlackJack!"
    elif calc_total(session["player"]) > 21:  # Player busts
         session["dealer_hidden_card"] = session["dealer"][1][-1][-1]
         session["game_status"] = "Player Bust!"
    elif calc_total(session["dealer"]) > 21:  # Dealer busts
         session["dealer_hidden_card"] = session["dealer"][1][-1][-1]
         session["game_status"] = "Dealer Bust!"
    elif calc_total(session["player"]) > calc_total(session["dealer"]):  # Player has higher score
         session["game_status"] = "Player Wins!"
         pass
    elif calc_total(session["dealer"]) > calc_total(session["player"]):  # Dealer has higher score
         session["game_status"] = "Dealer Wins!"
         pass
    else:
         session["game_status"] = "Its a Tie!"
         pass


def dealer_hit():
    while calc_total(session["dealer"]) < 17:
        session["dealer"].append(draw())
    
    check_end_game_logic()

def player_hit():
    session["player"].append(draw())
    #We can still stand
    if calc_total(session["player"]) < 21:
        session["game_status"] = "Hit or Stand?"
    else:
        check_end_game_logic()




@app.get("/")
@app.get("/start")
def display_opening_state():
    session["deck"] = make_deck()
    session["player"] = []
    session["dealer"] = []
    session["player"].append(draw())
    session["dealer"].append(draw())
    session["player"].append(draw())
    session["dealer"].append(draw())
    session["dealer_hidden_card"] = "back.png"
    session["game_status"] = ""


    check_start_game_logic(calc_total(session["player"]),calc_total(session["dealer"]),session["dealer_hidden_card"])

    return render_template(
        "start.html",
        player_cards=session["player"],
        player_total=calc_total(session["player"]),
        dealer_cards=session["dealer"],
        dealer_hidden_card=session["dealer_hidden_card"],
        dealer_total=calc_total(session["dealer"]),
        title="",
        header="",
        footer="",
        number_of_cards=len(session["deck"]),
        game_status=session["game_status"]
    )


@app.post("/stand")
def over_to_the_dealer():
    dealer_hit()
    
    return render_template(
        "start.html",
        player_cards=session["player"],
        player_total=calc_total(session["player"]),
        dealer_cards=session["dealer"],
        dealer_hidden_card=session["dealer_hidden_card"],
        dealer_total=calc_total(session["dealer"]),
        title="",
        header="",
        footer="",
        number_of_cards=len(session["deck"]),
        game_status=session["game_status"]
    )


@app.post("/hit")
def select_another_card():
    player_hit()
    return render_template(
        "start.html",
        player_cards=session["player"],
        player_total=calc_total(session["player"]),
        dealer_cards=session["dealer"],
        dealer_hidden_card=session["dealer_hidden_card"],
        dealer_total=calc_total(session["dealer"]),
        title="",
        header="",
        footer="",
        number_of_cards=len(session["deck"]),
        game_status=session["game_status"]
    )


if __name__ == "__main__":
    app.run(debug=True)
