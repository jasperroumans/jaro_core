"""Recovery tracker module for JARO-CORE.

This module keeps a recovery plan with entries such as NA sessions,
sponsor meetings and martial arts practice.
It generates a JSON summary and an Excel habit sheet for the current day.
"""

from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime, date
from typing import Tuple

from openpyxl import Workbook

__all__ = []


def run(output_dir: str | Path = Path(__file__).resolve().parent.parent / "data") -> Tuple[Path, Path]:
    """Create recovery tracking files in ``output_dir``.

    Parameters
    ----------
    output_dir : str | Path
        Directory where the tracker files will be stored.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()

    tracker_json = output_dir / f"tracker_recovery_{today}.json"
    habit_xlsx = output_dir / f"habit_sheet_{today}.xlsx"

    data = {
        "date": today,
        "entries": [
            {"type": "NA", "note": "Meeting"},
            {"type": "sponsor", "note": "Call"},
            {"type": "martial_arts", "note": "Training"},
            {"type": "groep", "note": "Session"},
        ],
    }

    with open(tracker_json, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    wb = Workbook()
    ws = wb.active
    ws.append(["date", "activity", "note"])
    for entry in data["entries"]:
        ws.append([today, entry["type"], entry["note"]])
    wb.save(habit_xlsx)

    print(f"Recovery tracker saved to {tracker_json} and {habit_xlsx}")
    return tracker_json, habit_xlsx

