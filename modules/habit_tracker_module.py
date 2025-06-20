"""Habit tracker module voor de JARO-TOOTH agent.

Dit module legt de basis voor het registreren van gewoontes, het analyseren
van gedrag en toekomstige integraties met agenda's of herinneringen.

Functies
--------
start()
    Bevestigt dat de habit tracker gestart is.
log_habit(gewoonte, status, opmerking="")
    Registreer een gewoonte met status en optionele opmerking.

Deze opzet houdt de module lichtgewicht en laat uitbreidingen toe zoals
habit-analyse, feedback op inconsistent gedrag en integratie met
kalender- of reminderfunctionaliteit.
"""

from datetime import datetime
from typing import Dict


def start() -> None:
    """Initialiseer de habit tracker module."""
    print("\U0001F4DD Habit tracker module gestart")


def log_habit(gewoonte: str, status: str, opmerking: str = "") -> Dict[str, str]:
    """Log een gewoonte-actie.

    Parameters
    ----------
    gewoonte : str
        De naam van de activiteit.
    status : str
        "AFGEMAAKT", "OVERGESLAGEN" of "GEPLAND".
    opmerking : str, optional
        Een toelichting of gevoel bij deze actie.
    """
    icons = {
        "AFGEMAAKT": "\u2705",  # ✅
        "OVERGESLAGEN": "\u274C",  # ❌
        "GEPLAND": "\U0001F553",  # 🕓
    }
    icon = icons.get(status.upper(), "")

    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "gewoonte": gewoonte,
        "status": status,
        "opmerking": opmerking,
    }

    print(f"{icon} Gewoonte '{gewoonte}' gemarkeerd als {status}")
    if opmerking:
        print(f"\U0001F4DD Opmerking: {opmerking}")
    print(log_entry)

    return log_entry
