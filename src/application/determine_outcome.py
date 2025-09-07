"""Determines the outcome of a Blackjack round for all players."""

from src.domain.Game import Game


class DetermineOutcome:
    """A use case that compares player hands against the dealer's hand and settles bets.

    This use case updates player balances and sets the final status of each hand
    (win, lose, or push).
    """

    def execute(self, game: Game):
        """Compares player hands to the dealer's hand and settles bets.

        Args:
            game (Game): The current game instance.

        Raises:
            ValueError: If the game state is not 'roundOver'.
        """
        if game.game_state != 'roundOver':
            raise ValueError("Can only determine outcome in 'roundOver' state.")

        dealer_hand = game.dealer.hands[0]
        dealer_value = dealer_hand.get_value()
        dealer_busted = dealer_hand.status == 'busted'
        dealer_has_blackjack = dealer_value == 21 and len(dealer_hand.cards) == 2

        for player in game.players:
            # Iterate through all hands of the player
            for i, player_hand in enumerate(player.hands):
                player_bet = player.bets[i]

                if player_hand.status == 'busted':
                    # Balance already deducted when bet was placed. No change needed here.
                    continue

                player_value = player_hand.get_value()
                player_has_blackjack = player_value == 21 and len(player_hand.cards) == 2

                if dealer_busted:
                    if player_has_blackjack:
                        player.balance += player_bet + int(player_bet * game.rules.blackjack_payout)
                        player_hand.status = 'win'
                    else:
                        player.balance += player_bet * 2  # Player gets back bet + wins bet
                        player_hand.status = 'win'
                elif player_has_blackjack and not dealer_has_blackjack:
                    player.balance += player_bet + int(player_bet * game.rules.blackjack_payout)
                    player_hand.status = 'win'
                elif player_value > dealer_value:
                    player.balance += player_bet * 2  # Player gets back bet + wins bet
                    player_hand.status = 'win'
                elif player_value < dealer_value:
                    # Balance already deducted. No change needed.
                    player_hand.status = 'lose'
                else:  # Push
                    player.balance += player_bet  # Player gets back original bet
                    player_hand.status = 'push'
