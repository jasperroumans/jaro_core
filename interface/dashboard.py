from __future__ import annotations

import os
import json
from datetime import datetime

REPO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
CONFIG_PATH = os.path.join(REPO_DIR, "config", "user_config.json")


def _load_config() -> dict:
    """Lees ``user_config.json`` uit de config map."""
    if not os.path.exists(CONFIG_PATH):
        return {}
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}


def print_dashboard() -> None:
    """Toon kerninformatie uit ``user_config.json`` op het scherm."""
    data = _load_config()
    gebruiker = data.get("gebruikersnaam", "onbekend")
    context = data.get("active_context", "onbekend")
    toon = data.get("toon", "onbekend")
    modules = ", ".join(data.get("modules", [])) or "geen"
    reflectie = "AAN" if data.get("reflectie") else "UIT"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("\U0001F4BB JARO-TOOTH DASHBOARD")
    print(f"Gebruiker: {gebruiker}")
    print(f"Context: {context}")
    print(f"Toon: {toon}")
    print(f"Actieve modules: {modules}")
    print(f"Reflectie: {reflectie}")
    print(f"Timestamp: {timestamp}")


if __name__ == "__main__":
    print_dashboard()
