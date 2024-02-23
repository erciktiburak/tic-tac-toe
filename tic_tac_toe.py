import tkinter as tk
import random
import json

EMPTY = ""
PLAYER_X = "X"
PLAYER_O = "O"
WINNING_COMBOS = [
    [(0, 0), (0, 1), (0, 2)],
    [(1, 0), (1, 1), (1, 2)],
    [(2, 0), (2, 1), (2, 2)],
    [(0, 0), (1, 0), (2, 0)],
    [(0, 1), (1, 1), (2, 1)],
    [(0, 2), (1, 2), (2, 2)],
    [(0, 0), (1, 1), (2, 2)],
    [(0, 2), (1, 1), (2, 0)]
]

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.score = 0

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "score": self.score
        }

    @staticmethod
    def from_dict(data):
        user = User(data["username"], data["password"])
        user.score = data["score"]
        return user

class TicTacToe:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic-Tac-Toe")
        self.board = [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]
        self.current_player = PLAYER_X
        self.create_widgets()
        self.load_users()

    def create_widgets(self):
        # Create UI elements
        self.login_frame = tk.Frame(self.master)
        self.login_frame.pack()
        self.username_label = tk.Label(self.login_frame, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.pack()
        self.password_label = tk.Label(self.login_frame, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.pack()
        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.pack()
        self.register_button = tk.Button(self.login_frame, text="Register", command=self.register)
        self.register_button.pack()

        self.game_frame = tk.Frame(self.master)
        self.game_frame.pack()
        self.buttons = [[None, None, None], [None, None, None], [None, None, None]]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.game_frame, text="", font=("Helvetica", 24), width=5, height=2,
                                                command=lambda i=i, j=j: self.make_move(i, j))
                self.buttons[i][j].grid(row=i, column=j)

        self.score_label = tk.Label(self.master, text="Score: 0")
        self.score_label.pack()

    def load_users(self):
        try:
            with open("users.json", "r") as file:
                data = json.load(file)
                self.users = [User.from_dict(user_data) for user_data in data]
        except FileNotFoundError:
            self.users = []

    def save_users(self):
        with open("users.json", "w") as file:
            data = [user.to_dict() for user in self.users]
            json.dump(data, file, indent=4)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        for user in self.users:
            if user.username == username and user.password == password:
                self.current_user = user
                self.update_score_label()
                self.switch_to_game()
                return
        # Login failed
        tk.messagebox.showerror("Error", "Invalid username or password")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if any(user.username == username for user in self.users):
            tk.messagebox.showerror("Error", "Username already exists")
            return
        user = User(username, password)
        self.users.append(user)
        self.current_user = user
        self.save_users()
        self.update_score_label()
        self.switch_to_game()

    def switch_to_game(self):
        self.login_frame.pack_forget()
        self.game_frame.pack()

    def update_score_label(self):
        self.score_label.config(text=f"Score: {self.current_user.score}")

    # Remaining game logic remains the same as before

root = tk.Tk()
game = TicTacToe(root)
root.mainloop()