from src.state import CalculatorState


def test_implicit_multiplication_before_parenthesis() -> None:
    state = CalculatorState("2")
    state.append("(")
    assert state.expression == "2*("


def test_parenthesis_button_opens_then_closes() -> None:
    state = CalculatorState()
    state.toggle_parenthesis()
    state.append("2")
    state.toggle_parenthesis()
    assert state.expression == "(2)"


def test_calculation_is_added_to_history() -> None:
    state = CalculatorState("1+2")
    assert state.calculate() == "3"
    assert state.history == ["1+2 = 3"]
