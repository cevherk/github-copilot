"""
Calculator (GUI)
----------------
A simple calculator GUI app using Tkinter.

Features:
- Buttons for digits 0-9
- Buttons for +, -, ×, ÷
- Button for = and C (clear)
- Displays current input and result
"""

import tkinter as tk
from tkinter import ttk

class CalculatorApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Calculator")
        self.expression = ""
        self.input_var = tk.StringVar(value="0")

        container = ttk.Frame(self.root, padding=16)
        container.pack(fill=tk.BOTH, expand=True)

        input_entry = ttk.Entry(container, textvariable=self.input_var, font=("Helvetica", 18), justify="right", state="readonly")
        input_entry.pack(fill=tk.X, pady=(0, 12))

        btns = [
            ["7", "8", "9", "÷"],
            ["4", "5", "6", "×"],
            ["1", "2", "3", "-"],
            ["0", "C", "=", "+"]
        ]

        for row in btns:
            row_frame = ttk.Frame(container)
            row_frame.pack(fill=tk.X, pady=2)
            for btn in row:
                ttk.Button(row_frame, text=btn, command=lambda b=btn: self.on_button_click(b), width=5).pack(side=tk.LEFT, padx=2)

    def on_button_click(self, char):
        if char in "0123456789":
            if self.input_var.get() == "0" or self.expression.endswith("="):
                self.expression = char
            else:
                self.expression += char
            self.input_var.set(self.expression)
        elif char in "+-×÷":
            if self.expression and self.expression[-1] not in "+-×÷":
                self.expression += char
                self.input_var.set(self.expression)
        elif char == "C":
            self.expression = ""
            self.input_var.set("0")
        elif char == "=":
            try:
                expr = self.expression.replace("×", "*").replace("÷", "/")
                result = str(eval(expr))
                self.input_var.set(result)
                self.expression += "="
            except Exception:
                self.input_var.set("Error")
                self.expression = ""


def main():
    root = tk.Tk()
    app = CalculatorApp(root)
    root.minsize(300, 400)
    root.mainloop()


if __name__ == "__main__":
    main()
