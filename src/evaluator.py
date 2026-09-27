"""Safe arithmetic expression evaluation independent of the GUI."""

from __future__ import annotations

import ast
import operator
from decimal import Decimal, DecimalException, localcontext
from typing import Final


class CalculationError(ValueError):
    """Raised when an expression cannot be evaluated safely."""


_BINARY_OPERATORS: Final = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
}
_UNARY_OPERATORS: Final = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}
MAX_EXPRESSION_LENGTH: Final = 200
MAX_AST_NODES: Final = 100
MAX_ABS_EXPONENT: Final = 1000
DECIMAL_PRECISION: Final = 28


def evaluate_expression(expression: str) -> Decimal:
    """Evaluate an arithmetic expression using an allow-listed AST.

    Supported operations are ``+``, ``-``, ``*``, ``/``, ``**``, unary signs,
    decimal numbers, and parentheses. Names, calls, attributes, and containers
    are deliberately rejected.
    """
    cleaned = expression.strip()
    if not cleaned:
        raise CalculationError("Enter an expression first.")
    if len(cleaned) > MAX_EXPRESSION_LENGTH:
        raise CalculationError(
            f"Expression cannot exceed {MAX_EXPRESSION_LENGTH} characters."
        )

    try:
        tree = ast.parse(cleaned, mode="eval")
    except SyntaxError as exc:
        raise CalculationError("The expression is incomplete or invalid.") from exc

    if sum(1 for _ in ast.walk(tree)) > MAX_AST_NODES:
        raise CalculationError("The expression is too complex.")

    try:
        with localcontext() as context:
            context.prec = DECIMAL_PRECISION
            result = _evaluate_node(tree.body)
    except ZeroDivisionError as exc:
        raise CalculationError("Division by zero is not allowed.") from exc
    except (DecimalException, OverflowError, ValueError) as exc:
        raise CalculationError("The result is outside the supported range.") from exc

    if not result.is_finite():
        raise CalculationError("The result must be a finite number.")
    return result


def _evaluate_node(node: ast.AST) -> Decimal:
    if isinstance(node, ast.Constant):
        if isinstance(node.value, bool) or not isinstance(node.value, (int, float)):
            raise CalculationError("Only numbers are allowed.")
        return Decimal(str(node.value))

    if isinstance(node, ast.BinOp) and type(node.op) in _BINARY_OPERATORS:
        left = _evaluate_node(node.left)
        right = _evaluate_node(node.right)
        if isinstance(node.op, ast.Pow):
            if right != right.to_integral_value():
                raise CalculationError("The exponent must be an integer.")
            if abs(right) > MAX_ABS_EXPONENT:
                raise CalculationError(
                    f"Exponent magnitude cannot exceed {MAX_ABS_EXPONENT}."
                )
        return _BINARY_OPERATORS[type(node.op)](left, right)

    if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPERATORS:
        return _UNARY_OPERATORS[type(node.op)](_evaluate_node(node.operand))

    raise CalculationError("The expression contains an unsupported operation.")


def format_result(value: Decimal) -> str:
    """Return a compact, display-friendly Decimal representation."""
    if value == 0:
        return "0"
    normalized = value.normalize()
    adjusted = normalized.adjusted()
    if -12 <= adjusted <= 20:
        text = format(normalized, "f")
        return text.rstrip("0").rstrip(".") if "." in text else text
    return format(normalized, "E")
