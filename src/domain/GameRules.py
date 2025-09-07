"""Defines the configurable rules for a Blackjack game."""

import dataclasses


@dataclasses.dataclass
class GameRules:
    """A dataclass holding the specific rules for a game instance.

    Attributes:
        blackjack_payout (float): The payout multiplier for a player's blackjack (e.g., 1.5 for 3:2).
        dealer_hits_on_soft_17 (bool): True if the dealer hits on a soft 17, False otherwise.
        min_bet (int): The minimum allowed bet amount for a round.
        max_bet (int): The maximum allowed bet amount for a round.
        num_decks (int): The number of 52-card decks used in the game.
        reshuffle_penetration (float): The percentage of the deck that is played before a reshuffle is triggered.
    """

    blackjack_payout: float = 1.5
    dealer_hits_on_soft_17: bool = True
    min_bet: int = 10
    max_bet: int = 100
    num_decks: int = 6
    reshuffle_penetration: float = 0.75  # Reshuffle after 75% of the deck is used
