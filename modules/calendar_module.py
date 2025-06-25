"""Simple calendar module for the JARO-TOOTH agent.

Provides basic hooks that can be imported by ``jaro_link_agent``.

Functions
---------
start()
    Print a confirmation that the calendar module started.
dagstart()
    Print a message when starting the daily planning.

This design keeps the module lightweight and allows future
extension with reminders or agenda integrations.
"""

from core.jaro_manifest import get_manifest_value, is_allowed_to
from core.user_config import get_user_value, is_user_enabled
from datetime import datetime
import os
import logging

__all__ = []

logger = logging.getLogger(__name__)

MANIFEST_DATA = get_manifest_value("contextual_info") or {}
VISION = get_manifest_value("jaro_vision") or {}
USER_PREFERENCES = get_user_value("personal_preferences") or {}
USER_ACTIVE = is_user_enabled("pc_on") if not os.environ.get("JARO_OVERRIDE") else True


def start():
    """Initialize the calendar module."""
    logger.debug("Calendar module start() called")
    print("\U0001F4C5 Calendar module succesvol gestart")


def dagstart():
    """Trigger daily planning startup."""
    logger.debug("Calendar dagstart() called")
    print("\U0001F31E Dagplanning geladen: klaar om te starten")


def run(context: str = "werk") -> None:
    """Voer de kalenderfunctionaliteit contextbewust uit."""
    if not USER_ACTIVE:
        logger.debug("Gebruiker niet actief; calendar wordt niet uitgevoerd")
        return

    context = context or USER_PREFERENCES.get("active_context", "werk")
    logger.debug("Calendar module run() with context: %s", context)
    label = "WERK" if context == "werk" else "PRIVÉ" if context == "privé" else "ONBEKEND"
    print(f"[{label}] Calendar gestart")

    if context == "werk":
        print("\u25B6 Simuleer werkinhoud voor calendar_module...")
    elif context == "privé":
        print("\u25C0 Simuleer privé-inhoud voor calendar_module...")
    else:
        print("\u26A0 Onbekende context – toon alles.")
