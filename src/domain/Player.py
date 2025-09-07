"""Represents a player in the Blackjack game."""

from src.domain.Hand import Hand
from typing import List


class Player:
    """Manages a player's balance, bets, and one or more hands of cards.

    Attributes:
        balance (int): The player's current money.
        hands (List[Hand]): A list of Hand objects the player currently holds.
        bets (List[int]): A list of bets corresponding to each hand.
        current_hand_index (int): The index of the hand currently being played (relevant for splits).
    """

    def __init__(self, balance: int):
        """Initializes a new Player with a starting balance.

        Args:
            balance (int): The initial balance of the player.
        """
        self.balance = balance
        self.hands = [Hand()]  # Player can have multiple hands after splitting
        self.bets = [0]  # Corresponding bets for each hand
        self.current_hand_index = 0  # Index of the hand currently being played

    def place_bet(self, amount: int, hand_index: int = 0):
        """Places a bet for a specific hand and deducts the amount from the player's balance.

        Args:
            amount (int): The amount to bet.
            hand_index (int): The index of the hand the bet is placed on (default is 0 for the first hand).

        Raises:
            ValueError: If the bet amount is not positive or if the player has insufficient balance.
        """
        if amount <= 0:
            raise ValueError("Bet amount must be positive.")
        if amount > self.balance:
            raise ValueError("Insufficient balance to place this bet.")

        # Ensure the bets list is large enough for the given hand_index
        while len(self.bets) <= hand_index:
            self.bets.append(0)

        self.bets[hand_index] = amount
        self.balance -= amount
        self.hands[hand_index].status = 'playing'  # Set hand status to playing

    def get_current_hand(self) -> Hand:
        """Returns the hand the player is currently playing.

        Returns:
            Hand: The current active Hand object.
        """
        return self.hands[self.current_hand_index]

    def get_current_bet(self) -> int:
        """Returns the bet corresponding to the current active hand.

        Returns:
            int: The bet amount for the current hand.
        """
        return self.bets[self.current_hand_index]

    def clear_hands(self):
        """Resets the player's hands and bets for a new round.

        All existing hands are replaced with a single new hand, and bets are reset.
        """
        self.hands = [Hand()]
        self.hands[0].status = 'betting'  # Reset status of the initial hand
        self.bets = [0]
        self.current_hand_index = 0

    def add_hand(self, hand: Hand, bet: int):
        """Adds a new hand to the player, typically used during a split action.

        Args:
            hand (Hand): The new Hand object to add.
            bet (int): The bet amount for the new hand.
        """
        self.hands.append(hand)
        self.bets.append(bet)

    def set_current_hand_index(self, index: int):
        """Sets the index of the hand currently being played.

        Args:
            index (int): The 0-based index of the hand to set as current.

        Raises:
            IndexError: If the provided index is out of bounds.
        """
        if 0 <= index < len(self.hands):
            self.current_hand_index = index
        else:
            raise IndexError("Hand index out of bounds.")

    def all_hands_played(self) -> bool:
        """Checks if all of the player's hands are in a final state (stand or busted).

        Returns:
            bool: True if all hands are played, False otherwise.
        """
        for hand in self.hands:
            if hand.status == 'playing':
                return False
        return True

    def get_overall_status(self) -> str:
        """Determines the player's overall status based on the status of all their hands.

        Returns:
            str: The overall status (e.g., 'playing', 'busted', 'win', 'push', 'stand').
        """
        if any(hand.status == 'playing' for hand in self.hands):
            return 'playing'
        elif all(hand.status == 'busted' for hand in self.hands):
            return 'busted'
        elif any(hand.status == 'win' for hand in self.hands):
            return 'win'
        elif any(hand.status == 'push' for hand in self.hands):
            return 'push'
        else:
            return 'stand'  # Default if all hands are stood or a mix of outcomes
