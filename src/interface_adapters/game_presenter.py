"""Transforms domain models into view models for the UI."""

from src.domain.Game import Game
from src.interface_adapters.game_view_model import GameViewModel, PlayerViewModel


class GamePresenter:
    """A presenter that converts the main Game domain object into a simple
    GameViewModel, suitable for consumption by the UI layer.
    """

    def present(self, game: Game) -> GameViewModel:
        """Converts the Game object into a GameViewModel.

        This method simplifies the complex domain model into a flat structure
        that the UI can easily render. It also contains presentation logic,
        such as hiding the dealer's second card during the player's turn.

        Args:
            game (Game): The current game instance.

        Returns:
            GameViewModel: The view model representing the current game state.
        """
        player_view_models = []
        # Assuming only one player for now
        player = game.players[0]

        for i, player_hand in enumerate(player.hands):
            player_view_models.append(PlayerViewModel(
                hand_index=i,
                cards=[{'rank': card.rank, 'suit': card.suit} for card in player_hand.cards],
                value=player_hand.get_value(),
                bet=player.bets[i],
                status=player_hand.status
            ))

        dealer_cards = []
        dealer_value = 0
        # Assuming dealer always plays with one hand
        dealer_current_hand = game.dealer.hands[0]

        # Hide dealer's second card if it is the player's turn
        if game.game_state == 'playerTurn' and len(dealer_current_hand.cards) == 2:
            dealer_cards.append({'rank': dealer_current_hand.cards[0].rank, 'suit': dealer_current_hand.cards[0].suit})
            dealer_cards.append({'rank': '?', 'suit': '?'})
            dealer_value = dealer_current_hand.cards[0].value
        else:
            dealer_cards = [{'rank': card.rank, 'suit': card.suit} for card in dealer_current_hand.cards]
            dealer_value = dealer_current_hand.get_value()

        return GameViewModel(
            player_balance=player.balance,
            players=player_view_models,
            dealer_cards=dealer_cards,
            dealer_value=dealer_value,
            game_state=game.game_state
        )
