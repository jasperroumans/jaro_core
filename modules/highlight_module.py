"""Highlight module voor JARO-CORE.

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


def debug_output() -> None:
    """Print diagnostische informatie over de huidige context."""
    module_name = os.path.splitext(os.path.basename(__file__))[0]
    gebruiker = get_user_value("gebruikersnaam")
    context = get_user_value("active_context")
    toon = get_manifest_value(
        f"contextgedrag.gedrag_per_context.{context}.toon"
    )
    reflectie = is_user_enabled("reflectie")
    suggesties = is_allowed_to(
        "mag_jaro_proactief contextwaarschuwingen geven"
    )
    print(f"Module: {module_name}")
    print(f"Gebruiker: {gebruiker}")
    print(f"Actieve context: {context}")
    print(f"Toon van context: {toon}")
    print(f"Reflectie actief? {reflectie}")
    print(f"Mag JARO suggesties doen? {suggesties}")

