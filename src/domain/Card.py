"""Represents a single playing card."""

import dataclasses


@dataclasses.dataclass
class Card:
    """A dataclass representing a card with a suit, rank, and game value.

    Attributes:
        suit (str): The suit of the card (e.g., 'Hearts', 'Spades').
        rank (str): The rank of the card (e.g., '7', 'King', 'Ace').
        value (int): The integer value of the card in Blackjack.
    """

    suit: str
    rank: str
    value: int
