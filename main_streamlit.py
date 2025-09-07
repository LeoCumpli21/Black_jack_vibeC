import streamlit as st


def main():
    """Main function to configure and run the multipage app."""
    # Define the pages
    config_page = st.Page(
        "src/infrastructure/ui/streamlit/pages/config_page.py",
        title="Game Configuration",
    )
    game_page = st.Page(
        "src/infrastructure/ui/streamlit/pages/game_page.py",
        title="Blackjack Table",
        icon="♠️",
    )

    # Create the navigation menu
    pg = st.navigation([config_page, game_page])

    # Set the main page config
    st.set_page_config(page_title="Blackjack by vibeC", page_icon="🎲", layout="wide")

    # Run the navigation
    pg.run()


if __name__ == "__main__":
    main()
