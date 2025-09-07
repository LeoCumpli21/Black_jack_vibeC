import pytest
from src.domain.Player import Player
from src.domain.Hand import Hand

def test_player_creation():
    player = Player(balance=100)
    assert player.balance == 100
    assert player.bets == [0]
    assert isinstance(player.hands[0], Hand)
    assert player.hands[0].status == 'playing'

def test_player_place_bet():
    player = Player(balance=100)
    player.place_bet(50)
    assert player.balance == 50
    assert player.bets == [50]
    assert player.hands[0].status == 'playing'

def test_player_place_bet_insufficient_balance():
    player = Player(balance=10)
    with pytest.raises(ValueError, match="Insufficient balance to place this bet."):
        player.place_bet(50)

def test_player_place_bet_zero_amount():
    player = Player(balance=100)
    with pytest.raises(ValueError, match="Bet amount must be positive."):
        player.place_bet(0)

def test_player_clear_hands():
    player = Player(balance=100)
    player.place_bet(20)
    player.hands.append(Hand())
    player.bets.append(20)
    player.clear_hands()
    assert player.hands[0].cards == []
    assert player.bets == [0]
    assert player.hands[0].status == 'betting'
    assert player.current_hand_index == 0
