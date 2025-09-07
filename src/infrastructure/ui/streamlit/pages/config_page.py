import streamlit as st
from src.domain.GameRules import GameRules
from src.domain.Player import Player
from src.domain.Game import Game
from src.interface_adapters.game_controller import GameController
from src.interface_adapters.game_presenter import GamePresenter

st.set_page_config(page_title="Game Configuration", layout="centered")

st.title("Setup Your Blackjack Game")

st.write("Use the options below to configure the rules for your game.")

# Create Rule Widgets
with st.form(key="game_rules_form"):
    st.header("Table Rules")

    c1, c2 = st.columns(2)
    with c1:
        min_bet = st.number_input("Minimum Bet", min_value=1, value=10, step=1)
        num_decks = st.number_input(
            "Number of Decks", min_value=1, max_value=8, value=6, step=1
        )
    with c2:
        max_bet = st.number_input("Maximum Bet", min_value=1, value=100, step=1)
        dealer_hits_on_soft_17 = st.checkbox("Dealer Hits on Soft 17", value=True)

    blackjack_payout = st.slider(
        "Blackjack Payout", min_value=1.0, max_value=2.0, value=1.5, step=0.1
    )

    st.header("Player Setup")
    player_balance = st.number_input(
        "Starting Player Balance", min_value=1, value=100, step=10
    )

    # Form submission button
    submitted = st.form_submit_button("Start Game")

if submitted:
    # Create an instance of GameRules using the values from the widgets
    rules = GameRules(
        min_bet=min_bet,
        max_bet=max_bet,
        num_decks=num_decks,
        blackjack_payout=blackjack_payout,
        dealer_hits_on_soft_17=dealer_hits_on_soft_17,
    )

    # Initialize the game objects
    player = Player(balance=player_balance)
    game = Game(players=[player], rules=rules)
    controller = GameController(game)
    presenter = GamePresenter()

    # Store these essential objects in the session state
    st.session_state.game = game
    st.session_state.controller = controller
    st.session_state.presenter = presenter

    # Navigate to the game page
    st.switch_page("src/infrastructure/ui/streamlit/pages/game_page.py")
