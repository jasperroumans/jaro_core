"""Bestandsmodule voor JARO-TOOTH.

Dit module biedt functionaliteit om bestanden in de datamap te sorteren op basis van hun extensie. De implementatie blijft bewust eenvoudig en uitbreidbaar zodat nieuwe bestandssoorten of acties later kunnen worden toegevoegd.

Functies
--------
start()
    Print een bevestiging dat de bestandsmodule is gestart.
auto_sort(doelmap="data")
    Sorteer bestanden naar submappen op basis van extensie.
"""

from core.jaro_manifest import get_manifest_value, is_allowed_to
from core.user_config import get_user_value, is_user_enabled
from datetime import datetime
import os
import logging
import json
import shutil

__all__ = []

logger = logging.getLogger(__name__)

MANIFEST_DATA = get_manifest_value("contextual_info") or {}
VISION = get_manifest_value("jaro_vision") or {}
USER_PREFERENCES = get_user_value("personal_preferences") or {}
USER_ACTIVE = is_user_enabled("pc_on") if not os.environ.get("JARO_OVERRIDE") else True

REPO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
LOG_FILE = os.path.join(REPO_DIR, "core", "activity_log.json")


def start() -> None:
    """Initialiseer de bestandsmodule."""
    logger.debug("Files module start() called")
    print("\U0001F5C2 Bestandsmodule gestart")


def _bepaal_submap(ext: str) -> str:
    """Geef de naam van de submap passend bij een extensie."""
    ext = ext.lower()
    mapping = {
        ".pdf": "pdf",
        ".jpg": "img",
        ".jpeg": "img",
        ".png": "img",
        ".docx": "docs",
        ".txt": "docs",
    }
    return mapping.get(ext, "other")


def _icon_for(ext: str) -> str:
    """Kies een icoon passend bij het bestandstype."""
    icons = {
        "pdf": "\U0001F4C4",  # 📄
        "img": "\U0001F5BC",  # 🖼
        "docs": "\U0001F4DD",  # 📝
        "other": "\U0001F4C1",  # 📁
    }
    return icons.get(_bepaal_submap(ext), "\U0001F4C1")


def _log_activiteit(boodschap: str) -> None:
    """Schrijf een logbericht naar ``activity_log.json``."""
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "message": boodschap,
    }
    logs = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                logs = json.load(f)
        except (json.JSONDecodeError, OSError):
            logs = []
    logs.append(entry)
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)


def auto_sort(doelmap: str = "data") -> None:
    """Sorteer bestanden in ``doelmap`` naar submappen op basis van extensie.

    Parameters
    ----------
    doelmap : str, optional
        De naam van de map binnen het project waarin gezocht wordt. Standaard
        ``"data"``.
    """
    repo_dir = REPO_DIR
    data_dir = os.path.join(repo_dir, doelmap)

    if not os.path.isdir(data_dir):
        print(f"Map '{data_dir}' bestaat niet")
        return

    moved = 0
    for naam in os.listdir(data_dir):
        pad = os.path.join(data_dir, naam)
        if os.path.isdir(pad):
            continue
        ext = os.path.splitext(naam)[1]
        submap = _bepaal_submap(ext)
        target_dir = os.path.join(data_dir, submap)
        os.makedirs(target_dir, exist_ok=True)
        dest = os.path.join(target_dir, naam)
        icoon = _icon_for(ext)
        try:
            shutil.move(pad, dest)
            status = "verplaatst"
            moved += 1
        except (OSError, shutil.Error) as exc:
            status = f"overgeslagen ({exc})"
        rel_dest = os.path.relpath(dest, repo_dir)
        print(f"{icoon} {naam} → {rel_dest} ({status})")

    boodschap = f"auto_sort uitgevoerd: {moved} bestanden verplaatst"
    logger.debug(boodschap)
    _log_activiteit(boodschap)
    print(boodschap)


def run(context: str = "werk") -> None:
    """Simuleer bestandsbeheer voor beide contexten."""
    if not USER_ACTIVE:
        logger.debug("Gebruiker niet actief; files wordt niet uitgevoerd")
        return

    context = context or USER_PREFERENCES.get("active_context", "werk")
    logger.debug("Files module run() with context: %s", context)
    label = "WERK" if context == "werk" else "PRIVÉ" if context == "privé" else "ONBEKEND"
    print(f"[{label}] Bestanden gestart")

    if context in {"werk", "privé"}:
        print("\u25B6 Simuleer bestandsbeheer in files_module...")
    else:
        print("\u26A0 Onbekende context – toon alles.")


