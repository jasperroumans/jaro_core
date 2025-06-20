"""Eenvoudige dashboard CLI voor JARO-TOOTH."""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime


# Zorg dat we de projectroot kunnen importeren
REPO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, REPO_DIR)

from core.backup_config import backup_user_config
from core.rollback_module import restore_user_config


CORE_DIR = os.path.join(REPO_DIR, "core")
USER_CONFIG_FILE = os.path.join(CORE_DIR, "user_config.json")
LOG_FILE = os.path.join(CORE_DIR, "activity_log.json")


def _load_json(path: str) -> list | dict:
    """Lees een JSON-bestand en geef een lege structuur bij fouten."""
    if not os.path.exists(path):
        return [] if path == LOG_FILE else {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return [] if path == LOG_FILE else {}


def _format_timestamp(ts: str) -> str:
    """Converteer ISO-timestamp naar HH:MM formaat."""
    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return dt.strftime("%H:%M")
    except ValueError:
        return ts


def _show_dashboard() -> tuple[list[dict], dict]:
    """Print de dashboardinformatie en geef logs/config terug."""
    config = _load_json(USER_CONFIG_FILE) or {}
    logs = _load_json(LOG_FILE) or []

    status = config.get("status", "ONBEKEND")
    active = config.get("actieve_modules", [])

    last_line = "Geen logboek aanwezig"
    if logs:
        entry = logs[-1]
        time_str = _format_timestamp(entry.get("timestamp", ""))
        last_line = f"[{time_str}] {entry.get('message', '')}"

    print("\U0001F4E1 JARO-TOOTH DASHBOARD")
    print(f"Status: {status}")
    print(f"Actieve modules: {len(active)}")
    print(f"Laatste log: {last_line}")
    print("")
    print("[1] Toon logboek")
    print("[2] Maak backup")
    print("[3] Rollback uitvoeren")
    print("[q] Afsluiten")

    return logs, config


def _show_full_log(logs: list[dict]) -> None:
    if not logs:
        print("Geen logs gevonden.")
        return
    for entry in logs:
        time_str = _format_timestamp(entry.get("timestamp", ""))
        print(f"[{time_str}] {entry.get('message', '')}")


def main() -> None:
    while True:
        logs, _ = _show_dashboard()
        keuze = input("Maak een keuze: ").strip().lower()
        if keuze == "1":
            _show_full_log(logs)
            input("Druk op Enter om verder te gaan...")
        elif keuze == "2":
            backup_user_config()
            input("Druk op Enter om verder te gaan...")
        elif keuze == "3":
            restore_user_config()
            input("Druk op Enter om verder te gaan...")
        elif keuze == "q":
            break
        else:
            print("Ongeldige keuze.")


if __name__ == "__main__":
    main()

