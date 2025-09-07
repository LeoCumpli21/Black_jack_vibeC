import pytest
from src.domain.Game import Game
from src.domain.Player import Player
from src.domain.GameRules import GameRules
from src.application.place_bet import PlaceBet

def test_place_bet_success():
    player = Player(balance=100)
    rules = GameRules(min_bet=10, max_bet=100)
    game = Game(players=[player], rules=rules)
    
    place_bet = PlaceBet()
    place_bet.execute(game=game, bets={player: 50})

    assert player.bets[0] == 50
    assert player.hands[0].status == 'playing'

def test_place_bet_insufficient_balance():
    player = Player(balance=10)
    rules = GameRules(min_bet=10, max_bet=100)
    game = Game(players=[player], rules=rules)
    
    place_bet = PlaceBet()
    with pytest.raises(ValueError, match="Insufficient balance."):
        place_bet.execute(game=game, bets={player: 20})