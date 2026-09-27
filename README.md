# GUI Calculator

A lightweight desktop calculator written in Python with **Tkinter**. This
refactoring keeps the original GUI framework while separating calculation,
state, and presentation responsibilities so the project is safer, testable,
and easier to extend.

## Features

- Addition, subtraction, multiplication, division, powers, decimals, and parentheses
- Safe AST-based evaluation—no direct `eval()`
- Decimal arithmetic with 28-digit working precision
- Mouse and keyboard input
- Automatic implicit multiplication such as `2(` becoming `2*(`
- Session calculation history (`Ctrl+H`)
- Clear error messages and bounded expression complexity
- Unit tests for the evaluator and state rules
- Installable `src/` package with a command-line entry point

## Requirements

- Python 3.10 or newer
- Tkinter (included with standard Windows Python installations)

Verify Tkinter is available:

```powershell
python -m tkinter
```

## Quick start

### Windows PowerShell

```powershell
git clone <repository-url>
cd gui-calculator
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
gui-calculator
```

You can also run the package directly after installation:

```powershell
python -m gui_calculator
```

The root `main.py` remains as a compatibility launcher:

```powershell
python main.py
```

## Controls

| Action | Mouse | Keyboard |
|---|---|---|
| Calculate | `=` | `Enter` |
| Delete last character | `C` | `Backspace` |
| Clear expression | `CE` | `Escape` |
| Open history | — | `Ctrl+H` |
| Enter operators/parentheses | Buttons | `+ - * / ( )` |

`**` is the power operator. The parenthesis button decides whether to open or
close a group from the current expression context.

## Development

Install development tools:

```powershell
python -m pip install -e ".[dev]"
```

Run quality checks:

```powershell
pytest
ruff check .
ruff format --check .
mypy src
```

Apply formatting:

```powershell
ruff format .
```

## Project structure

```text
gui-calculator/
├── docs/
│   └── REFACTORING.md
├── src/gui_calculator/
│   ├── __init__.py
│   ├── __main__.py
│   ├── state.py
│   ├── app.py
│   └── evaluator.py
├── tests/
│   ├── test_evaluator.py
│   └── test_state.py
├── .gitignore
├── main.py
├── pyproject.toml
└── README.md
```

- `evaluator.py` owns safe parsing, arithmetic, limits, and result formatting.
- `state.py` owns editable state and input rules without requiring a GUI.
- `CalculatorApp` owns only Tkinter widgets, events, and user feedback.
- `main.py` preserves the original way of starting the application.

## Design notes

The evaluator parses expressions into a Python abstract syntax tree and only
allows explicit numeric and arithmetic node types. Calls, names, attributes,
collections, and all other syntax are rejected. Complexity and exponent limits
also prevent accidental resource-heavy expressions.

Tkinter's event loop is started only by `main()`, never inside a widget class.
That keeps construction predictable and makes modules safe to import in tests.

## Roadmap

Good next features, in suggested order:

1. Add memory buttons (`MC`, `MR`, `M+`, `M-`) to `CalculatorState`.
2. Save history to a small JSON file through a separate repository class.
3. Add selectable themes and persist the selected theme.
4. Add scientific functions through an explicit function allow-list.
5. Add clipboard actions and an accessible context menu.
6. Package a Windows executable with PyInstaller and automate releases in GitHub Actions.
7. Add GUI interaction tests after choosing a display-capable CI strategy.

## Contributing

Create a feature branch, add or update tests, run all checks, and submit a pull
request with a focused description. Keep calculation logic independent from
Tkinter wherever possible.
