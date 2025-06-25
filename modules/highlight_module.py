"""Highlight module voor JARO-TOOTH.

Deze eenvoudige variant drukt enkel een bevestiging bij het starten
en kan later uitgebreid worden met echte functionaliteit.
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
    """Start de highlight module."""
    logger.debug("Highlight module start() called")
    print("\U0001F3A5 Highlight module gestart")


def run(context: str = "werk") -> None:
    """Simuleer highlight-functionaliteit op basis van de context."""
    if not USER_ACTIVE:
        logger.debug("Gebruiker niet actief; highlight wordt niet uitgevoerd")
        return

    context = context or USER_PREFERENCES.get("active_context", "werk")
    logger.debug("Highlight module run() with context: %s", context)
    label = "WERK" if context == "werk" else "PRIVÉ" if context == "privé" else "ONBEKEND"
    print(f"[{label}] Highlight gestart")

    if context == "werk":
        print("\u25B6 Simuleer werkinhoud voor highlight_module...")
    elif context == "privé":
        print("\u25C0 Simuleer privé-inhoud voor highlight_module...")
    else:
        print("\u26A0 Onbekende context – toon alles.")

