"""Defines the data structures for the game's view model."""

import dataclasses
from typing import List, Dict


@dataclasses.dataclass
class PlayerViewModel:
    """A simple data structure representing a player's hand for the UI.

    Attributes:
        hand_index (int): The index of this hand in the player's list of hands.
        cards (List[Dict[str, str]]): A list of cards in the hand.
        value (int): The current total value of the hand.
        bet (int): The bet amount placed on this hand.
        status (str): The current status of the hand (e.g., 'playing', 'busted').
    """

    hand_index: int
    cards: List[Dict[str, str]]
    value: int
    bet: int
    status: str


@dataclasses.dataclass
class GameViewModel:
    """A simple data structure representing the entire game state for the UI.

    Attributes:
        player_balance (int): The current balance of the player.
        players (List[PlayerViewModel]): A list of view models for each of the player's hands.
        dealer_cards (List[Dict[str, str]]): A list of the dealer's cards.
        dealer_value (int): The current value of the dealer's hand.
        game_state (str): The overall state of the game (e.g., 'playerTurn').
    """

    player_balance: int
    players: List[PlayerViewModel]
    dealer_cards: List[Dict[str, str]]
    dealer_value: int
    game_state: str
