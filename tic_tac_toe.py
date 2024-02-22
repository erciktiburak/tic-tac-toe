import tkinter as tk
import random

# Constants
EMPTY = ""
PLAYER_X = "X"
PLAYER_O = "O"
WINNING_COMBOS = [
    [(0, 0), (0, 1), (0, 2)],  # Row 1
    [(1, 0), (1, 1), (1, 2)],  # Row 2
    [(2, 0), (2, 1), (2, 2)],  # Row 3
    [(0, 0), (1, 0), (2, 0)],  # Column 1
    [(0, 1), (1, 1), (2, 1)],  # Column 2
    [(0, 2), (1, 2), (2, 2)],  # Column 3
    [(0, 0), (1, 1), (2, 2)],  # Diagonal 1
    [(0, 2), (1, 1), (2, 0)]   # Diagonal 2
]

class TicTacToe:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic-Tac-Toe")
        self.board = [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]
        self.current_player = PLAYER_X
        self.create_widgets()
        self.reset_game()

    def create_widgets(self):
        self.buttons = [[None, None, None], [None, None, None], [None, None, None]]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.master, text="", font=("Helvetica", 24), width=5, height=2,
                                                command=lambda i=i, j=j: self.make_move(i, j))
                self.buttons[i][j].grid(row=i, column=j)

    def reset_game(self):
        self.board = [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]
        self.current_player = PLAYER_X
        self.update_board_ui()

    def update_board_ui(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j]["text"] = self.board[i][j]

    def make_move(self, row, col):
        if self.board[row][col] == EMPTY:
            self.board[row][col] = self.current_player
            self.update_board_ui()
            if self.check_winner(self.current_player):
                self.display_winner(self.current_player)
                self.reset_game()
                return
            if self.is_board_full():
                self.display_winner("Draw")
                self.reset_game()
                return
            self.current_player = PLAYER_O if self.current_player == PLAYER_X else PLAYER_X
            if self.current_player == PLAYER_O:
                self.ai_make_move()

    def ai_make_move(self):
        # Simple AI: Randomly select an empty square
        empty_squares = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == EMPTY]
        if empty_squares:
            row, col = random.choice(empty_squares)
            self.make_move(row, col)

    def check_winner(self, player):
        for combo in WINNING_COMBOS:
            if all(self.board[i][j] == player for i, j in combo):
                return True
        return False

    def is_board_full(self):
        return all(all(cell != EMPTY for cell in row) for row in self.board)

    def display_winner(self, player):
        if player == "Draw":
            winner_text = "It's a draw!"
        else:
            winner_text = f"Player {player} wins!"
        winner_label = tk.Label(self.master, text=winner_text, font=("Helvetica", 16))
        winner_label.grid(row=3, column=0, columnspan=3)

# Create the main window
root = tk.Tk()
game = TicTacToe(root)

# Start the GUI event loop
root.mainloop()