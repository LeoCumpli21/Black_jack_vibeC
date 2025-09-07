import streamlit as st
from typing import List, Dict

def display_card(card: Dict[str, str], use_back=False):
    """
    Renders a single card by displaying its image.
    """
    # Handle the dealer's face-down card or an empty card placeholder
    if use_back or card.get('rank') == '?':
        image_path = "assets/png_cards/back.png"
    else:
        # Convert rank and suit to lowercase for the filename
        rank = card['rank'].lower()
        suit = card['suit'].lower()
        image_path = f"assets/png_cards/{rank}_of_{suit}.png"

    try:
        st.image(image_path, width=120)
    except FileNotFoundError:
        # Fallback to text if an image is not found
        st.error(f"Image not found: {image_path}")
        st.markdown(f"```\n {card['rank']} of {card['suit']} \n```")

def display_hand(hand: List[Dict[str, str]], is_dealer=False, game_state=None):
    """
    Renders a collection of cards in a horizontal layout.
    Hides the dealer's second card if it's the player's turn.
    """
    num_cards = len(hand)
    if num_cards == 0:
        return

    cols = st.columns(num_cards)
    for i, card in enumerate(hand):
        with cols[i]:
            # Hide the dealer's second card during the player's turn
            use_back = is_dealer and i == 1 and game_state == 'playerTurn'
            display_card(card, use_back=use_back)
