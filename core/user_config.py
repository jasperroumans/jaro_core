import json
import os
from datetime import datetime

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
CONFIG_PATH = os.path.join(BASE_DIR, "config", "user_config.json")
LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "user_config_log.json")

USER_CONFIG_DATA = None


def _log(status: str, message: str) -> None:
    """Schrijf een logbericht weg naar ``logs/user_config_log.json``."""
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


def load_user_config() -> dict:
    """Laad de gebruikersconfiguratie en valideer verplichte velden."""
    global USER_CONFIG_DATA
    if not os.path.exists(CONFIG_PATH):
        _log("error", "config/user_config.json bestaat niet")
        USER_CONFIG_DATA = {}
        return {}
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as exc:
        _log("error", f"JSON fout: {exc}")
        USER_CONFIG_DATA = {}
        return {}

    required = ["gebruikersnaam", "taal", "modules"]
    missing = [k for k in required if k not in data]
    if missing:
        _log("error", f"Ontbrekende velden: {', '.join(missing)}")
    else:
        _log("ok", "User config succesvol geladen")
    USER_CONFIG_DATA = data
    return data


def get_user_value(path: str):
    """Haal een waarde op uit de gebruikersconfig via een puntpad."""
    global USER_CONFIG_DATA
    if USER_CONFIG_DATA is None:
        USER_CONFIG_DATA = load_user_config()
    parts = path.split(".") if path else []
    value = USER_CONFIG_DATA
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


def is_user_enabled(key: str) -> bool:
    """Controleer of een booleansleutel ergens in de config ``True`` is."""
    global USER_CONFIG_DATA
    if USER_CONFIG_DATA is None:
        USER_CONFIG_DATA = load_user_config()
    return _search_key(USER_CONFIG_DATA, key)


def reload_user_config() -> dict:
    """Herlaad de configuratie van schijf en ververs de globale versie."""
    global USER_CONFIG_DATA
    USER_CONFIG_DATA = None
    return load_user_config()


def profile_info() -> None:
    """Print kerninformatie uit de gebruikersconfig."""
    global USER_CONFIG_DATA
    if USER_CONFIG_DATA is None:
        USER_CONFIG_DATA = load_user_config()
    data = USER_CONFIG_DATA
    naam = data.get("gebruikersnaam", "onbekend")
    taal = data.get("taal", "onbekend")
    toon = data.get("toon", "onbekend")
    context = data.get("active_context", "onbekend")
    modules = ", ".join(data.get("modules", []))
    print(f"Gebruiker: {naam}")
    print(f"Taal: {taal}")
    print(f"Toon: {toon}")
    print(f"Actieve context: {context}")
    print(f"Modules: {modules}")
