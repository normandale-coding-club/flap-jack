import random

cards = {
    "♠": [2, 3, 4, 5, 6, 7, 8, 9, 10],
    "♥": [2, 3, 4, 5, 6, 7, 8, 9, 10],
    "♦": [2, 3, 4, 5, 6, 7, 8, 9, 10],
    "♣": [2, 3, 4, 5, 6, 7, 8, 9, 10],
    "K": [10],
    "Q": [10],
    "J": [10],
    "A": [1, 11]
}

players = ["Player 1", "Player 2", "Player 3", "Player 4"]
scores = {player: 0 for player in players}
status = {player: "active" for player in players}
active_players = players.copy()
turn_count = 0


def choose_ace_value(player):
    while True:
        choice = input(f"{player}, choose one of these: 1 or 11: ").strip()
        if choice in ("1", "11"):
            return int(choice)
        print("Invalid choice. Please enter 1 or 11.")


def print_scoreboard():
    print("\n=== SCOREBOARD ===")
    for p in players:
        print(f"{p}: {scores[p]} points ({status[p]})")
    print("==================\n")


def bust_player(player):
    status[player] = "busted"
    if player in active_players:
        active_players.remove(player)
    print(f"{player} busted and is eliminated!")


def stand_player(player):
    status[player] = "stood"
    if player in active_players:
        active_players.remove(player)
    print(f"{player} chose to stand")


def play_round():
    global turn_count
    for player in active_players[:]:
        turn_count += 1

        if turn_count % len(players) == 0:
            print_scoreboard()

        print("Current:", player)
        card = random.choice(list(cards))

        if card == "A":
            num_took = choose_ace_value(player)
        else:
            num_took = random.choice(cards[card])

        print(player, "got", card, num_took)

        decision = input("Wish to hit or stand? (h/s): ").strip().lower()
        if decision == "h":
            scores[player] += num_took
            print(player, "chose to hit")
            if scores[player] > 21:
                bust_player(player)
        elif decision == "s":
            stand_player(player)
        else:
            dice = random.choice(["h", "s"])
            print(player, "chose to", "hit" if dice == "h" else "stand")
            if dice == "h":
                scores[player] += num_took
                if scores[player] > 21:
                    bust_player(player)
            else:
                stand_player(player)

        if not active_players:
            break


def find_winner():
    valid_scores = [(scores[p], p) for p in players if scores[p] <= 21]
    print("\n=== FINAL SCORES ===")
    for p in players:
        print(f"{p}: {scores[p]} points ({status[p]})")
    print("====================")

    if not valid_scores:
        print("No winner: all players busted.")
        return

    best_score = max(valid_scores)[0]
    winners = [p for score, p in valid_scores if score == best_score]

    if len(winners) == 1:
        print(f"Winner: {winners[0]} with {best_score} points!")
    else:
        print(f"It's a tie between {', '.join(winners)} with {best_score} points!")


def main():
    print("Starting the card game. Every player can hit until they stand or bust.")
    while active_players:
        play_round()
    find_winner()


if __name__ == "__main__":
    main()
    
