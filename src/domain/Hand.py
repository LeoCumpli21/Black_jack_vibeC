"""Represents a player's or dealer's hand of cards."""

from typing import List
from src.domain.Card import Card


class Hand:
    """Manages the cards in a single hand and calculates its value.

    Attributes:
        cards (List[Card]): A list of Card objects currently in the hand.
        status (str): The current status of the hand (e.g., 'playing', 'busted', 'stand').
    """

    def __init__(self):
        """Initializes an empty hand with a 'playing' status."""
        self.cards = []
        self.status = 'playing'  # playing, busted, stand

    def add_card(self, card: Card):
        """Adds a card to the hand.

        Args:
            card (Card): The Card object to add to the hand.
        """
        self.cards.append(card)

    def get_value(self) -> int:
        """Calculates the total value of the hand, intelligently handling Aces.

        Aces are valued at 11 unless that would cause the hand to bust (exceed 21),
        in which case they are valued at 1.

        Returns:
            int: The calculated value of the hand.
        """
        value = 0
        num_aces = 0
        for card in self.cards:
            if card.rank == 'Ace':
                num_aces += 1
                value += 11
            else:
                value += card.value

        while value > 21 and num_aces > 0:
            value -= 10
            num_aces -= 1
        return value
