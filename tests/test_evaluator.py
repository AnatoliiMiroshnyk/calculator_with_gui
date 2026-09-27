from decimal import Decimal

import pytest

from src.evaluator import (
    CalculationError,
    evaluate_expression,
    format_result,
)


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("2 + 3 * 4", Decimal("14")),
        ("(2 + 3) * 4", Decimal("20")),
        ("-2 ** 3", Decimal("-8")),
        ("0.1 + 0.2", Decimal("0.3")),
        ("2 ** 10", Decimal("1024")),
    ],
)
def test_evaluate_valid_expression(expression: str, expected: Decimal) -> None:
    assert evaluate_expression(expression) == expected


@pytest.mark.parametrize(
    "expression",
    ["", "1 / 0", "__import__('os')", "abs(-1)", "2 ** 1.5", "2 ** 1001"],
)
def test_rejects_invalid_or_unsafe_expression(expression: str) -> None:
    with pytest.raises(CalculationError):
        evaluate_expression(expression)


def test_format_result_removes_unnecessary_zeroes() -> None:
    assert format_result(Decimal("10.5000")) == "10.5"
