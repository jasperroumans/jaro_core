#!/usr/bin/env python3
"""Update a feedback log for the repository modules."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Iterable


def update_feedback(
    modules_dir: str | Path = Path(__file__).resolve().parent.parent / "modules",
    log_file: str | Path = Path(__file__).resolve().parent.parent / "data" / "log_002.json",
) -> Path:
    """Generate or append feedback entries for all modules.

    Parameters
    ----------
    modules_dir : str | Path
        Directory containing the modules to scan.
    log_file : str | Path
        Path to the feedback log file.
    """
    modules_dir = Path(modules_dir)
    log_file = Path(log_file)
    log_file.parent.mkdir(parents=True, exist_ok=True)

    if log_file.exists():
        with open(log_file, "r", encoding="utf-8") as f:
            entries = json.load(f)
    else:
        entries = []

    timestamp = datetime.utcnow().isoformat() + "Z"
    for module_path in modules_dir.glob("*.py"):
        entry = {
            "timestamp": timestamp,
            "memory_path": str(module_path),
            "advice": f"Review {module_path.stem} for potential improvements",
        }
        entries.append(entry)

    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)

    print(f"Feedback written to {log_file}")
    return log_file


def main() -> None:
    update_feedback()


if __name__ == "__main__":
    main()
