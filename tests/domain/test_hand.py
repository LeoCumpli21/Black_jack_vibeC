from src.domain.Hand import Hand
from src.domain.Card import Card


def test_add_card():
    hand = Hand()
    hand.add_card(Card("Hearts", "Ace", 11))
    assert len(hand.cards) == 1


def test_get_value():
    hand = Hand()
    hand.add_card(Card("Hearts", "Ace", 11))
    hand.add_card(Card("Diamonds", "10", 10))
    assert hand.get_value() == 21


def test_get_value_with_multiple_aces():
    hand = Hand()
    hand.add_card(Card("Hearts", "Ace", 11))
    hand.add_card(Card("Diamonds", "Ace", 11))
    assert hand.get_value() == 12


def test_get_value_bust():
    hand = Hand()
    hand.add_card(Card("Hearts", "10", 10))
    hand.add_card(Card("Diamonds", "10", 10))
    hand.add_card(Card("Clubs", "2", 2))
    assert hand.get_value() == 22