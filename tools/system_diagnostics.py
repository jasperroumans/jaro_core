#!/usr/bin/env python3
"""Run basic integrity checks for configuration credentials."""

from __future__ import annotations

import os

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))

from utilities.config_loader import load_credentials


def run_diagnostics() -> None:
    """Print which credentials are missing, if any."""
    creds = load_credentials()
    missing = [key for key, value in creds.items() if not value]
    if missing:
        print(f"\u26A0\ufe0f Ontbrekende credentials: {missing}")
    else:
        print("\u2705 Alle credentials correct geladen.")


if __name__ == "__main__":
    run_diagnostics()
