from src.domain.Deck import Deck


def test_deck_creation():
    deck = Deck()
    assert len(deck.cards) == 52


def test_multiple_decks():
    deck = Deck(num_decks=2)
    assert len(deck.cards) == 104


def test_deal():
    deck = Deck()
    card = deck.deal()
    assert len(deck.cards) == 51
    assert card is not None


def test_shuffle():
    deck1 = Deck()
    deck2 = Deck()
    deck2.shuffle()
    # It's possible, but highly unlikely, that the shuffled deck is the same as the original
    assert [str(c) for c in deck1.cards] != [str(c) for c in deck2.cards]
