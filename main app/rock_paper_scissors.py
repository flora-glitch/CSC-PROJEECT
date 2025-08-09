import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import json
from pathlib import Path

# Enhanced Rock-Paper-Scissors GUI
# Features:
# - Player name input
# - Mode: Classic (R/P/S) or Extended (R/P/S/Lizard/Spock)
# - Difficulty: Easy / Medium / Hard (adaptive)
# - Best-of-N rounds selection (first to wins_needed wins)
# - Scoreboard, round history, stats saved to rps_stats.json
# - Keyboard shortcuts and emojis
# - Reset stats and reset match buttons

STATS_FILE = Path("rps_stats.json")

CLASSIC_CHOICES = ["rock", "paper", "scissors"]
EXTENDED_CHOICES = ["rock", "paper", "scissors", "lizard", "spock"]


# For each choice, list choices it defeats
WIN_MAP = {
    "rock": ["scissors", "lizard"],
    "paper": ["rock", "spock"],
    "scissors": ["paper", "lizard"],
    "lizard": ["paper", "spock"],
    "spock": ["scissors", "rock"]
}


class RPSApp:
    def _init_(self, root):
        self.root = root
        root.title("🎮 Rock Paper Scissors — Enhanced")
        root.geometry("800x520")
        root.resizable(False, False)

        # State
        self.player_name = tk.StringVar(value="Player")
        self.mode = tk.StringVar(value="Classic")
        self.difficulty = tk.StringVar(value="Easy")
        self.best_of = tk.IntVar(value=3)
        self.auto_restart = tk.BooleanVar(value=False)

        self.choices = CLASSIC_CHOICES.copy()
        self.wins_needed = self.best_of.get() // 2 + 1

        self.player_score = 0
        self.comp_score = 0
        self.ties = 0
        self.round_number = 0

        self.player_history = []  # list of player's choices for AI
        self.history = []  # round history lines

        self.stats = self.load_stats()

        self.build_ui()
        self.bind_keys()
        self.update_ui_for_mode()

    # ---------------- Stats ----------------
    def load_stats(self):
        if STATS_FILE.exists():
            try:
                return json.loads(STATS_FILE.read_text(encoding="utf-8"))
            except Exception:
                return {}
        return {}

    def save_stats(self):
        try:
            STATS_FILE.write_text(json.dumps(self.stats, indent=2), encoding="utf-8")
        except Exception as e:
            print("Could not save stats:", e)

    def reset_stats(self):
        if messagebox.askyesno("Reset stats", "Delete saved stats?"):
            self.stats = {}
            if STATS_FILE.exists():
                try:
                    STATS_FILE.unlink()
                except Exception:
                    pass
            self.update_stats_panel()

    # ---------------- UI ----------------
    def build_ui(self):
        # Top settings frame
        top = tk.Frame(self.root, padx=10, pady=6)
        top.pack(fill="x")

        tk.Label(top, text="Name:").pack(side="left")
        tk.Entry(top, textvariable=self.player_name, width=14).pack(side="left", padx=(0, 12))

        tk.Label(top, text="Mode:").pack(side="left")
        tk.OptionMenu(top, self.mode, "Classic", "Extended", command=lambda _: self.update_ui_for_mode()).pack(side="left", padx=(0, 12))

        tk.Label(top, text="Difficulty:").pack(side="left")
        tk.OptionMenu(top, self.difficulty, "Easy", "Medium", "Hard").pack(side="left", padx=(0, 12))

        tk.Label(top, text="Best of:").pack(side="left")
        tk.OptionMenu(top, self.best_of, 1, 3, 5, 7, 9, command=lambda _: self.update_wins_needed()).pack(side="left", padx=(0, 12))

        tk.Checkbutton(top, text="Auto-restart", variable=self.auto_restart).pack(side="left", padx=(0, 12))

        tk.Button(top, text="Start New Match", command=self.start_new_match).pack(side="right", padx=(10,0))
        tk.Button(top, text="Reset Stats", command=self.reset_stats).pack(side="right")

        # Middle frame with choices and scoreboard/history
        middle = tk.Frame(self.root)
        middle.pack(fill="both", expand=True, padx=10, pady=6)

        # Left: buttons for choices
        left = tk.Frame(middle, bd=1, relief="sunken", padx=10, pady=10)
        left.pack(side="left", fill="y", padx=(0,10))

        tk.Label(left, text="Choose:", font=("Arial", 14, "bold")).pack(pady=(0,8))

        self.choice_buttons = {}
        for choice in EXTENDED_CHOICES:
            btn = tk.Button(left, text=f"{EMOJI[choice]}  {choice.title()}", width=14, height=2,
                            command=lambda c=choice: self.player_move(c))
            btn.pack(pady=4)
            self.choice_buttons[choice] = btn

        # center: scoreboard
        center = tk.Frame(middle, bd=1, relief="sunken", padx=10, pady=10)
        center.pack(side="left", fill="both", expand=True)

        self.score_label = tk.Label(center, text="Player 0  —  0 Computer", font=("Arial", 20, "bold"))
        self.score_label.pack(pady=(4,8))

        self.round_label = tk.Label(center, text="Round: 0", font=("Arial", 12))
        self.round_label.pack()

        result_frame = tk.Frame(center)
        result_frame.pack(pady=8)
        self.result_var = tk.StringVar(value="Make your move!")
        self.result_label = tk.Label(result_frame, textvariable=self.result_var, font=("Arial", 16))
        self.result_label.pack()

        # history listbox
        hist_frame = tk.Frame(center)
        hist_frame.pack(fill="both", expand=True, pady=(12,0))
        tk.Label(hist_frame, text="Round History").pack()
        self.history_listbox = tk.Listbox(hist_frame, height=10)
        self.history_listbox.pack(fill="both", expand=True, padx=6, pady=6)

        # right: stats and controls
        right = tk.Frame(middle, bd=1, relief="sunken", padx=10, pady=10, width=220)
        right.pack(side="right", fill="y")

        tk.Label(right, text="Match Controls", font=("Arial", 12, "bold")).pack(pady=(0,6))
        tk.Button(right, text="Reset Match", command=self.reset_match).pack(fill="x", pady=4)
        tk.Button(right, text="Show Stats", command=self.show_stats).pack(fill="x", pady=4)

        tk.Label(right, text="", height=1).pack()  # spacer

        tk.Label(right, text="Saved Stats", font=("Arial", 12, "bold")).pack(pady=(6,4))
        self.stats_text = tk.Text(right, height=8, width=28, state="disabled", bg="#f7f7f7")
        self.stats_text.pack(padx=4, pady=4)

        # instructions / key bindings
        bottom = tk.Frame(self.root, padx=10, pady=6)
        bottom.pack(fill="x")
        kb = "Keys: r=rock, p=paper, s=scissors, l=lizard, k=spock"
        tk.Label(bottom, text=kb, fg="gray").pack(side="left")

        self.update_stats_panel()
        self.start_new_match()

    # ---------------- Mode / Settings ----------------
    def update_wins_needed(self):
        self.wins_needed = self.best_of.get() // 2 + 1

    def update_ui_for_mode(self):
        mode = self.mode.get()
        if mode == "Classic":
            self.choices = CLASSIC_CHOICES.copy()
        else:
            self.choices = EXTENDED_CHOICES.copy()
        # enable/disable buttons
        for choice, btn in self.choice_buttons.items():
            if choice in self.choices:
                btn.config(state="normal")
            else:
                btn.config(state="disabled")

    # ---------------- Gameplay ----------------
    def start_new_match(self):
        self.player_score = 0
        self.comp_score = 0
        self.ties = 0
        self.round_number = 0
        self.player_history.clear()
        self.history.clear()
        self.history_listbox.delete(0, tk.END)
        self.update_wins_needed()
        self.update_scoreboard()
        self.result_var.set("Match started: good luck!")
        # ensure choices reflect current mode
        self.update_ui_for_mode()

    def reset_match(self):
        if messagebox.askyesno("Reset match", "Reset current match?"):
            self.start_new_match()

    def player_move(self, choice):
        # run a round
        comp = self.compute_computer_choice()
        self.round_number += 1
        self.player_history.append(choice)
        res = self.judge_round(choice, comp)
        if res == "win":
            self.player_score += 1
            self.flash_result("win")
            self.result_var.set(f"You win this round — {EMOJI[choice]} beats {EMOJI[comp]}")
        elif res == "lose":
            self.comp_score += 1
            self.flash_result("lose")
            self.result_var.set(f"You lose this round — {EMOJI[comp]} beats {EMOJI[choice]}")
        else:
            self.ties += 1
            self.flash_result("tie")
            self.result_var.set(f"Tie — both chose {EMOJI[choice]}")

        # update history
        hist_line = f"Round {self.round_number}: {self.player_name.get()} {EMOJI[choice]}  vs  CPU {EMOJI[comp]} -> {res.title()}"
        self.history.insert(0, hist_line)
        self.history_listbox.insert(0, hist_line)
        # update scoreboard
        self.update_scoreboard()
        # check end condition
        self.check_end_condition()

    def compute_computer_choice(self):
        choices = self.choices
        mode = self.difficulty.get()
        # Easy: random
        if mode == "Easy" or not self.player_history:
            return random.choice(choices)
        # Medium: 40% chance to counter player's last move, else random
        if mode == "Medium":
            last = self.player_history[-1]
            if random.random() < 0.4:
                beaters = [c for c in choices if last in WIN_MAP[c]]
                if beaters:
                    return random.choice(beaters)
            return random.choice(choices)
        # Hard: track player's frequencies and choose a beater of most frequent move(s)
        if mode == "Hard":
            freq = {}
            for p in self.player_history:
                if p in choices:
                    freq[p] = freq.get(p, 0) + 1
            if not freq:
                return random.choice(choices)
            # find most frequent player choices
            max_count = max(freq.values())
            most = [p for p, c in freq.items() if c == max_count]
            target = random.choice(most)
            beaters = [c for c in choices if target in WIN_MAP[c]]
            if beaters:
                return random.choice(beaters)
            return random.choice(choices)
        return random.choice(choices)

    def judge_round(self, player, comp):
        if player == comp:
            return "tie"
        # player wins if comp in WIN_MAP[player]
        if comp in WIN_MAP[player]:
            return "win"
        else:
            return "lose"

    def update_scoreboard(self):
        self.score_label.config(text=f"{self.player_name.get()} {self.player_score}  —  {self.comp_score} CPU")
        self.round_label.config(text=f"Round: {self.round_number}  (First to {self.wins_needed} wins)")
        self.update_stats_panel()

    def check_end_condition(self):
        if self.player_score >= self.wins_needed or self.comp_score >= self.wins_needed:
            # match finished
            if self.player_score > self.comp_score:
                winner = self.player_name.get()
                self.stats.setdefault("matches_won", 0)
                self.stats["matches_won"] += 1
                messagebox.showinfo("Match Over", f"Congratulations — {winner} won the match!")
            elif self.comp_score > self.player_score:
                winner = "CPU"
                self.stats.setdefault("matches_lost", 0)
                self.stats["matches_lost"] += 1
                messagebox.showinfo("Match Over", "CPU won the match. Better luck next time!")
            else:
                self.stats.setdefault("matches_tied", 0)
                self.stats["matches_tied"] += 1
                messagebox.showinfo("Match Over", "Match ended in a tie.")
            # update overall stats
            self.stats.setdefault("total_matches", 0)
            self.stats["total_matches"] += 1
            self.stats.setdefault("total_rounds", 0)
            self.stats["total_rounds"] += self.round_number
            # save stats
            self.save_stats()
            self.update_stats_panel()
            # disable buttons until restart if not auto-restart
            if self.auto_restart.get():
                self.start_new_match()
            else:
                for btn in self.choice_buttons.values():
                    btn.config(state="disabled")

    def flash_result(self, result):
        orig = self.result_label.cget("fg")
        if result == "win":
            color = "green"
        elif result == "lose":
            color = "red"
        else:
            color = "orange"
        self.result_label.config(fg=color)
        # revert after 500ms
        self.root.after(500, lambda: self.result_label.config(fg=orig))

    # ---------------- Stats panel ----------------
    def update_stats_panel(self):
        s = self.stats
        total_matches = s.get("total_matches", 0)
        won = s.get("matches_won", 0)
        lost = s.get("matches_lost", 0)
        tied = s.get("matches_tied", 0)
        total_rounds = s.get("total_rounds", 0)
        text = f"Total matches: {total_matches}\nMatches won: {won}\nMatches lost: {lost}\nMatches tied: {tied}\nTotal rounds played: {total_rounds}\n"
        self.stats_text.config(state="normal")
        self.stats_text.delete("1.0", tk.END)
        self.stats_text.insert(tk.END, text)
        self.stats_text.config(state="disabled")

    def show_stats(self):
        s = self.stats
        total_matches = s.get("total_matches", 0)
        won = s.get("matches_won", 0)
        lost = s.get("matches_lost", 0)
        tied = s.get("matches_tied", 0)
        total_rounds = s.get("total_rounds", 0)
        messagebox.showinfo("Saved Stats", f"Total matches: {total_matches}\nMatches won: {won}\nMatches lost: {lost}\nMatches tied: {tied}\nTotal rounds played: {total_rounds}")

    # ---------------- Keyboard ----------------
    def bind_keys(self):
        self.root.bind("r", lambda e: self.try_key("rock"))
        self.root.bind("p", lambda e: self.try_key("paper"))
        self.root.bind("s", lambda e: self.try_key("scissors"))
        self.root.bind("l", lambda e: self.try_key("lizard"))
        self.root.bind("k", lambda e: self.try_key("spock"))

    def try_key(self, choice):
        if choice in self.choices:
            self.player_move(choice)



if __name__== "_main_":
    root = tk.Tk()
    app = RPSApp(root)
    root.mainloop()