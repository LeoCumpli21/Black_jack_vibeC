import pytest
from src.domain.Game import Game
from src.domain.Player import Player
from src.domain.GameRules import GameRules
from src.application.player_action import PlayerAction
from src.domain.Card import Card
from src.domain.Deck import Deck
from src.domain.Hand import Hand

@pytest.fixture
def setup_game_and_player():
    player = Player(balance=100)
    rules = GameRules()
    game = Game(players=[player], rules=rules)
    game.game_state = 'playerTurn'
    action = PlayerAction()
    return game, player, action

def test_player_action_hit(setup_game_and_player):
    game, player, action = setup_game_and_player
    
    player.get_current_hand().add_card(Card("Hearts", "10", 10))
    player.get_current_hand().add_card(Card("Diamonds", "7", 7))
    
    # Control the deck to ensure a non-busting card is dealt
    game.deck.cards.clear()
    game.deck.cards.append(Card("Clubs", "2", 2))

    action.execute(game=game, player=player, action='hit')

    assert len(player.get_current_hand().cards) == 3
    assert player.get_current_hand().status != 'busted'

def test_player_action_hit_bust(setup_game_and_player):
    game, player, action = setup_game_and_player
    
    game.deck.cards.clear()
    game.deck.cards.append(Card("Clubs", "5", 5))

    player.get_current_hand().add_card(Card("Hearts", "10", 10))
    player.get_current_hand().add_card(Card("Diamonds", "Queen", 10))
    
    action.execute(game=game, player=player, action='hit')

    assert len(player.get_current_hand().cards) == 3
    assert player.get_current_hand().get_value() == 25
    assert player.get_current_hand().status == 'busted'

def test_player_action_stand(setup_game_and_player):
    game, player, action = setup_game_and_player
    
    action.execute(game=game, player=player, action='stand')

    assert player.get_current_hand().status == 'stand'

def test_player_action_invalid_action(setup_game_and_player):
    game, player, action = setup_game_and_player
    
    with pytest.raises(ValueError, match="Invalid action: foo"):
        action.execute(game=game, player=player, action='foo')

def test_player_action_wrong_state(setup_game_and_player):
    game, player, action = setup_game_and_player
    game.game_state = 'betting'
    
    with pytest.raises(ValueError, match="Not the player's turn."):
        action.execute(game=game, player=player, action='hit')

def test_player_action_double_down_success(setup_game_and_player):
    game, player, action = setup_game_and_player
    player.balance = 100
    player.place_bet(10)
    player.get_current_hand().add_card(Card("Hearts", "5", 5))
    player.get_current_hand().add_card(Card("Diamonds", "5", 5))
    game.deck.cards.clear()
    game.deck.cards.append(Card("Clubs", "10", 10)) # Card to be dealt

    action.execute(game=game, player=player, action='doubleDown')

    assert player.balance == 80 # 100 - 10 (original bet) - 10 (doubled bet)
    assert player.get_current_bet() == 20
    assert len(player.get_current_hand().cards) == 3
    assert player.get_current_hand().get_value() == 20
    assert player.get_current_hand().status == 'stand'

def test_player_action_double_down_bust(setup_game_and_player):
    game, player, action = setup_game_and_player
    player.balance = 100
    player.place_bet(10)
    player.get_current_hand().add_card(Card("Hearts", "10", 10))
    player.get_current_hand().add_card(Card("Diamonds", "7", 7))
    game.deck.cards.clear()
    game.deck.cards.append(Card("Clubs", "5", 5)) # Card to be dealt

    action.execute(game=game, player=player, action='doubleDown')

    assert player.balance == 80
    assert player.get_current_bet() == 20
    assert len(player.get_current_hand().cards) == 3
    assert player.get_current_hand().get_value() == 22
    assert player.get_current_hand().status == 'busted'

def test_player_action_double_down_insufficient_balance(setup_game_and_player):
    game, player, action = setup_game_and_player
    player.balance = 5
    player.place_bet(5)
    player.get_current_hand().add_card(Card("Hearts", "5", 5))
    player.get_current_hand().add_card(Card("Diamonds", "5", 5))

    with pytest.raises(ValueError, match="Insufficient balance to double down."):
        action.execute(game=game, player=player, action='doubleDown')

