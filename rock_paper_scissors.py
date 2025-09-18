"""
Rock–Paper–Scissors (GUI)
-------------------------
Single-player GUI game versus the computer, built with Tkinter.

Features:
- Buttons for Rock / Paper / Scissors
- Shows computer's move and the round result
- Detailed scoreboard with wins, losses, ties, and statistics
- Running score for Player and Computer
- Reset Score button and Quit button
- Keyboard shortcuts: R, P, S to play; Q to quit; Cmd+R to reset

How to run (macOS):
	python3 rock_paper_scissors.py

Note: Tkinter usually ships with Python on macOS. If it is missing, install a
Python build that includes Tk (e.g., from python.org) or add Tcl/Tk via Homebrew.
"""

import random
import sys

try:
	import tkinter as tk
	from tkinter import ttk, messagebox
except Exception as exc:
	print("Tkinter could not be imported. Install/enable Tkinter and try again.")
	print(f"Details: {exc}")
	sys.exit(1)


CHOICES = ("rock", "paper", "scissors")


def decide_winner(player: str, computer: str) -> str:
	"""Return 'win', 'lose', or 'tie' from player's perspective.
	Rules:
	  - rock beats scissors
	  - paper beats rock
	  - scissors beats paper
	"""
	p = player.lower()
	c = computer.lower()
	if p == c:
		return "tie"
	wins_over = {
		"rock": "scissors",
		"paper": "rock",
		"scissors": "paper",
	}
	return "win" if wins_over.get(p) == c else "lose"


class RPSApp:
	def __init__(self, root: tk.Tk):
		self.root = root
		self.root.title("Rock–Paper–Scissors")

		# Use a modern ttk theme if available
		try:
			style = ttk.Style()
			# Prefer 'clam' on macOS for consistent button rendering
			if "clam" in style.theme_names():
				style.theme_use("clam")
		except Exception:
			pass

		# Game state
		self.player_score = 0
		self.computer_score = 0
		self.ties = 0
		self.total_rounds = 0

		# Tk variables for binding to labels
		self.score_var = tk.StringVar(value=self._format_score())
		self.detailed_stats_var = tk.StringVar(value=self._format_detailed_stats())
		self.result_var = tk.StringVar(value="Make your move!")
		self.computer_var = tk.StringVar(value="Computer hasn't played yet.")

		# Build UI
		container = ttk.Frame(self.root, padding=16)
		container.pack(fill=tk.BOTH, expand=True)

		title = ttk.Label(container, text="Rock–Paper–Scissors", font=("Helvetica", 16, "bold"))
		title.pack(pady=(0, 8))

		# Main score display
		score_lbl = ttk.Label(container, textvariable=self.score_var, font=("Helvetica", 12, "bold"))
		score_lbl.pack(pady=(0, 4))

		# Detailed statistics
		stats_lbl = ttk.Label(container, textvariable=self.detailed_stats_var, font=("Helvetica", 10))
		stats_lbl.pack(pady=(0, 12))

		# Buttons row
		btn_row = ttk.Frame(container)
		btn_row.pack(pady=(0, 12))

		self._make_choice_button(btn_row, "Rock", "rock").pack(side=tk.LEFT, padx=6)
		self._make_choice_button(btn_row, "Paper", "paper").pack(side=tk.LEFT, padx=6)
		self._make_choice_button(btn_row, "Scissors", "scissors").pack(side=tk.LEFT, padx=6)

		result_lbl = ttk.Label(container, textvariable=self.result_var, font=("Helvetica", 13, "bold"))
		result_lbl.pack(pady=(4, 6))

		comp_lbl = ttk.Label(container, textvariable=self.computer_var)
		comp_lbl.pack(pady=(0, 8))

		# Control buttons
		ctrl_row = ttk.Frame(container)
		ctrl_row.pack(pady=(4, 0))

		ttk.Button(ctrl_row, text="Reset Score", command=self.reset_score).pack(side=tk.LEFT, padx=6)
		ttk.Button(ctrl_row, text="Quit", command=self.on_quit).pack(side=tk.LEFT, padx=6)

		# Keyboard shortcuts
		self.root.bind("<KeyPress-r>", lambda e: self.play("rock"))
		self.root.bind("<KeyPress-p>", lambda e: self.play("paper"))
		self.root.bind("<KeyPress-s>", lambda e: self.play("scissors"))
		self.root.bind("<KeyPress-q>", lambda e: self.on_quit())

		# Cmd+R (macOS) to reset
		self.root.bind("<Command-r>", lambda e: self.reset_score())

	def _make_choice_button(self, parent, text: str, choice: str) -> ttk.Button:
		return ttk.Button(parent, text=text, command=lambda: self.play(choice))

	def _format_score(self) -> str:
		return f"Player: {self.player_score}   Computer: {self.computer_score}"

	def _format_detailed_stats(self) -> str:
		"""Format detailed statistics including ties and percentages."""
		if self.total_rounds == 0:
			return "Wins: 0 | Losses: 0 | Ties: 0 | Total: 0 | Win Rate: 0.0%"
		
		win_rate = (self.player_score / self.total_rounds) * 100
		return (f"Wins: {self.player_score} | Losses: {self.computer_score} | "
				f"Ties: {self.ties} | Total: {self.total_rounds} | Win Rate: {win_rate:.1f}%")

	def play(self, player_choice: str):
		if player_choice not in CHOICES:
			messagebox.showerror("Invalid move", f"'{player_choice}' is not a valid choice.")
			return

		computer_choice = random.choice(CHOICES)
		outcome = decide_winner(player_choice, computer_choice)

		# Update round counter
		self.total_rounds += 1

		if outcome == "win":
			self.player_score += 1
			self.result_var.set("You win this round! 🎉")
		elif outcome == "lose":
			self.computer_score += 1
			self.result_var.set("You lose this round. 😢")
		else:
			self.ties += 1
			self.result_var.set("It's a tie. 😐")

		self.computer_var.set(f"Computer chose: {computer_choice.title()}")
		self.score_var.set(self._format_score())
		self.detailed_stats_var.set(self._format_detailed_stats())

	def reset_score(self):
		self.player_score = 0
		self.computer_score = 0
		self.ties = 0
		self.total_rounds = 0
		self.score_var.set(self._format_score())
		self.detailed_stats_var.set(self._format_detailed_stats())
		self.result_var.set("Scores reset. Make your move!")
		self.computer_var.set("Computer hasn't played yet.")

	def on_quit(self):
		self.root.quit()


def main(argv=None):
	root = tk.Tk()
	app = RPSApp(root)
	root.minsize(400, 250)
	root.mainloop()
	return 0


if __name__ == "__main__":
	raise SystemExit(main(sys.argv[1:]))