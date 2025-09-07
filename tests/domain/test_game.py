from src.domain.Game import Game
from src.domain.Player import Player
from src.domain.GameRules import GameRules


def test_game_creation():
    players = [Player(balance=100)]
    rules = GameRules()
    game = Game(players, rules)
    assert len(game.players) == 1
    assert game.dealer is not None
    assert game.deck is not None
    assert game.rules == rules
    assert game.game_state == "betting"