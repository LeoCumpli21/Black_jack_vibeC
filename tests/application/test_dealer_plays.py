import pytest
from src.domain.Game import Game
from src.domain.Player import Player
from src.domain.GameRules import GameRules
from src.application.dealer_plays import DealerPlays
from src.domain.Card import Card

def test_dealer_plays_hit_until_17():
    rules = GameRules()
    game = Game(players=[], rules=rules)
    game.game_state = 'dealerTurn'
    
    game.dealer.hands[0].add_card(Card("Hearts", "10", 10))
    game.dealer.hands[0].add_card(Card("Diamonds", "6", 6))
    
    game.deck.cards.clear()
    game.deck.cards.append(Card("Clubs", "5", 5))

    dealer_plays = DealerPlays()
    dealer_plays.execute(game)

    assert game.dealer.hands[0].get_value() == 21
    assert game.dealer.hands[0].status == 'stand'

def test_dealer_plays_stand_on_17():
    rules = GameRules(dealer_hits_on_soft_17=False)
    game = Game(players=[], rules=rules)
    game.game_state = 'dealerTurn'
    
    game.dealer.hands[0].add_card(Card("Hearts", "10", 10))
    game.dealer.hands[0].add_card(Card("Diamonds", "7", 7))
    
    dealer_plays = DealerPlays()
    dealer_plays.execute(game)

    assert game.dealer.hands[0].get_value() == 17
    assert len(game.dealer.hands[0].cards) == 2
    assert game.dealer.hands[0].status == 'stand'

def test_dealer_plays_hit_on_soft_17():
    rules = GameRules(dealer_hits_on_soft_17=True)
    game = Game(players=[], rules=rules)
    game.game_state = 'dealerTurn'
    
    game.dealer.hands[0].add_card(Card("Hearts", "Ace", 11))
    game.dealer.hands[0].add_card(Card("Diamonds", "6", 6))
    
    game.deck.cards.clear()
    game.deck.cards.append(Card("Clubs", "5", 5))

    dealer_plays = DealerPlays()
    dealer_plays.execute(game)

    assert game.dealer.hands[0].get_value() == 12
    assert len(game.dealer.hands[0].cards) == 3
    assert game.dealer.hands[0].status == 'stand'

def test_dealer_stands_at_18():
    rules = GameRules()
    game = Game(players=[], rules=rules)
    game.game_state = 'dealerTurn'
    
    game.dealer.hands[0].add_card(Card("Hearts", "10", 10))
    game.dealer.hands[0].add_card(Card("Diamonds", "8", 8)) # Hand value is 18
    
    dealer_plays = DealerPlays()
    dealer_plays.execute(game)

    assert game.dealer.hands[0].get_value() == 18
    assert game.dealer.hands[0].status == 'stand'

def test_dealer_busts():
    rules = GameRules()
    game = Game(players=[], rules=rules)
    game.game_state = 'dealerTurn'
    
    game.dealer.hands[0].add_card(Card("Hearts", "10", 10))
    game.dealer.hands[0].add_card(Card("Diamonds", "6", 6)) # Hand value is 16
    
    game.deck.cards.clear()
    game.deck.cards.append(Card("Clubs", "10", 10)) # Dealer hits and gets 10, busts.

    dealer_plays = DealerPlays()
    dealer_plays.execute(game)

    assert game.dealer.hands[0].get_value() == 26
    assert game.dealer.hands[0].status == 'busted'
    
def test_dealer_plays_wrong_state():
    rules = GameRules()
    game = Game(players=[], rules=rules)
    game.game_state = 'playerTurn'
    
    dealer_plays = DealerPlays()
    with pytest.raises(ValueError, match="Not the dealer's turn."):
        dealer_plays.execute(game)