def test_player_action_double_down_not_two_cards(setup_game_and_player):
    game, player, action = setup_game_and_player
    player.balance = 100
    player.place_bet(10)
    player.get_current_hand().add_card(Card("Hearts", "5", 5)) # Only one card

    with pytest.raises(ValueError, match="Can only double down on a two-card hand."):
        action.execute(game=game, player=player, action='doubleDown')

    player.get_current_hand().add_card(Card("Diamonds", "5", 5))
    player.get_current_hand().add_card(Card("Clubs", "5", 5)) # Three cards

    with pytest.raises(ValueError, match="Can only double down on a two-card hand."):
        action.execute(game=game, player=player, action='doubleDown')

def test_player_action_double_down_wrong_state(setup_game_and_player):
    game, player, action = setup_game_and_player
    game.game_state = 'betting'
    player.balance = 100
    player.place_bet(10)
    player.get_current_hand().add_card(Card("Hearts", "5", 5))
    player.get_current_hand().add_card(Card("Diamonds", "5", 5))

    with pytest.raises(ValueError, match="Not the player's turn."):
        action.execute(game=game, player=player, action='doubleDown')

def test_player_action_split_success(setup_game_and_player):
    game, player, action = setup_game_and_player
    player.balance = 100
    player.place_bet(10)
    player.get_current_hand().add_card(Card("Hearts", "8", 8))
    player.get_current_hand().add_card(Card("Diamonds", "8", 8))
    game.deck.cards.clear()
    game.deck.cards.append(Card("Clubs", "7", 7)) # Card for second hand
    game.deck.cards.append(Card("Spades", "6", 6)) # Card for first hand

    action.execute(game=game, player=player, action='split')

    assert player.balance == 80 # 100 - 10 (original bet) - 10 (split bet)
    assert len(player.hands) == 2
    assert player.bets == [10, 10]
    assert len(player.hands[0].cards) == 2
    assert len(player.hands[1].cards) == 2
    assert player.hands[0].get_value() == 14 # 8 + 6
    assert player.hands[1].get_value() == 15 # 8 + 7
    assert player.hands[0].status == 'playing'
    assert player.hands[1].status == 'playing'

def test_player_action_split_insufficient_balance(setup_game_and_player):
    game, player, action = setup_game_and_player
    player.balance = 5
    player.place_bet(5)
    player.get_current_hand().add_card(Card("Hearts", "8", 8))
    player.get_current_hand().add_card(Card("Diamonds", "8", 8))

    with pytest.raises(ValueError, match="Insufficient balance to split."):
        action.execute(game=game, player=player, action='split')

def test_player_action_split_not_two_cards(setup_game_and_player):
    game, player, action = setup_game_and_player
    player.balance = 100
    player.place_bet(10)
    player.get_current_hand().add_card(Card("Hearts", "8", 8))

    with pytest.raises(ValueError, match="Can only split a two-card hand."):
        action.execute(game=game, player=player, action='split')

def test_player_action_split_cards_not_same_rank(setup_game_and_player):
    game, player, action = setup_game_and_player
    player.balance = 100
    player.place_bet(10)
    player.get_current_hand().add_card(Card("Hearts", "8", 8))
    player.get_current_hand().add_card(Card("Diamonds", "9", 9))

    with pytest.raises(ValueError, match="Cards must be of the same rank to split."):
        action.execute(game=game, player=player, action='split')

def test_player_action_split_wrong_state(setup_game_and_player):
    game, player, action = setup_game_and_player
    game.game_state = 'betting'
    player.balance = 100
    player.place_bet(10)
    player.get_current_hand().add_card(Card("Hearts", "8", 8))
    player.get_current_hand().add_card(Card("Diamonds", "8", 8))

    with pytest.raises(ValueError, match="Not the player's turn."):
        action.execute(game=game, player=player, action='split')
