"""Eenvoudige CLI voor het beheren van user_config.json."""

from __future__ import annotations

import json
import os
from datetime import datetime

BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "core")
USER_CONFIG_FILE = os.path.join(BASE_DIR, "user_config.json")
LOG_FILE = os.path.join(BASE_DIR, "activity_log.json")
MODULES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "modules")



def _log(message: str) -> None:
    """Sla een logregel op in activity_log.json."""
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "message": message,
    }
    logs = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                logs = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            pass
    logs.append(entry)
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)


def _load_config() -> dict:
    """Lees user_config.json en geef een standaardstructuur bij fouten."""
    if not os.path.exists(USER_CONFIG_FILE):
        print("Geen user_config.json gevonden; nieuwe configuratie wordt aangemaakt.")
        return {"status": "UIT", "actieve_modules": []}
    try:
        with open(USER_CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Fout: user_config.json bevat ongeldige JSON.")
        return {"status": "UIT", "actieve_modules": []}


def _save_config(config: dict) -> None:
    """Schrijf de configuratie terug naar het bestand."""
    config["laatst_bijgewerkt"] = datetime.utcnow().isoformat() + "Z"
    with open(USER_CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print("Configuratie opgeslagen.")


def _detect_modules() -> list[str]:
    """Zoek beschikbare *_module.py bestanden in de modules map."""
    mods = [f[:-3] for f in os.listdir(MODULES_DIR) if f.endswith("_module.py")]
    return mods


def _toon_status(config: dict) -> None:
    print(f"Status: {config.get('status', 'ONBEKEND')}")
    print("Actieve modules:")
    for mod in config.get("actieve_modules", []):
        print(f" - {mod}")


def _beheer_modules(config: dict) -> None:
    while True:
        beschikbare = sorted(set(_detect_modules()) | set(config.get("actieve_modules", [])))
        print("\nModules:")
        for i, mod in enumerate(beschikbare, 1):
            status = "AAN" if mod in config.get("actieve_modules", []) else "UIT"
            print(f"{i}. [{status}] {mod}")
        print("n. nieuwe module toevoegen")
        print("q. terug")
        keuze = input("Kies een optie: ").strip().lower()
        if keuze == "q":
            break
        if keuze == "n":
            naam = input("Naam van de nieuwe module: ").strip()
            if naam:
                if naam not in beschikbare:
                    beschikbare.append(naam)
                if naam not in config.get("actieve_modules", []):
                    config.setdefault("actieve_modules", []).append(naam)
                    _log(f"Module {naam} geactiveerd via config_ui")
            continue
        if keuze.isdigit():
            index = int(keuze) - 1
            if 0 <= index < len(beschikbare):
                mod = beschikbare[index]
                mods = config.setdefault("actieve_modules", [])
                if mod in mods:
                    mods.remove(mod)
                    _log(f"Module {mod} gedeactiveerd via config_ui")
                else:
                    mods.append(mod)
                    _log(f"Module {mod} geactiveerd via config_ui")
            else:
                print("Ongeldige keuze.")
        else:
            print("Ongeldige invoer.")


def _wijzig_status(config: dict) -> None:
    huidig = config.get("status", "UIT")
    print(f"Huidige status: {huidig}")
    nieuw = input("Nieuwe status (AAN/UIT/ACTIEF): ").strip().upper()
    if nieuw in {"AAN", "UIT", "ACTIEF"}:
        if nieuw != huidig:
            config["status"] = nieuw
            _log(f"Status gewijzigd naar {nieuw} via config_ui")
    else:
        print("Ongeldige status.")


def main() -> None:
    config = _load_config()
    while True:
        print("\nConfiguratiemenu")
        print("1. Toon huidige configuratie")
        print("2. Modules activeren/deactiveren")
        print("3. Status wijzigen")
        print("q. Afsluiten")
        keuze = input("Maak een keuze: ").strip().lower()
        if keuze == "1":
            _toon_status(config)
        elif keuze == "2":
            _beheer_modules(config)
        elif keuze == "3":
            _wijzig_status(config)
        elif keuze == "q":
            _save_config(config)
            break
        else:
            print("Ongeldige keuze.")


if __name__ == "__main__":
    main()
