"""Braindump module voor JARO-TOOTH.

Wordt geactiveerd in de context 'privé'. De functionaliteit is
gesimuleerd via een simpel opstartbericht.
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


def start() -> None:
    """Initialiseer de braindump module."""
    logger.debug("Braindump module start() called")
    print("\U0001F4DD Braindump module gestart")


def run(context: str = "werk") -> None:
    """Simuleer braindump functionaliteit afhankelijk van de context."""
    if not USER_ACTIVE:
        logger.debug("Gebruiker niet actief; braindump wordt niet uitgevoerd")
        return

    context = context or USER_PREFERENCES.get("active_context", "werk")
    logger.debug("Braindump module run() with context: %s", context)
    label = "WERK" if context == "werk" else "PRIVÉ" if context == "privé" else "ONBEKEND"
    print(f"[{label}] Braindump gestart")

    if context == "werk":
        print("\u25B6 Simuleer werkinhoud voor braindump_module...")
    elif context == "privé":
        print("\u25C0 Simuleer privé-inhoud voor braindump_module...")
    else:
        print("\u26A0 Onbekende context – toon alles.")

