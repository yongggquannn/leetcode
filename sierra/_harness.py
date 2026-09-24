"""Test helpers: load() picks your code or the reference solution (SIERRA_REF=1)."""
import importlib
import os


def load(name: str):
    prefix = "solutions." if os.environ.get("SIERRA_REF") else ""
    return importlib.import_module(prefix + name)
