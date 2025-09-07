from src.interface_adapters.game_controller import GameController
from src.interface_adapters.game_presenter import GamePresenter
from src.domain.Game import Game
from src.domain.Player import Player
from src.domain.GameRules import GameRules


def main():
    # Initialization
    player = Player(balance=100)
    rules = GameRules()
    game = Game(players=[player], rules=rules)
    controller = GameController(game)
    presenter = GamePresenter()

    print("Welcome to Blackjack!")

    while True:
        # Betting
        while True:
            try:
                bet_amount = int(input(f"You have ${player.balance}. Place your bet: "))
                if bet_amount > 0 and bet_amount <= player.balance:
                    controller.place_bets({player: bet_amount})
                    break
                else:
                    print("Invalid bet amount.")
            except ValueError:
                print("Please enter a number.")

        # Start Round
        controller.start_new_round()

        # Player's Turn
        while player.get_overall_status() == "playing":
            view_model = presenter.present(game)
            
            # Display all player hands
            for hand_vm in view_model.players:
                print(f"Your hand {hand_vm.hand_index + 1}: {hand_vm.cards} (Value: {hand_vm.value})")

            print(f"Dealer's hand: {view_model.dealer_cards}")

            current_hand = player.get_current_hand()

            # Determine available actions based on player's current hand and game state
            available_actions = ["h", "s"]
            # Double down is only available on the first action of a hand (2 cards)
            if len(current_hand.cards) == 2 and player.balance >= player.bets[player.current_hand_index]:
                available_actions.append("d") # Double Down
                # Split is only available on the first action of a hand with two same-rank cards
                if current_hand.cards[0].rank == current_hand.cards[1].rank:
                    available_actions.append("sp") # Split
            
            action_prompt = "Do you want to (h)it, (s)tand"
            if "d" in available_actions:
                action_prompt += ", (d)oubleDown"
            if "sp" in available_actions:
                action_prompt += ", (sp)lit"
            action_prompt += "? "

            action = input(action_prompt).lower()

            if action in ["h", "hit"]:
                controller.perform_player_action(player, "hit")
            elif action in ["s", "stand"]:
                controller.perform_player_action(player, "stand")
            elif action in ["d", "doubledown"] and "d" in available_actions:
                controller.perform_player_action(player, "doubleDown")
                # Re-present view model to show the new card after double down
                view_model = presenter.present(game)
                for hand_vm in view_model.players:
                    if hand_vm.hand_index == player.current_hand_index: # Only show the hand that was just acted upon
                        print(f"Your hand {hand_vm.hand_index + 1}: {hand_vm.cards} (Value: {hand_vm.value})")
                print(f"You doubled down. Your bet for this hand is now ${player.get_current_bet()}")
            elif action in ["sp", "split"] and "sp" in available_actions:
                controller.perform_player_action(player, "split")
                # Re-present view model to show the new hands after split
                view_model = presenter.present(game)
                for hand_vm in view_model.players:
                    print(f"Your hand {hand_vm.hand_index + 1}: {hand_vm.cards} (Value: {hand_vm.value})")
                    print(f"Bet for hand {hand_vm.hand_index + 1} is ${player.bets[hand_vm.hand_index]}")
            else:
                print("Invalid action or action not available.")

        # Dealer's Turn
        game.game_state = "dealerTurn"
        controller.dealer_turn()

        # Get view model before determining outcome (which clears hands)
        view_model = presenter.present(game)

        # End of Round (determines outcome, clears hands, resets bets/status)
        controller.end_round()

        print(
            f"Dealer's hand: {view_model.dealer_cards} (Value: {view_model.dealer_value})"
        )

        # Display final player hands and values
        for hand_vm in view_model.players:
            print(f"Your final hand {hand_vm.hand_index + 1}: {hand_vm.cards} (Value: {hand_vm.value})")

        # Determine Outcome (using the status from the view_model, which was captured before reset)
        player_overall_status = player.get_overall_status()
        if player_overall_status == "win":
            print("You win!")
        elif player_overall_status == "lose":
            print("You lose.")
        elif player_overall_status == "push":
            print("It's a push.")
        elif player_overall_status == "busted":
            print("You busted!")

        print(f"Your new balance is ${player.balance}")

        play_again = input("Play another round? (y/n): ").lower()
        if play_again != "y":
            break


if __name__ == "__main__":
    main()
