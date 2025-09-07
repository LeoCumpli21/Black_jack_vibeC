# Blackjack Game: Clean Architecture Development Plan

## 1. Introduction

This document provides a development plan for creating the Blackjack game following the principles of Clean Architecture. This approach will ensure a separation of concerns, making the game logic independent of any specific framework, UI, or database. The result will be a system that is easy to maintain, test, and scale.

## 2. Clean Architecture Layers

We will structure the application into the following layers, starting from the core:

### Layer 1: Entities (Domain Layer)

This layer contains the core business objects and rules of the game. These are the most fundamental and high-level concepts.

*   **`Card`**: Represents a single playing card with a suit, rank, and value.
*   **`Hand`**: Represents a collection of cards held by a player or dealer, including logic to calculate the hand's value.
*   **`Player`**: Represents a player, holding a hand, a balance, and a current bet.
*   **`Dealer`**: A specialized `Player` with its own set of rules for playing.
*   **`GameRules`**: An entity that encapsulates the rules of the game, such as the payout for Blackjack, whether the dealer hits on a soft 17, etc.

### Layer 2: Use Cases (Application Layer)

This layer orchestrates the flow of data between the entities and the outer layers. It contains the application-specific business logic.

*   **`StartRound`**: Initializes a new round of the game.
*   **`PlaceBet`**: A use case for a player to place a bet.
*   **`PlayerAction`**: A single use case to handle all player actions (`hit`, `stand`, `doubleDown`, `split`, `surrender`, `insurance`). This use case will take the player's action as input.
*   **`DealerPlays`**: A use case that executes the dealer's turn based on the game rules.
*   **`DetermineOutcome`**: A use case to determine the winner of the round and calculate payouts.

### Layer 3: Interface Adapters

This layer acts as a bridge between the core application and the external world (UI, databases, etc.).

*   **`GameController`**: Receives input from the UI (e.g., a player clicks the "Hit" button) and passes it to the appropriate use case.
*   **`GamePresenter`**: Takes the output from the use cases and formats it into a `ViewModel` that is easy for the UI to display. It decouples the core application from the UI implementation.
*   **`GameStateGateway`**: (Optional) An interface for saving and loading the game state, allowing for persistence.

### Layer 4: Frameworks & Drivers

This is the outermost layer, containing the specific implementations of external concerns.

*   **`UI`**: The user interface of the game. This could be a web application (e.g., using React, Vue, or Angular), a mobile app, or a desktop application.
*   **`DataPersistence`**: The implementation of the `GameStateGateway`, e.g., using browser `localStorage`, a file, or a database.

## 3. Development Steps

Development should proceed from the inside out, starting with the core domain logic.

### Step 1: Implement the Domain Layer (Entities)

1.  Create the `Card`, `Hand`, `Player`, and `Dealer` classes with their attributes and methods.
2.  These classes should be plain objects with no dependencies on any other layer.
3.  Write comprehensive unit tests for this layer to ensure the core game logic is correct (e.g., test hand value calculations with Aces).

### Step 2: Implement the Application Layer (Use Cases)

1.  Create the use case classes (`StartRound`, `PlayerAction`, etc.).
2.  These classes will depend on the entities from the domain layer but nothing from the outer layers.
3.  Implement the game's state machine logic within these use cases.
4.  Write unit tests for each use case to verify the application logic.

### Step 3: Implement the Interface Adapters

1.  Create the `GameController` to handle user input.
2.  Create the `GamePresenter` to format data for the UI.
3.  Define the interfaces for any gateways (like `GameStateGateway`).

### Step 4: Implement the UI (Frameworks & Drivers)

1.  Choose a UI framework (e.g., React for a web app).
2.  Build the UI components to display the game state (cards, buttons, etc.).
3.  Connect the UI to the `GameController` for handling user actions and to the `GamePresenter` for receiving state updates.

## 4. Proposed Directory Structure

```
/src
  /domain
    - Card.py
    - Hand.py
    - Player.py
    - Dealer.py
    - GameRules.py
  /application
    - StartRound.py
    - PlayerAction.py
    - DealerPlays.py
    - DetermineOutcome.py
  /interface-adapters
    - GameController.py
    - GamePresenter.py
    - GameStateGateway.py
  /infrastructure
    /ui
      - GameView.py
      - CardComponent.py
      - ... (other UI components)
    /persistence
      - LocalStorageGameState.py
```
