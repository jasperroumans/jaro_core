"""Notities module voor JARO-TOOTH.

Deze minimale implementatie wordt gebruikt om context switching te
demonstreren. Bij het starten toont de module enkel een bericht.
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
    """Start de notities module."""
    logger.debug("Notities module start() called")
    print("\U0001F4D1 Notities module gestart")


def run(context: str = "werk") -> None:
    """Toon gesimuleerde notities afhankelijk van de context."""
    if not USER_ACTIVE:
        logger.debug("Gebruiker niet actief; notities wordt niet uitgevoerd")
        return

    context = context or USER_PREFERENCES.get("active_context", "werk")
    logger.debug("Notities module run() met context: %s", context)
    label = "WERK" if context == "werk" else "PRIVÉ" if context == "privé" else "ONBEKEND"
    print(f"[{label}] Notities gestart")

    if context == "werk":
        print("\u25B6 Simuleer werkinhoud voor notities_module...")
    elif context == "privé":
        print("\u25C0 Simuleer privé-inhoud voor notities_module...")
    else:
        print("\u26A0 Onbekende context – toon alles.")

