"""Tkinter presentation layer for the calculator."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox
from typing import Final

from .evaluator import CalculationError
from .state import OPERATORS, CalculatorState

WINDOW_TITLE: Final = "Calculator"
BUTTON_ROWS: Final = (
    ("7", "8", "9", "+", "C"),
    ("4", "5", "6", "-", "CE"),
    ("1", "2", "3", "*", "**"),
    ("()", "0", ".", "/", "="),
)


class CalculatorApp(tk.Frame):
    """Main calculator window using the existing Tkinter framework."""

    def __init__(self, master: tk.Tk) -> None:
        super().__init__(master)
        self.master = master
        self.state = CalculatorState()
        self.display_value = tk.StringVar(value="0")
        self.status_value = tk.StringVar(value="Ready")
        self._build_window()
        self._build_widgets()
        self._bind_keyboard()

    def _build_window(self) -> None:
        self.master.title(WINDOW_TITLE)
        self.master.geometry("420x520")
        self.master.minsize(360, 440)
        self.master.configure(bg="#1f1f1f")

    def _build_widgets(self) -> None:
        self.pack(expand=True, fill="both")
        self.configure(bg="#1f1f1f")

        display = tk.Label(
            self,
            textvariable=self.display_value,
            font=("Segoe UI", 30),
            anchor="se",
            justify="right",
            bg="#595954",
            fg="white",
            padx=12,
            pady=12,
        )
        display.grid(row=0, column=0, columnspan=5, sticky="nsew")

        for row_index, row in enumerate(BUTTON_ROWS, start=1):
            for column_index, label in enumerate(row):
                button = tk.Button(
                    self,
                    text=label,
                    font=("Segoe UI", 18),
                    borderwidth=0,
                    relief="flat",
                    bg=self._button_color(label),
                    fg="white",
                    activebackground="#565656",
                    activeforeground="white",
                    command=lambda value=label: self._on_button(value),
                )
                button.grid(
                    row=row_index,
                    column=column_index,
                    sticky="nsew",
                    padx=1,
                    pady=1,
                )

        status = tk.Label(
            self,
            textvariable=self.status_value,
            anchor="w",
            bg="#1f1f1f",
            fg="#c8c8c8",
            padx=8,
        )
        status.grid(row=5, column=0, columnspan=5, sticky="ew")

        for column in range(5):
            self.grid_columnconfigure(column, weight=1, uniform="buttons")
        self.grid_rowconfigure(0, weight=2)
        for row in range(1, 5):
            self.grid_rowconfigure(row, weight=1, uniform="buttons")

    @staticmethod
    def _button_color(label: str) -> str:
        if label == "=":
            return "#0067c0"
        if label in OPERATORS or label == "()":
            return "#3d3d3d"
        if label in {"C", "CE"}:
            return "#7a3131"
        return "#2e2e2e"

    def _bind_keyboard(self) -> None:
        self.master.bind("<Key>", self._on_key)
        self.master.bind("<Return>", lambda _event: self._calculate())
        self.master.bind("<KP_Enter>", lambda _event: self._calculate())
        self.master.bind("<BackSpace>", lambda _event: self._backspace())
        self.master.bind("<Escape>", lambda _event: self._clear())
        self.master.bind("<Control-h>", lambda _event: self._show_history())

    def _on_key(self, event: tk.Event) -> None:
        if event.keysym in {"Return", "KP_Enter", "BackSpace", "Escape"}:
            return
        if event.char in "0123456789.+-*/()":
            self._append(event.char)

    def _on_button(self, label: str) -> None:
        actions = {
            "=": self._calculate,
            "C": self._backspace,
            "CE": self._clear,
            "()": self._toggle_parenthesis,
        }
        action = actions.get(label)
        action() if action else self._append(label)

    def _append(self, token: str) -> None:
        try:
            self.state.append(token)
            self._refresh("Editing")
        except CalculationError as exc:
            self._show_error(exc)

    def _toggle_parenthesis(self) -> None:
        try:
            self.state.toggle_parenthesis()
            self._refresh("Editing")
        except CalculationError as exc:
            self._show_error(exc)

    def _backspace(self) -> None:
        self.state.backspace()
        self._refresh("Last character removed")

    def _clear(self) -> None:
        self.state.clear()
        self._refresh("Cleared")

    def _calculate(self) -> None:
        try:
            self.state.calculate()
            self._refresh("Calculated — Ctrl+H opens history")
        except CalculationError as exc:
            self._show_error(exc)

    def _refresh(self, status: str) -> None:
        self.display_value.set(self.state.expression or "0")
        self.status_value.set(status)

    def _show_error(self, error: CalculationError) -> None:
        self.status_value.set(str(error))
        messagebox.showerror("Calculation error", str(error), parent=self.master)

    def _show_history(self) -> None:
        window = tk.Toplevel(self.master)
        window.title("Calculation history")
        window.geometry("440x300")
        text = tk.Text(window, font=("Consolas", 12), wrap="word", padx=10, pady=10)
        text.pack(expand=True, fill="both")
        history = "\n".join(reversed(self.state.history)) or "No calculations yet."
        text.insert("1.0", history)
        text.configure(state="disabled")


def main() -> None:
    """Create the Tk root and start the event loop."""
    root = tk.Tk()
    CalculatorApp(root)
    root.mainloop()
