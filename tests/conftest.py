# wiki/apv-v2/tests/conftest.py
"""Shared test fixtures for APV V2 tools."""
import sys
from pathlib import Path

# Ensure tools/ is importable
sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

FIXTURES_DIR = Path(__file__).parent / "fixtures"
