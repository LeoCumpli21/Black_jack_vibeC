import pytest
from src.domain.Game import Game
from src.domain.Player import Player
from src.domain.GameRules import GameRules
from src.application.determine_outcome import DetermineOutcome
from src.application.reset_round import ResetRound
from src.domain.Card import Card

@pytest.fixture
def game():
    player = Player(balance=100)
    player.place_bet(10)
    rules = GameRules(blackjack_payout=1.5)
    game = Game(players=[player], rules=rules)
    game.game_state = 'roundOver'
    return game

def test_player_wins(game):
    game.players[0].hands[0].add_card(Card("Hearts", "10", 10))
    game.players[0].hands[0].add_card(Card("Diamonds", "Jack", 10))
    game.dealer.hands[0].add_card(Card("Clubs", "9", 9))
    game.dealer.hands[0].add_card(Card("Spades", "8", 8))

    DetermineOutcome().execute(game)
    assert game.players[0].balance == 110

def test_player_loses(game):
    game.players[0].hands[0].add_card(Card("Hearts", "10", 10))
    game.players[0].hands[0].add_card(Card("Diamonds", "7", 7))
    game.dealer.hands[0].add_card(Card("Clubs", "9", 9))
    game.dealer.hands[0].add_card(Card("Spades", "Jack", 10))

    DetermineOutcome().execute(game)
    assert game.players[0].balance == 90

def test_player_push(game):
    game.players[0].hands[0].add_card(Card("Hearts", "10", 10))
    game.players[0].hands[0].add_card(Card("Diamonds", "7", 7))
    game.dealer.hands[0].add_card(Card("Clubs", "9", 9))
    game.dealer.hands[0].add_card(Card("Spades", "8", 8))

    DetermineOutcome().execute(game)
    assert game.players[0].balance == 100

def test_player_blackjack(game):
    game.players[0].hands[0].add_card(Card("Hearts", "Ace", 11))
    game.players[0].hands[0].add_card(Card("Diamonds", "Jack", 10))
    game.dealer.hands[0].add_card(Card("Clubs", "9", 9))
    game.dealer.hands[0].add_card(Card("Spades", "8", 8))

    DetermineOutcome().execute(game)
    assert game.players[0].balance == 115

def test_player_blackjack_push(game):
    game.players[0].hands[0].add_card(Card("Hearts", "Ace", 11))
    game.players[0].hands[0].add_card(Card("Diamonds", "Jack", 10))
    game.dealer.hands[0].add_card(Card("Clubs", "Ace", 11))
    game.dealer.hands[0].add_card(Card("Spades", "Queen", 10))

    DetermineOutcome().execute(game)
    assert game.players[0].balance == 100

def test_player_busts(game):
    game.players[0].hands[0].status = 'busted'
    game.players[0].hands[0].add_card(Card("Hearts", "10", 10))
    game.players[0].hands[0].add_card(Card("Diamonds", "Jack", 10))
    game.players[0].hands[0].add_card(Card("Clubs", "5", 5))

    DetermineOutcome().execute(game)
    assert game.players[0].balance == 90

def test_dealer_busts(game):
    game.dealer.hands[0].status = 'busted'
    game.dealer.hands[0].add_card(Card("Hearts", "10", 10))
    game.dealer.hands[0].add_card(Card("Diamonds", "Jack", 10))
    game.dealer.hands[0].add_card(Card("Clubs", "5", 5))
    game.players[0].hands[0].add_card(Card("Spades", "9", 9))
    game.players[0].hands[0].add_card(Card("Spades", "8", 8))

    DetermineOutcome().execute(game)
    assert game.players[0].balance == 110

def test_wrong_state(game):
    game.game_state = 'playerTurn'
    with pytest.raises(ValueError, match="Can only determine outcome in 'roundOver' state."):
        DetermineOutcome().execute(game)

def test_resets_for_next_round(game):
    # This test now verifies the reset functionality which is in its own use case
    ResetRound().execute(game)
    
    assert game.players[0].hands[0].cards == []
    assert game.players[0].bets == [0]
    assert game.players[0].hands[0].status == 'betting'
    assert game.dealer.hands[0].cards == []
    assert game.dealer.hands[0].status == 'betting'
    assert game.game_state == 'betting'
