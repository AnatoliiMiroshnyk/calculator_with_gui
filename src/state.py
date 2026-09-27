"""Calculator state and input-editing rules independent of Tkinter."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Final

from .evaluator import (
    MAX_EXPRESSION_LENGTH,
    CalculationError,
    evaluate_expression,
    format_result,
)

OPERATORS: Final = ("+", "-", "*", "/", "**")


@dataclass
class CalculatorState:
    """State and expression-editing rules, kept separate from widgets."""

    expression: str = ""
    history: list[str] = field(default_factory=list)

    def clear(self) -> None:
        self.expression = ""

    def backspace(self) -> None:
        self.expression = self.expression[:-1]

    def append(self, token: str) -> None:
        candidate = self._candidate_with(token)
        if len(candidate) > MAX_EXPRESSION_LENGTH:
            raise CalculationError(
                f"Expression cannot exceed {MAX_EXPRESSION_LENGTH} characters."
            )
        self.expression = candidate

    def toggle_parenthesis(self) -> None:
        opened = self.expression.count("(")
        closed = self.expression.count(")")
        last = self.expression[-1:] or None
        if opened > closed and last not in OPERATORS and last != "(":
            self.append(")")
        else:
            self.append("(")

    def calculate(self) -> str:
        original = self.expression
        result = format_result(evaluate_expression(original))
        self.history.append(f"{original} = {result}")
        self.expression = result
        return result

    def _candidate_with(self, token: str) -> str:
        current = self.expression
        last = current[-1:] or None

        if token.isdigit():
            prefix = "*" if last == ")" else ""
            return f"{current}{prefix}{token}"

        if token == ".":
            if last == ")":
                raise CalculationError("Add an operator before a decimal number.")
            number = _current_number(current)
            if "." in number:
                raise CalculationError("A number can contain only one decimal point.")
            prefix = "0" if not number else ""
            return f"{current}{prefix}."

        if token == "(":
            prefix = "*" if last and (last.isdigit() or last in ".)") else ""
            return f"{current}{prefix}("

        if token == ")":
            if current.count("(") <= current.count(")"):
                raise CalculationError("There is no open parenthesis to close.")
            if not last or last in "+-*/.(":
                raise CalculationError("Complete the value before closing parentheses.")
            return f"{current})"

        if token in OPERATORS:
            if not current:
                return "-" if token == "-" else current
            if last == "(":
                return f"{current}-" if token == "-" else current
            if last in "+-*/.":
                stripped = current.rstrip("+-*/.")
                if token == "-" and stripped != current:
                    return f"{current}-"
                return f"{stripped}{token}"
            return f"{current}{token}"

        raise CalculationError(f"Unsupported input: {token}")


def _current_number(expression: str) -> str:
    index = len(expression)
    while index > 0 and (
        expression[index - 1].isdigit() or expression[index - 1] == "."
    ):
        index -= 1
    return expression[index:]
