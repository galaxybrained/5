import os

# Clear the console screen
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

# Tic Tac Toe

# Function to print the board
def print_board(board):
    clear_screen()
    print("╔═══╦═══╦═══╗")
    print(f"║ {board[0]} ║ {board[1]} ║ {board[2]} ║")
    print("╠═══╬═══╬═══╣")
    print(f"║ {board[3]} ║ {board[4]} ║ {board[5]} ║")
    print("╠═══╬═══╬═══╣")
    print(f"║ {board[6]} ║ {board[7]} ║ {board[8]} ║")
    print("╚═══╩═══╩═══╝")
    print("\n")

# Function to check if any player has won
def check_win(board):
    # Check rows
    for i in range(0, 9, 3):
        if board[i] == board[i + 1] == board[i + 2] != " ":
            return board[i]

    # Check columns
    for i in range(3):
        if board[i] == board[i + 3] == board[i + 6] != " ":
            return board[i]

    # Check diagonals
    if board[0] == board[4] == board[8] != " ":
        return board[0]
    if board[2] == board[4] == board[6] != " ":
        return board[2]

    return None

# Function to play a round of the game
def play_round(player1, player2):
    board = [" " for _ in range(9)]  # Create a new board for each round
    current_player = "X"

    while True:
        print_board(board)

        # Get the player's move
        move = input(f"{player1 if current_player == 'X' else player2}, enter your move (1-9): ")

        # Validate the move
        if not move.isdigit() or not (1 <= int(move) <= 9):
            clear_screen()
            print("Invalid move. Please enter a number from 1 to 9.\n")
            continue

        move = int(move) - 1

        if board[move] != " ":
            clear_screen()
            print("That position is already occupied. Please choose an empty position.\n")
            continue

        # Update the board
        board[move] = current_player

        # Check for a win
        winner = check_win(board)
        if winner:
            clear_screen()
            print_board(board)
            print(f"Congratulations, {player1 if winner == 'X' else player2}! You won this round!\n")
            return winner

        # Check for a draw
        if " " not in board:
            clear_screen()
            print_board(board)
            print("It's a draw!\n")
            return None

        # Switch players
        current_player = "O" if current_player == "X" else "X"

# Function to play the game with multiple rounds
def play_game():
    clear_screen()
    print("Welcome to Tic Tac Toe Tournament!\n")

    player1 = input("Enter Player 1's name: ")
    player2 = input("Enter Player 2's name: ")
    rounds = int(input("Enter the number of rounds to play: "))

    player1_score = 0
    player2_score = 0

    for round_num in range(1, rounds + 1):
        print(f"\nRound {round_num}:")

        winner = play_round(player1, player2)

        if winner == "X":
            player1_score += 1
        elif winner == "O":
            player2_score += 1

    clear_screen()
    print("Tournament Results:\n")
    print(f"{player1}: {player1_score} wins")
    print(f"{player2}: {player2_score} wins")

    if player1_score > player2_score:
        print(f"\nCongratulations, {player1}! You are the winner of the tournament!")
    elif player2_score > player1_score:
        print(f"\nCongratulations, {player2}! You are the winner of the tournament!")
    else:
        print("\nIt's a tie! The tournament ended in a draw.")

# Start the game
play_game()
