"""Handles the dealer's turn in a Blackjack game."""

from src.domain.Game import Game


class DealerPlays:
    """A use case that executes the dealer's turn based on Blackjack rules.

    The dealer will hit until their hand value is 17 or more.
    Configurable to hit or stand on a soft 17.
    """

    def execute(self, game: Game):
        """Executes the dealer's turn.

        Args:
            game (Game): The current game instance.

        Raises:
            ValueError: If the game state is not 'dealerTurn'.
        """
        if game.game_state != 'dealerTurn':
            raise ValueError("Not the dealer's turn.")

        dealer = game.dealer
        rules = game.rules

        # Dealer hits until 17 or more
        while dealer.hands[0].get_value() < 17:
            dealer.hands[0].add_card(game.deck.deal())

        # Handle soft 17 rule
        is_soft_17 = dealer.hands[0].get_value() == 17 and any(card.rank == 'Ace' for card in dealer.hands[0].cards)
        if is_soft_17 and rules.dealer_hits_on_soft_17:
            dealer.hands[0].add_card(game.deck.deal())

        # Set dealer hand status
        if dealer.hands[0].get_value() > 21:
            dealer.hands[0].status = 'busted'
        else:
            dealer.hands[0].status = 'stand'
            
        game.game_state = 'roundOver'
