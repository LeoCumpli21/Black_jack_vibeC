"""Represents the deck of cards for the Blackjack game."""

import random
from typing import List
from .Card import Card


class Deck:
    """Manages a collection of cards, supporting multiple decks, shuffling, and dealing."""

    def __init__(self, num_decks: int = 1):
        """Initializes the Deck for a specified number of 52-card decks.

        Args:
            num_decks (int): The number of standard 52-card decks to use.
        """
        self.cards: List[Card] = []
        self.discard_pile: List[Card] = []
        self.num_decks = num_decks
        self.build_and_shuffle()

    def build_and_shuffle(self):
        """Builds a new, full, and shuffled deck of cards."""
        self.cards = []
        self.discard_pile = []
        for _ in range(self.num_decks):
            for suit in ["Hearts", "Diamonds", "Clubs", "Spades"]:
                for rank, value in {
                    "2": 2,
                    "3": 3,
                    "4": 4,
                    "5": 5,
                    "6": 6,
                    "7": 7,
                    "8": 8,
                    "9": 9,
                    "10": 10,
                    "Jack": 10,
                    "Queen": 10,
                    "King": 10,
                    "Ace": 11,
                }.items():
                    self.cards.append(Card(suit, rank, value))
        self.shuffle()

    def shuffle(self):
        """Randomly shuffles the cards in the deck."""
        random.shuffle(self.cards)

    def deal(self) -> Card:
        """Deals one card from the top of the deck and adds it to the discard pile.

        If the deck is empty, it automatically rebuilds and shuffles it before dealing.

        Returns:
            Card: The card dealt from the top of the deck.
        """
        if not self.cards:
            self.build_and_shuffle()
        
        card = self.cards.pop()
        self.discard_pile.append(card)
        return card

    @property
    def total_cards(self) -> int:
        """Returns the total number of cards that should be in a full shoe."""
        return self.num_decks * 52
