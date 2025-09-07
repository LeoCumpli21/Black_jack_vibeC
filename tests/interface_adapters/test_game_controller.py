import pytest
from unittest.mock import MagicMock
from src.domain.Game import Game
from src.domain.Player import Player
from src.domain.GameRules import GameRules
from src.interface_adapters.game_controller import GameController

@pytest.fixture
def mock_game():
    return MagicMock(spec=Game)

@pytest.fixture
def game_controller(mock_game):
    controller = GameController(mock_game)
    controller.start_round = MagicMock()
    controller.place_bet = MagicMock()
    controller.player_action = MagicMock()
    controller.dealer_plays = MagicMock()
    controller.determine_outcome = MagicMock()
    return controller

def test_start_new_round(game_controller, mock_game):
    game_controller.start_new_round()
    game_controller.start_round.execute.assert_called_once_with(mock_game)

def test_place_bets(game_controller, mock_game):
    player = Player(100)
    bets = {player: 50}
    mock_game.game_state = 'betting' # Set game_state for the mock
    mock_game.rules = MagicMock(spec=GameRules, min_bet=10, max_bet=100) # Set rules for the mock
    game_controller.place_bets(bets)
    game_controller.place_bet.execute.assert_called_once_with(mock_game, bets)

def test_place_bets_wrong_state(game_controller, mock_game):
    player = Player(100)
    bets = {player: 50}
    mock_game.game_state = 'playerTurn'
    with pytest.raises(ValueError, match="Can only place bets in 'betting' state."):
        game_controller.place_bets(bets)

def test_place_bets_below_limit(game_controller, mock_game):
    player = Player(100)
    bets = {player: 5}
    mock_game.game_state = 'betting' # Set game_state for the mock
    mock_game.rules = MagicMock(spec=GameRules, min_bet=10, max_bet=100)
    with pytest.raises(ValueError, match="Bet is not within the table limits."):
        game_controller.place_bets(bets)

def test_place_bets_above_limit(game_controller, mock_game):
    player = Player(200)
    bets = {player: 150}
    mock_game.game_state = 'betting' # Set game_state for the mock
    mock_game.rules = MagicMock(spec=GameRules, min_bet=10, max_bet=100)
    with pytest.raises(ValueError, match="Bet is not within the table limits."):
        game_controller.place_bets(bets)

def test_perform_player_action(game_controller, mock_game):
    player = Player(100)
    action = 'hit'
    game_controller.perform_player_action(player, action)
    game_controller.player_action.execute.assert_called_once_with(mock_game, player, action)

def test_dealer_turn(game_controller, mock_game):
    game_controller.dealer_turn()
    game_controller.dealer_plays.execute.assert_called_once_with(mock_game)

def test_end_round(game_controller, mock_game):
    game_controller.end_round()
    game_controller.determine_outcome.execute.assert_called_once_with(mock_game)
