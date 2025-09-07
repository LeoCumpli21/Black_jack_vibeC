"""Handles the action of a player placing a bet."""

from src.domain.Game import Game
from src.domain.Player import Player


class PlaceBet:
    """A use case that allows one or more players to place their bets for a round.

    This use case interacts with the Player entity to deduct the bet amount
    from their balance.
    """

    def execute(self, game: Game, bets: dict[Player, int]):
        """Executes the bet placement for given players.

        Args:
            game (Game): The current game instance.
            bets (dict[Player, int]): A dictionary mapping Player objects to their bet amounts.
        """
        for player, amount in bets.items():
            player.place_bet(amount)
