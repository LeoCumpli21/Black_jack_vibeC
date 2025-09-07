# Digital Blackjack Game Functionality

## 1. Introduction

This document outlines the functional requirements for creating a digital Blackjack game. It is intended for developers and provides a breakdown of the game's objects, flow, and logic, based on the rules defined in `casino_black_jack_table_rules.md`.

## 2. Core Game Objects (Data Structures)

### `Card`
*   **Attributes:**
    *   `suit`: (String) e.g., 'Hearts', 'Diamonds', 'Clubs', 'Spades'.
    *   `rank`: (String) e.g., '2', '10', 'King', 'Ace'.
    *   `value`: (Integer or Array) The game value of the card. e.g., 10 for face cards, [1, 11] for an Ace.

### `Deck`
*   **Attributes:**
    *   `cards`: (Array of `Card` objects) The collection of cards in the deck.
*   **Methods:**
    *   `constructor(numberOfDecks)`: Creates a deck with the specified number of 52-card decks.
    *   `shuffle()`: Randomizes the order of the `cards` array.
    *   `deal()`: Removes and returns the top card from the deck.

### `Hand`
*   **Attributes:**
    *   `cards`: (Array of `Card` objects) The cards currently in the hand.
*   **Methods:**
    *   `addCard(card)`: Adds a card to the hand.
    *   `getValue()`: (Integer) Calculates the total value of the hand, intelligently handling the value of Aces (1 or 11) to get the best possible score without busting.

### `Player`
*   **Attributes:**
    *   `hand`: (Hand object) The player's current hand.
    *   `balance`: (Integer) The player's current money.
    *   `bet`: (Integer) The amount the player has bet in the current round.
    *   `status`: (String) The player's current status, e.g., 'betting', 'playing', 'busted', 'stand'.

### `Dealer`
*   **Inherits from:** `Player`.
*   **Additional Logic:** The dealer has a specific set of rules for playing their hand (e.g., must hit until 17).

### `Game`
*   **Attributes:**
    *   `deck`: (`Deck` object)
    *   `players`: (Array of `Player` objects)
    *   `dealer`: (`Dealer` object)
    *   `gameState`: (String) The current state of the game, e.g., 'betting', 'dealing', 'playerTurn', 'dealerTurn', 'roundOver'.
    *   `minBet`, `maxBet`: (Integer) The table's betting limits.

## 3. Game Flow (State Machine)

1.  **Initialization:**
    *   Create a `Game` object.
    *   Instantiate `Player` and `Dealer` objects.
    *   Create and shuffle the `Deck` with a configurable number of decks.

2.  **Betting Phase (`betting` state):**
    *   Prompt each player to place a bet within the `minBet` and `maxBet` limits.
    *   Once all players have placed their bets, transition to the `dealing` state.

3.  **Dealing Phase (`dealing` state):**
    *   Deal two cards to each player and the dealer, one at a time, face up.
    *   The dealer's second card is dealt face down.
    *   Check for any Blackjacks. If a player has Blackjack, they are paid 3 to 2 immediately, unless the dealer also has Blackjack (in which case it's a push).
    *   Transition to the `playerTurn` state.

4.  **Player's Turn (`playerTurn` state):**
    *   For each player, in sequence:
        *   Allow the player to perform actions: `hit`, `stand`, `doubleDown`, `split`, `surrender`.
        *   The available actions depend on the player's hand and the game rules.
        *   If the player busts or stands, their turn is over.
    *   Once all players have finished their turns, transition to the `dealerTurn` state.

5.  **Dealer's Turn (`dealerTurn` state):**
    *   Reveal the dealer's face-down card.
    *   The dealer plays their hand according to the fixed rules:
        *   Hit until the hand value is 17 or more.
        *   A configurable rule determines if the dealer hits or stands on a soft 17.
    *   Transition to the `roundOver` state.

6.  **Resolution Phase (`roundOver` state):**
    *   Compare each player's hand to the dealer's hand.
    *   Determine the outcome for each player (win, lose, push).
    *   Settle all bets and update player balances.
    *   Prepare for the next round. Check if the deck needs to be shuffled.
    *   Transition back to the `betting` state.

## 4. Player Actions (Functions/Methods)

*   `placeBet(amount)`: The player places a bet.
*   `hit()`: The player requests one more card.
*   `stand()`: The player ends their turn.
*   `doubleDown()`: The player doubles their bet and receives exactly one more card.
*   `split()`: If the player has two cards of the same value, they can split them into two separate hands, placing a second bet.
*   `surrender()`: The player forfeits their hand and half their bet.
*   `takeInsurance()`: If the dealer's upcard is an Ace, the player can place a side bet that the dealer has Blackjack.

## 5. UI/UX Elements

*   **Table View:** A visual representation of the Blackjack table.
*   **Card Display:** Clear visuals for each card in a player's and the dealer's hand.
*   **Action Buttons:** Buttons for `hit`, `stand`, etc. These should be enabled or disabled based on the current game state and the player's hand.
*   **Betting Interface:** An interface for players to place their bets.
*   **Information Display:** A display for player balances, current bets, and hand values.
*   **Game Messages:** A text area to display messages like "Player wins", "Bust!", "Dealer has Blackjack", etc.
