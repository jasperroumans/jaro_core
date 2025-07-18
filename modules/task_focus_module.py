"""Task focus module for JARO-CORE.

Keeps track of daily focus or blockage in a CSV log with a simple CLI.
"""

from __future__ import annotations

import csv
from datetime import datetime, date
from pathlib import Path
import argparse
from typing import Tuple

__all__ = []


def log_focus(
    task: str,
    status: str = "FOCUS",
    note: str = "",
    log_dir: str | Path = Path(__file__).resolve().parent.parent / "data",
) -> Path:
    """Log a focus entry and return the created file path."""
    log_dir = Path(log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    log_file = log_dir / f"task_focus_log_{today}.csv"
    exists = log_file.exists()
    with open(log_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not exists:
            writer.writerow(["timestamp", "task", "status", "note"])
        writer.writerow([datetime.utcnow().isoformat(), task, status, note])
    print(f"Logged {task} with status {status}")
    return log_file


def show_log(log_dir: str | Path = Path(__file__).resolve().parent.parent / "data") -> None:
    """Print the current day's focus log."""
    log_dir = Path(log_dir)
    log_file = log_dir / f"task_focus_log_{date.today().isoformat()}.csv"
    if not log_file.exists():
        print("Geen logbestand gevonden")
        return
    with open(log_file, "r", encoding="utf-8") as f:
        print(f.read())


def main() -> None:
    parser = argparse.ArgumentParser(description="Task focus logger")
    parser.add_argument("task", nargs="?", help="Taak om te loggen")
    parser.add_argument("--status", default="FOCUS", choices=["FOCUS", "BLOCKADE"], help="Status van de taak")
    parser.add_argument("--note", default="", help="Optionele notitie")
    parser.add_argument("--show", action="store_true", help="Toon het logbestand")
    args = parser.parse_args()

    if args.show:
        show_log()
    elif args.task:
        log_focus(args.task, args.status, args.note)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

