from src.domain.Game import Game
from src.domain.Player import Player
from src.domain.GameRules import GameRules
from src.application.start_round import StartRound

def test_start_round_execute():
    players = [Player(balance=100)]
    rules = GameRules()
    game = Game(players=players, rules=rules)
    
    start_round = StartRound()
    game = start_round.execute(game)

    assert len(game.players[0].hands[0].cards) == 2
    assert len(game.dealer.hands[0].cards) == 2
    assert len(game.deck.cards) == (rules.num_decks * 52) - 4
    assert game.game_state == 'playerTurn'
