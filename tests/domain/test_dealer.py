from src.domain.Dealer import Dealer


def test_dealer_creation():
    dealer = Dealer()
    assert dealer.balance == 0