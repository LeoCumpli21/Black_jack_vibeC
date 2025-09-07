"""Handles all player actions during their turn."""

from src.domain.Game import Game
from src.domain.Player import Player
from src.domain.Hand import Hand
from src.domain.Card import Card


class PlayerAction:
    """A use case to handle all player actions (hit, stand, double down, split)."""

    def execute(self, game: Game, player: Player, action: str):
        """Executes a given action for a player.

        Args:
            game (Game): The current game instance.
            player (Player): The player performing the action.
            action (str): The action to perform (e.g., 'hit', 'stand').

        Raises:
            ValueError: If the action is invalid or not allowed at the current time.
        """
        if game.game_state != 'playerTurn':
            raise ValueError("Not the player's turn.")

        current_hand = player.get_current_hand()

        if action == 'hit':
            self._hit(game, player, current_hand)
        elif action == 'stand':
            self._stand(player, current_hand)
        elif action == 'doubleDown':
            self._double_down(game, player, current_hand)
        elif action == 'split':
            self._split(game, player, current_hand)
        else:
            raise ValueError(f"Invalid action: {action}")

        # After any action, check if the current hand is done and advance to the next active hand
        if current_hand.status != 'playing':
            self._advance_to_next_active_hand(player)

    def _hit(self, game: Game, player: Player, hand: Hand):
        """Private method to handle the 'hit' action."""
        hand.add_card(game.deck.deal())
        if hand.get_value() > 21:
            hand.status = 'busted'

    def _stand(self, player: Player, hand: Hand):
        """Private method to handle the 'stand' action."""
        hand.status = 'stand'

    def _double_down(self, game: Game, player: Player, hand: Hand):
        """Private method to handle the 'doubleDown' action."""
        current_bet = player.get_current_bet()

        if player.balance < current_bet:
            raise ValueError("Insufficient balance to double down.")
        if len(hand.cards) != 2:
            raise ValueError("Can only double down on a two-card hand.")

        player.balance -= current_bet
        player.bets[player.current_hand_index] = current_bet * 2
        hand.add_card(game.deck.deal())
        if hand.get_value() > 21:
            hand.status = 'busted'
        else:
            hand.status = 'stand'

    def _split(self, game: Game, player: Player, hand: Hand):
        """Private method to handle the 'split' action."""
        current_bet = player.get_current_bet()

        if len(hand.cards) != 2:
            raise ValueError("Can only split a two-card hand.")
        if hand.cards[0].rank != hand.cards[1].rank:
            raise ValueError("Cards must be of the same rank to split.")
        if player.balance < current_bet:
            raise ValueError("Insufficient balance to split.")

        # Deduct the second bet
        player.balance -= current_bet

        # Create new hand and move one card
        new_hand = Hand()
        new_hand.add_card(hand.cards.pop())
        new_hand.status = 'playing'  # New hand is active

        # Add new hand to player's hands
        player.add_hand(new_hand, current_bet)

        # Deal new cards to both hands
        hand.add_card(game.deck.deal())
        new_hand.add_card(game.deck.deal())

        # The original hand remains 'playing'

    def _advance_to_next_active_hand(self, player: Player):
        """After a hand is finished, advances to the next available hand for the player.

        This is primarily for handling multiple hands after a split.
        If no more hands are available to play, the player's turn is over.
        """
        # Find the next hand that is still 'playing'
        original_index = player.current_hand_index
        found_next = False
        for i in range(original_index + 1, len(player.hands)):
            if player.hands[i].status == 'playing':
                player.set_current_hand_index(i)
                found_next = True
                break

        if not found_next:
            # If no more playing hands, check if any hand is still active (not busted or stood)
            # This handles cases where a split hand might have been added after the current index
            for i in range(len(player.hands)):
                if player.hands[i].status == 'playing':
                    player.set_current_hand_index(i)
                    found_next = True
                    break

        if not found_next:
            # All hands are played (busted or stood), so the player's turn is over
            # The overall player status will be determined by DetermineOutcome
            player.set_current_hand_index(0)  # Reset to first hand for next round or display
