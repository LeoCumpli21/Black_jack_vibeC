"""Handles the initialization of a new round in a Blackjack game."""

from src.domain.Game import Game


class StartRound:
    """A use case that initializes a new round of Blackjack.

    This includes checking if a reshuffle is needed and dealing initial cards.
    """

    def execute(self, game: Game):
        """Executes the start of a new round.

        Checks if the deck penetration has reached the threshold for a reshuffle.
        Deals two cards to each player and the dealer.

        Args:
            game (Game): The current game instance.

        Returns:
            Game: The updated game instance after dealing.
        """
        # Check if the deck needs to be reshuffled
        num_remaining_cards = len(game.deck.cards)
        penetration = 1.0 - (num_remaining_cards / game.deck.total_cards)
        if penetration >= game.rules.reshuffle_penetration:
            game.deck.build_and_shuffle()
            # Optionally, you could add a message to the game state to inform the UI
            # game.add_message("Deck has been reshuffled.")

        # Deal initial cards
        for _ in range(2):
            for player in game.players:
                player.hands[0].add_card(game.deck.deal())
            game.dealer.hands[0].add_card(game.deck.deal())
        
        game.game_state = 'playerTurn'
        return game
