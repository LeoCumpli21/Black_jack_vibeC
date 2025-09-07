"""Represents the central state of the Blackjack game."""

from typing import List
from .Player import Player
from .Dealer import Dealer
from .Deck import Deck
from .GameRules import GameRules


class Game:
    """Holds the overall state of a Blackjack game.

    This includes all players, the dealer, the deck, the game rules, and the current game state.
    """

    def __init__(self, players: List[Player], rules: GameRules):
        """Initializes a new game session.

        Args:
            players (List[Player]): A list of Player objects participating in the game.
            rules (GameRules): The set of rules governing this game instance.
        """
        self.players = players
        self.dealer = Dealer()
        self.deck = Deck(rules.num_decks)
        self.rules = rules
        self.game_state = 'betting'  # Current state: 'betting', 'playerTurn', 'dealerTurn', 'roundOver'
