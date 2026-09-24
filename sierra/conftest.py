"""Lets `pytest sierra/tests` work too (SIERRA_REF=1 pytest ... for reference solutions)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
