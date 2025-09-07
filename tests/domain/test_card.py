from src.domain.Card import Card


def test_card_creation():
    card = Card("Hearts", "Ace", 11)
    assert card.suit == "Hearts"
    assert card.rank == "Ace"
    assert card.value == 11
