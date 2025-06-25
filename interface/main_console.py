from __future__ import annotations

import os
import sys
import importlib
import random

# Zorg dat we de projectroot kunnen importeren
REPO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, REPO_DIR)

from interface.dashboard import print_dashboard
from core.jaro_manifest import get_manifest_value, reload_manifest
from core.user_config import reload_user_config
from modules import braindump_module, calendar_module


def _reflectiecheck() -> None:
    """Stel een willekeurige reflectievraag indien toegestaan."""
    allowed = get_manifest_value("zelfreflectie.mag_reflectievraag_stellen")
    if not allowed:
        print("Reflectievragen zijn niet toegestaan.")
        return
    vragen = get_manifest_value("zelfreflectie.voorbeeldvragen") or []
    if not vragen:
        print("Geen reflectievragen beschikbaar.")
        return
    vraag = random.choice(vragen)
    print(f"\U0001F914 {vraag}")
    input("Jouw antwoord: ")


def _debug_module() -> None:
    """Laat de gebruiker een module kiezen en toon debug_output."""
    modules_dir = os.path.join(REPO_DIR, "modules")
    modules = [f[:-3] for f in os.listdir(modules_dir) if f.endswith("_module.py")]
    if not modules:
        print("Geen modules gevonden.")
        return
    for i, mod in enumerate(modules, 1):
        print(f"{i}. {mod}")
    keuze = input("Kies een module: ").strip()
    mod_name = ""
    if keuze.isdigit() and 1 <= int(keuze) <= len(modules):
        mod_name = modules[int(keuze) - 1]
    else:
        mod_name = keuze
    try:
        module = importlib.import_module(mod_name)
    except ImportError:
        print("Module niet gevonden.")
        return
    debug_fn = getattr(module, "debug_output", None)
    if callable(debug_fn):
        debug_fn()
    else:
        print("debug_output() ontbreekt in deze module.")


def _reload_vision_profile() -> None:
    """Herlaad het manifest en de gebruikersconfig."""
    reload_manifest()
    reload_user_config()
    print("Visie en profiel opnieuw geladen.")
    print_dashboard()


def main() -> None:
    """Hoofdprogramma voor de eenvoudige CLI."""
    print_dashboard()
    while True:
        print("\nMaak een keuze:")
        print("1. \U0001F4D3 Braindump starten")
        print("2. \U0001F4C5 Calendar openen")
        print("3. \U0001FAA9 Reflectiecheck doen")
        print("4. \U0001F9E0 Toon debug-output (module kiezen)")
        print("5. \U0001F501 Herlaad visie en profiel")
        print("q. \u274C Stoppen")
        keuze = input(">> ").strip().lower()
        if keuze == "1":
            braindump_module.start()
        elif keuze == "2":
            calendar_module.dagstart()
        elif keuze == "3":
            _reflectiecheck()
        elif keuze == "4":
            _debug_module()
        elif keuze == "5":
            _reload_vision_profile()
        elif keuze == "q":
            break
        else:
            print("Ongeldige keuze.")


if __name__ == "__main__":
    main()
