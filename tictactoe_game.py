# 🎮 Tic-Tac-Toe with Alpha-Beta Pruning
# Author: Jerstin Mangahis Mane
# Description: Human (X - Blue) vs AI (O - Yellow) with Alpha-Beta Pruning

# --- STEP 1: Display Board ---

def print_board(board):
    """Display the board in a neat 3x3 grid with color and numbering."""
    print("\n")
    for i in range(0, 9, 3):
        row = []
        for j in range(3):
            cell = board[i + j]
            if cell == 'X':
                row.append("\033[34mX\033[0m")  # Blue X
            elif cell == 'O':
                row.append("\033[33mO\033[0m")  # Yellow O
            else:
                row.append(str(i + j + 1))  # Show box number
        print("  " + " | ".join(row))
        if i < 6:
            print(" ---+---+---")
    print("\n")

# --- STEP 2: Game Rules & Helpers ---

LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6)
]

def winner(board):
    for a, b, c in LINES:
        if board[a] != ' ' and board[a] == board[b] == board[c]:
            return board[a]
    return None

def moves(board):
    return [i for i, v in enumerate(board) if v == ' ']

def terminal(board):
    return winner(board) is not None or not moves(board)

# --- STEP 3: Utility Function ---

def utility(board, me='O', opp='X'):
    w = winner(board)
    if w == me:
        return 1
    elif w == opp:
        return -1
    else:
        return 0

# --- STEP 4: Alpha-Beta Pruning ---

def alphabeta(board, player, alpha=-2, beta=2, me='O', opp='X'):
    if terminal(board):
        return utility(board, me, opp), None

    if player == me:
        best = (-2, None)  # MAX node
        for m in moves(board):
            b2 = board[:]
            b2[m] = player
            val, _ = alphabeta(b2, opp, alpha, beta, me, opp)
            if val > best[0]:
                best = (val, m)
            alpha = max(alpha, val)
            if alpha >= beta:  # prune
                break
        return best
    else:
        best = (2, None)  # MIN node
        for m in moves(board):
            b2 = board[:]
            b2[m] = player
            val, _ = alphabeta(b2, me, alpha, beta, me, opp)
            if val < best[0]:
                best = (val, m)
            beta = min(beta, val)
            if alpha >= beta:  # prune
                break
        return best

# --- STEP 5: Game Loop ---

def play_game():
    board = [' '] * 9
    human = 'X'
    ai = 'O'

    print("\n\033[36m═══════════════════════════════════════════\033[0m")
    print("You are \033[34mX (Blue)\033[0m, AI is \033[33mO (Yellow)\033[0m.")
    print("\033[36m═══════════════════════════════════════════\033[0m")
    print_board(board)

    first = input("Do you want to go first? (y/n): ").strip().lower().startswith('y')
    current = human if first else ai

    while not terminal(board):
        if current == human:
            try:
                move = int(input("\033[34mYour move (1-9): \033[0m")) - 1
            except ValueError:
                print("Please enter a valid number (1-9).")
                continue
            if move not in moves(board):
                print("That spot is already taken or invalid.")
                continue
            board[move] = human
        else:
            print("\033[33mAI is thinking...🧠\033[0m")
            _, move = alphabeta(board, player=ai, alpha=-2, beta=2, me=ai, opp=human)
            board[move] = ai
            print(f"\033[33mAI chose position {move + 1}\033[0m")

        print_board(board)
        current = ai if current == human else human

    w = winner(board)
    if w == human:
        print("🎉 You win! Great job!")
    elif w == ai:
        print("🤖 AI wins! Better luck next time!")
    else:
        print("😐 It's a draw!")

# --- STEP 6: Run the Game ---

if __name__ == "__main__":
    play_game()
