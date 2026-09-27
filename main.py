"""Backward-compatible launcher for the GUI calculator."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from src.app import main

if __name__ == "__main__":
    main()
