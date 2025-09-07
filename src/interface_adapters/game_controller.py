"""Handles user input and orchestrates application use cases."""

from src.application.start_round import StartRound
from src.application.place_bet import PlaceBet
from src.application.player_action import PlayerAction
from src.application.dealer_plays import DealerPlays
from src.application.determine_outcome import DetermineOutcome
from src.application.reset_round import ResetRound
from src.domain.Game import Game
from src.domain.Player import Player
from typing import Dict


class GameController:
    """A controller that acts as a facade over the application's use cases.

    This class simplifies the interaction between the UI and the core application logic.
    The UI layer calls methods on this controller to perform game actions.
    """

    def __init__(self, game: Game):
        """Initializes the GameController with all necessary use cases.

        Args:
            game (Game): The main game instance.
        """
        self.game = game
        self.start_round = StartRound()
        self.place_bet = PlaceBet()
        self.player_action = PlayerAction()
        self.dealer_plays = DealerPlays()
        self.determine_outcome = DetermineOutcome()
        self.reset_round = ResetRound()

    def start_new_round(self):
        """Starts a new round of the game."""
        self.start_round.execute(self.game)

    def place_bets(self, bets: Dict[Player, int]):
        """Places bets for players and validates them against game rules.

        Args:
            bets (Dict[Player, int]): A dictionary mapping players to their bet amounts.

        Raises:
            ValueError: If the bet is invalid or the game is not in the 'betting' state.
        """
        if self.game.game_state != 'betting':
            raise ValueError("Can only place bets in 'betting' state.")

        for player, amount in bets.items():
            if not (self.game.rules.min_bet <= amount <= self.game.rules.max_bet):
                raise ValueError("Bet is not within the table limits.")
            if player.balance < amount:
                raise ValueError("Insufficient balance to place this bet.")
            self.place_bet.execute(self.game, {player: amount})

    def perform_player_action(self, player: Player, action: str):
        """Performs a specific action for a player (e.g., hit, stand).

        Args:
            player (Player): The player performing the action.
            action (str): The action to be performed.
        """
        self.player_action.execute(self.game, player, action)

    def dealer_turn(self):
        """Executes the dealer's turn."""
        self.dealer_plays.execute(self.game)

    def end_round(self):
        """Ends the round by determining the outcome for all players."""
        self.determine_outcome.execute(self.game)

    def reset_round_for_new_game(self):
        """Resets the game state for a new round."""
        self.reset_round.execute(self.game)
