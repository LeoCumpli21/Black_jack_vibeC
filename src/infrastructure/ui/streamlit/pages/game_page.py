import streamlit as st
from src.infrastructure.ui.streamlit.ui_components import display_hand

st.set_page_config(page_title="Blackjack Table", layout="wide")

# Inject CSS for card styling
st.markdown("""
<style>
    /* Target the div that Streamlit creates for st.image */
    div[data-testid="stImage"] {
        background-color: white;
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# Guardrail: Ensure game is in session state.
if "game" not in st.session_state:
    st.warning(
        "Please configure and start a new game from the 'Game Configuration' page first."
    )
    st.page_link("pages/config_page.py", label="Go to Configuration", icon="⚙️")
    st.stop()

# shorter aliases for session state objects
game = st.session_state.game
controller = st.session_state.controller
presenter = st.session_state.presenter
player = game.players[0]  # Assuming single player

# Get the latest view model
view_model = presenter.present(game)

# --- Main Game State Router ---

if view_model.game_state == "betting":
    st.title("Place Your Bet")
    st.info(
        f"Dealer hits on soft 17: **{game.rules.dealer_hits_on_soft_17}** | Decks: **{game.rules.num_decks}**"
    )

    balance_col, bet_col = st.columns(2)
    with balance_col:
        st.metric("Your Balance", f"${view_model.player_balance}")

    with bet_col:
        with st.form(key="bet_form"):
            bet_amount = st.number_input(
                f"Enter your bet ({game.rules.min_bet} - {game.rules.max_bet})",
                min_value=game.rules.min_bet,
                max_value=game.rules.max_bet,
                step=1,
            )
            submitted = st.form_submit_button("Place Bet")
            if submitted:
                try:
                    controller.place_bets({player: bet_amount})
                    controller.start_new_round()
                    st.rerun()
                except ValueError as e:
                    st.error(e)

elif view_model.game_state == "playerTurn":
    # If all hands are played, it's the dealer's turn. This is the main state transition.
    if player.all_hands_played():
        # 1. Set state to dealerTurn and let dealer play.
        game.game_state = 'dealerTurn'
        controller.dealer_turn()

        # 2. Immediately determine the outcome of the hands.
        controller.end_round() # This now only determines outcome, doesn't reset.
        
        # 3. Rerun to display the round over screen with correct results.
        st.rerun()

    # --- Default player turn display ---
    dealer_col, player_col = st.columns(2)
    with dealer_col:
        st.header("Dealer's Hand")
        display_hand(
            view_model.dealer_cards, is_dealer=True, game_state=view_model.game_state
        )
    
    with player_col:
        st.header(f"Your Hand(s) - Balance: ${player.balance}")
        for i, hand_vm in enumerate(view_model.players):
            is_active_hand = i == player.current_hand_index
            hand_label = f"Hand {i + 1} (Value: {hand_vm.value}) - Bet: ${hand_vm.bet}"

            if is_active_hand and hand_vm.status == "playing":
                st.subheader(f"▶️ {hand_label}")
            else:
                st.subheader(hand_label)

            display_hand(hand_vm.cards)

            # Display status and action buttons only for the active hand
            if is_active_hand and hand_vm.status == "playing":
                # Determine available actions
                can_double = len(hand_vm.cards) == 2 and player.balance >= hand_vm.bet
                can_split = (
                    len(hand_vm.cards) == 2
                    and hand_vm.cards[0]["rank"] == hand_vm.cards[1]["rank"]
                    and player.balance >= hand_vm.bet
                )

                action_cols = st.columns(4)
                with action_cols[0]:
                    if st.button("Hit", key=f"hit_{i}", use_container_width=True):
                        controller.perform_player_action(player, "hit")
                        st.rerun()
                with action_cols[1]:
                    if st.button("Stand", key=f"stand_{i}", use_container_width=True):
                        controller.perform_player_action(player, "stand")
                        st.rerun()
                with action_cols[2]:
                    if st.button("Double Down", key=f"double_{i}", use_container_width=True, disabled=not can_double):
                        controller.perform_player_action(player, "doubleDown")
                        st.rerun()
                with action_cols[3]:
                    if st.button("Split", key=f"split_{i}", use_container_width=True, disabled=not can_split):
                        controller.perform_player_action(player, "split")
                        st.rerun()
            elif hand_vm.status != "playing":
                st.info(f"Hand status: **{hand_vm.status.upper()}**")
            st.markdown("---")

elif view_model.game_state == "roundOver":
    st.header("🏁 Round Over 🏁")

    # Determine overall outcome message
    outcome = player.get_overall_status()
    if outcome == "win":
        st.success(f"You win! Your new balance is ${player.balance}")
    elif outcome == "push":
        st.warning(f"It's a push. Your balance is ${player.balance}")
    else:  # lose or busted
        st.error(f"You lose. Your new balance is ${player.balance}")

    # Display final hands
    dealer_col, player_col = st.columns(2)
    with dealer_col:
        st.subheader(f"Dealer's Hand (Value: {view_model.dealer_value})")
        display_hand(view_model.dealer_cards)
    with player_col:
        st.subheader("Your Hand(s)")
        for hand_vm in view_model.players:
            st.text(
                f"Hand {hand_vm.hand_index + 1} (Value: {hand_vm.value}) - Status: {hand_vm.status.upper()}"
            )
            display_hand(hand_vm.cards)
            st.markdown("---")

    if st.button("Next Round"):
        controller.reset_round_for_new_game()
        st.rerun()


elif view_model.game_state == "roundOver":
    st.header("🏁 Round Over 🏁")

    # Determine overall outcome message
    outcome = player.get_overall_status()
    if outcome == "win":
        st.success(f"You win! Your new balance is ${player.balance}")
    elif outcome == "push":
        st.warning(f"It's a push. Your balance is ${player.balance}")
    else:  # lose or busted
        st.error(f"You lose. Your new balance is ${player.balance}")

    # Display final hands
    dealer_col, player_col = st.columns(2)
    with dealer_col:
        st.subheader(f"Dealer's Hand (Value: {view_model.dealer_value})")
        display_hand(view_model.dealer_cards)
    with player_col:
        st.subheader("Your Hand(s)")
        for hand_vm in view_model.players:
            st.text(
                f"Hand {hand_vm.hand_index + 1} (Value: {hand_vm.value}) - Status: {hand_vm.status.upper()}"
            )
            display_hand(hand_vm.cards)
            st.markdown("---")

    if st.button("Next Round"):
        controller.end_round()
        st.rerun()
