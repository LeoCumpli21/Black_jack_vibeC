"""Handles the resetting of the game state for a new round."""

from src.domain.Game import Game


class ResetRound:
    """A use case responsible for clearing all player and dealer hands
    and resetting the game state to 'betting' for the next round.
    """

    def execute(self, game: Game):
        """Clears all player and dealer hands and resets the game state for the next round.

        Args:
            game (Game): The current game instance.
        """
        for player in game.players:
            player.clear_hands()
        
        game.dealer.clear_hands()

        game.game_state = 'betting'
