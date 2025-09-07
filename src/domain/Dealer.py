"""Represents the Dealer in a Blackjack game."""

from .Player import Player


class Dealer(Player):
    """Represents the dealer, a specialized type of Player.

    The dealer starts with a balance of zero and follows a fixed set of rules
    for playing their hand.
    """

    def __init__(self):
        """Initializes the Dealer."""
        super().__init__(balance=0)
