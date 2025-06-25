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
REPO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
NOTES_DIR = os.path.join(REPO_DIR, "data", "notities")


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


def opslaan_notitie(tekst: str) -> str:
    """Sla een notitie op in ``NOTES_DIR`` met een timestamp."""
    os.makedirs(NOTES_DIR, exist_ok=True)
    timestamp = datetime.utcnow().isoformat().replace(":", "-").split(".")[0]
    bestand = os.path.join(NOTES_DIR, f"notitie_{timestamp}.txt")
    with open(bestand, "w", encoding="utf-8") as f:
        f.write(tekst)
    rel_pad = os.path.relpath(bestand, REPO_DIR)
    print(f"\U0001F4DD Notitie opgeslagen: {rel_pad}")
    if is_allowed_to("mag_jaro_proactief contextwaarschuwingen geven"):
        print("💡 Wil je dat ik hier een taak van maak?")
    return bestand


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

