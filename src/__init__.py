"""A small, safe, and testable Tkinter calculator."""

from .evaluator import CalculationError, evaluate_expression

__all__ = ["CalculationError", "evaluate_expression"]
__version__ = "2.0.0"
