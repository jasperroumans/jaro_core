"""Rollback module voor JARO-CORE.

Dit script herstelt een eerdere versie van ``user_config.json`` door een
back-up uit de map ``backups`` te kiezen. Het kan zowel zelfstandig
worden uitgevoerd als geïmporteerd in een CLI.
"""

from __future__ import annotations

import os
import shutil
from typing import List

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(BASE_DIR)
USER_CONFIG_FILE = os.path.join(BASE_DIR, "user_config.json")
BACKUP_DIR = os.path.join(REPO_DIR, "backups")


def _list_backups() -> List[str]:
    """Geef alle beschikbare back-upbestanden terug."""
    if not os.path.isdir(BACKUP_DIR):
        return []

    files = [
        f
        for f in os.listdir(BACKUP_DIR)
        if f.startswith("user_config_backup_") and f.endswith(".json")
    ]
    files.sort(reverse=True)
    return files


def restore_user_config() -> None:
    """Laat de gebruiker een back-up kiezen en herstel deze."""
    backups = _list_backups()

    if not backups:
        print("Geen back-ups gevonden.")
        return

    print("\U0001F4DC Beschikbare back-ups:")
    for i, name in enumerate(backups, 1):
        print(f"{i}. {name}")

    keuze = input(f"Kies een back-up om te herstellen (1-{len(backups)}): ").strip()
    if not keuze.isdigit():
        print("Ongeldige keuze.")
        return

    index = int(keuze) - 1
    if index < 0 or index >= len(backups):
        print("Ongeldige keuze.")
        return

    selected = backups[index]
    src = os.path.join(BACKUP_DIR, selected)

    try:
        shutil.copy2(src, USER_CONFIG_FILE)
    except (OSError, PermissionError) as exc:
        print(f"Fout bij het herstellen: {exc}")
        return

    timestamp = selected.replace("user_config_backup_", "").replace(".json", "")
    print(
        f"\u267B\ufe0f Herstel voltooid: user_config.json vervangen door back-up {timestamp}"
    )


if __name__ == "__main__":
    restore_user_config()
