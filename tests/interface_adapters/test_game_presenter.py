import pytest
from src.domain.Game import Game
from src.domain.Player import Player
from src.domain.Dealer import Dealer
from src.domain.Card import Card
from src.domain.GameRules import GameRules
from src.interface_adapters.game_presenter import GamePresenter
from src.interface_adapters.game_view_model import GameViewModel

def test_present_game_state():
    player = Player(balance=100)
    player.hands[0].add_card(Card(suit='Hearts', rank='10', value=10))
    player.hands[0].add_card(Card(suit='Spades', rank='5', value=5))
    player.bets[0] = 20
    player.hands[0].status = 'playing'

    dealer = Dealer()
    dealer.hands[0].add_card(Card(suit='Clubs', rank='7', value=7))
    dealer.hands[0].add_card(Card(suit='Diamonds', rank='King', value=10))

    game = Game(players=[player], rules=GameRules())
    game.dealer = dealer
    game.game_state = 'roundOver'

    presenter = GamePresenter()
    view_model = presenter.present(game)

    assert isinstance(view_model, GameViewModel)
    assert len(view_model.players) == 1
    assert view_model.players[0].value == 15
    assert view_model.player_balance == 100
    assert view_model.players[0].bet == 20
    assert view_model.players[0].status == 'playing'
    assert len(view_model.players[0].cards) == 2
    assert view_model.players[0].cards[0]['rank'] == '10'

    assert len(view_model.dealer_cards) == 2
    assert view_model.dealer_value == 17
    assert view_model.game_state == 'roundOver'

def test_present_hides_dealer_card():
    player = Player(balance=100)
    dealer = Dealer()
    dealer.hands[0].add_card(Card(suit='Clubs', rank='7', value=7))
    dealer.hands[0].add_card(Card(suit='Diamonds', rank='King', value=10))

    game = Game(players=[player], rules=GameRules())
    game.dealer = dealer
    game.game_state = 'playerTurn'
    
    presenter = GamePresenter()
    view_model = presenter.present(game)

    assert len(view_model.dealer_cards) == 2
    assert view_model.dealer_cards[1]['rank'] == '?'
    assert view_model.dealer_value == 7
