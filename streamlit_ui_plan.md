# Streamlit UI Development Plan (Multipage)

## 1. Project Goal

The objective is to build a rich, interactive User Interface for the existing Blackjack game using Streamlit's multipage app functionality. This will replace the current command-line interface (CLI).

The UI will consist of two distinct pages:
1.  **Configuration Page:** Allows the user to set the rules of the game before playing.
2.  **Game Page:** The primary interface for playing the game.

## 2. Core Architectural Concepts

Our Clean Architecture is perfectly suited for this. The core game logic (Domain and Application layers) will remain untouched. We are building a new UI in the Infrastructure layer.

### Key Considerations for the Developer:

*   **State Management (`st.session_state`):** This remains the most critical concept. Since a user will navigate between separate page files (`.py` scripts), `st.session_state` is the **only** way to share data and maintain the game's state between pages. All core objects (`Game`, `GameController`, etc.) **must** be stored here.

*   **Multipage Navigation:** We will use `st.navigation` to create a clear, navigable sidebar. The main app file will act as a router, defining the pages. This is a cleaner approach than using `if/else` blocks to show/hide content.

*   **Component Isolation:** The logic for rendering UI elements (like a card) should be isolated in its own functions and files. This makes the page scripts cleaner and simplifies future updates (like switching from text-based cards to images).

---

## 3. Step-by-Step Development Plan

### Step 1: Project Setup (Multipage Structure)

1.  Create a new directory: `src/infrastructure/ui/streamlit/`.
2.  Inside this new directory, create the following files. This structure separates the main router from the pages themselves:
    *   `main_app.py`: The main entry point and navigation router for the Streamlit application.
    *   `pages/`: A new subdirectory to hold the page scripts.
        *   `config_page.py`: The UI and logic for the "Game Configuration" screen.
        *   `game_page.py`: The UI and logic for the main game board.
    *   `ui_components.py`: This will hold our reusable UI functions for rendering things like cards and hands.

### Step 2: Build the Main App Router (`main_app.py`)

This file configures and runs the navigation. It does not contain any page-specific UI code.

```python
import streamlit as st

# This is the main entry point for the app

def main():
    """Main function to configure and run the multipage app."""
    # Define the pages
    config_page = st.Page(
        "pages/config_page.py",
        title="Game Configuration",
        icon=":gear:"
    )
    game_page = st.Page(
        "pages/game_page.py",
        title="Blackjack Table",
        icon="♠️"
    )

    # Create the navigation menu
    pg = st.navigation([config_page, game_page])

    # Set the main page config
    st.set_page_config(page_title="Blackjack by vibeC", page_icon="🎲", layout="wide")

    # Run the navigation
    pg.run()

if __name__ == "__main__":
    main()
```

### Step 3: Build the Configuration Page (`pages/config_page.py`)

This page is responsible for setting up the game.

1.  **Display Title:** Use `st.title("Setup Your Blackjack Game")`.
2.  **Create Rule Widgets:** For each rule in the `GameRules` dataclass, create a corresponding Streamlit widget (e.g., `st.number_input`, `st.slider`, `st.checkbox`).
3.  **Create "Start Game" Button:**
    *   Use `if st.button("Start Game")`.
    *   **Inside this `if` block:**
        1.  Create an instance of `GameRules` using the values from the widgets.
        2.  Initialize the `Player`, `Game`, `GameController`, and `GamePresenter` objects.
        3.  Store these essential objects in the session state:
            *   `st.session_state.game = game`
            *   `st.session_state.controller = controller`
            *   `st.session_state.presenter = presenter`
        4.  Navigate to the game page: `st.switch_page("pages/game_page.py")`

### Step 4: Build the Game Page (`pages/game_page.py`)

This page is the main game interface. It will use a state machine approach based on the game state.

1.  **Add a Guardrail:** At the very top of the file, check if the game has been initialized. If not, direct the user back to the configuration page.
    ```python
    if 'game' not in st.session_state:
        st.warning("Please configure and start a new game from the 'Game Configuration' page first.")
        st.stop()
    ```
2.  **Get the View Model:** `view_model = st.session_state.presenter.present(st.session_state.game)`.
3.  **Implement the Game State Router:** Use `if/elif` to display the correct UI for the current state (`betting`, `playerTurn`, `roundOver`), as detailed in the previous version of this plan.
4.  **Import and Use UI Components:** Use the `display_hand` function from `ui_components.py` to render the player and dealer hands.

### Step 5: Create UI Components (`ui_components.py`)

This file's purpose remains the same. It decouples rendering logic from the page logic.

1.  **`display_card(card: dict)`:** Takes a card dictionary and renders it as text for now (`st.markdown`).
2.  **`display_hand(hand: list[dict])`:** Takes a list of cards, uses `st.columns` for layout, and calls `display_card` for each card.

### Step 6: Plan for Image-Based Cards (Future)

This plan remains unchanged. When ready, the developer will modify **only** the `display_card` function in `ui_components.py` to use `st.image`. The rest of the application will update automatically, demonstrating the power of this isolated design.