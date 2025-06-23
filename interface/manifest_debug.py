from __future__ import annotations

import json
import os
from datetime import datetime

import sys

# Zorg dat we de projectroot kunnen importeren
REPO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, REPO_DIR)

from core.jaro_manifest import load_manifest, get_manifest_value, is_allowed_to

LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs', 'manifest_log.json')


def _log_error(message: str) -> None:
    """Append an error entry to the manifest log."""
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "status": "error",
        "message": message,
    }
    logs = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        except (json.JSONDecodeError, OSError):
            logs = []
    logs.append(entry)
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)


def main() -> None:
    try:
        load_manifest()
        print("✅ Manifest geladen")
    except Exception as exc:  # pylint: disable=broad-except
        msg = f"Fout bij laden manifest: {exc}"
        print(msg)
        _log_error(msg)
        print(f"Logbestand: {os.path.abspath(LOG_FILE)}")
        return

    # Drie voorbeeldpaden uitlezen
    paths = [
        "rol_en_karakter.identiteit",
        "contextgedrag.gedrag_per_context.werk.toon",
        "autonomiebeleid.rol_van_jaro",
    ]
    for path in paths:
        value = get_manifest_value(path)
        print(f"{path}: {value}")

    allowed = is_allowed_to("mag_reflectievraag_stellen")
    print(f"Reflectievragen toegestaan: {allowed}")

    print(f"Logbestand: {os.path.abspath(LOG_FILE)}")


if __name__ == "__main__":
    main()
