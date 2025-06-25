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

from core.jaro_manifest import get_manifest_value, is_allowed_to
from core.user_config import get_user_value, is_user_enabled
from datetime import datetime
import os
import logging
from typing import Dict

__all__ = []

logger = logging.getLogger(__name__)

MANIFEST_DATA = get_manifest_value("contextual_info") or {}
VISION = get_manifest_value("jaro_vision") or {}
USER_PREFERENCES = get_user_value("personal_preferences") or {}
USER_ACTIVE = is_user_enabled("pc_on") if not os.environ.get("JARO_OVERRIDE") else True


def start() -> None:
    """Initialiseer de habit tracker module."""
    logger.debug("Habit tracker module start() called")
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

    logger.debug("Log habit %s status %s", gewoonte, status)
    print(f"{icon} Gewoonte '{gewoonte}' gemarkeerd als {status}")
    if opmerking:
        print(f"\U0001F4DD Opmerking: {opmerking}")
    print(log_entry)

    return log_entry


def run(context: str = "werk") -> None:
    """Simuleer habit-tracker-acties afhankelijk van de context."""
    if not USER_ACTIVE:
        logger.debug("Gebruiker niet actief; habit tracker wordt niet uitgevoerd")
        return

    context = context or USER_PREFERENCES.get("active_context", "werk")
    logger.debug("Habit tracker run() with context: %s", context)
    label = "WERK" if context == "werk" else "PRIVÉ" if context == "privé" else "ONBEKEND"
    print(f"[{label}] Habit Tracker gestart")

    if context == "werk":
        print("\u25B6 Simuleer werkinhoud voor habit_tracker_module...")
    elif context == "privé":
        print("\u25C0 Simuleer privé-inhoud voor habit_tracker_module...")
    else:
        print("\u26A0 Onbekende context – toon alles.")
