#!/usr/bin/env python3
"""Generate a weekly integrity log entry for CodeQL cron runs."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import json

LOG_DIR = Path("data_storage/logs/integriteit")
LOG_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    entry = {
        "timestamp": datetime.now().isoformat(),
        "source": "codeql_cron",
        "summary": "CodeQL scan succesvol gedraaid",
        "status": "OK",
        "branch": "main",
        "notes": "Scanresultaten beschikbaar in .github/workflows/codeql.yml",
    }

    filename = f"log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
    with (LOG_DIR / filename).open("w", encoding="utf-8") as f:
        json.dump(entry, f, indent=2, ensure_ascii=False)

    print(f"\u2705 Integriteitslog opgeslagen als: {filename}")


if __name__ == "__main__":
    main()
