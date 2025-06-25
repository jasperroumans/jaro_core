import json
import os
from datetime import datetime

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
MANIFEST_PATH = os.path.join(BASE_DIR, "config", "jaro_visie.json")
LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "manifest_log.json")

MANIFEST_DATA = None


def _log(status: str, message: str) -> None:
    """Schrijf een logbericht weg naar ``logs/manifest_log.json``."""
    os.makedirs(LOG_DIR, exist_ok=True)
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "status": status,
        "message": message,
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
        json.dump(logs, f, indent=2, ensure_ascii=False)


def load_manifest() -> dict:
    """Laad het manifestbestand in en valideer verplichte topniveaus."""
    global MANIFEST_DATA
    if not os.path.exists(MANIFEST_PATH):
        _log("error", "config/jaro_visie.json bestaat niet")
        raise FileNotFoundError("config/jaro_visie.json bestaat niet")
    try:
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as exc:
        _log("error", f"JSON fout: {exc}")
        raise

    required = [
        "rol_en_karakter",
        "autonomiebeleid",
        "contextgedrag",
        "herstelgedrag",
        "relatiebescherming",
        "zelfreflectie",
        "stress_gedrag",
        "dempmogelijkheden",
        "activatie",
    ]
    missing = [k for k in required if k not in data]
    if missing:
        _log("error", f"Ontbrekende sleutels: {', '.join(missing)}")
    else:
        _log("ok", "Manifest succesvol geladen")
    MANIFEST_DATA = data
    return data


def get_manifest_value(path: str):
    """Haal een waarde op uit het manifest via een puntgescheiden pad."""
    global MANIFEST_DATA
    if MANIFEST_DATA is None:
        MANIFEST_DATA = load_manifest()
    parts = path.split(".") if path else []
    value = MANIFEST_DATA
    for part in parts:
        if isinstance(value, dict) and part in value:
            value = value[part]
        else:
            return None
    return value


def _search_key(data, key: str) -> bool:
    """Doorzoek recursief naar ``key`` met waarde ``True``."""
    if isinstance(data, dict):
        for k, v in data.items():
            if k == key and v is True:
                return True
            if _search_key(v, key):
                return True
    elif isinstance(data, list):
        for item in data:
            if _search_key(item, key):
                return True
    return False


def is_allowed_to(key: str) -> bool:
    """Controleer of een booleansleutel ergens in het manifest ``True`` is."""
    global MANIFEST_DATA
    if MANIFEST_DATA is None:
        MANIFEST_DATA = load_manifest()
    return _search_key(MANIFEST_DATA, key)


def save_manifest(data: dict) -> None:
    """Sla een bijgewerkte manifestdict op."""
    global MANIFEST_DATA
    os.makedirs(os.path.dirname(MANIFEST_PATH), exist_ok=True)
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    MANIFEST_DATA = data
    _log("ok", "Manifest bijgewerkt")


def reload_manifest() -> None:
    """Herlaad het manifest van schijf."""
    global MANIFEST_DATA
    MANIFEST_DATA = load_manifest()
