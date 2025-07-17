"""Simple email module for JARO-CORE.

Provides basic communication hooks that can be imported by ``jaro_link_agent``.

Functions
---------
start()
    Print a confirmation that the email module started.
send_email(ontvanger, onderwerp, bericht)
    Simulate sending an email by printing the contents.

This design keeps the module lightweight and easily extensible with real
email-sending capabilities via SMTP or an API.
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
    """Initialize the email module."""
    logger.debug("Email module start() called")
    print("\U0001F4E7 Email module gestart")


def send_email(ontvanger: str, onderwerp: str, bericht: str) -> None:
    """Simulate sending an email.

    Parameters
    ----------
    ontvanger : str
        Recipient address.
    onderwerp : str
        Subject line.
    bericht : str
        Body of the email.
    """
    logger.debug("send_email called to %s with subject %s", ontvanger, onderwerp)
    print(f"\u2709\ufe0f Simulatie: E-mail verzonden naar {ontvanger} met onderwerp: '{onderwerp}'")
    print(f"Inhoud:\n{bericht}")


def run(context: str = "werk") -> None:
    """Simuleer contextbewuste e-mailafhandeling."""
    if not USER_ACTIVE:
        logger.debug("Gebruiker niet actief; email wordt niet uitgevoerd")
        return

    context = context or USER_PREFERENCES.get("active_context", "werk")
    logger.debug("Email module run() with context: %s", context)
    label = "WERK" if context == "werk" else "PRIVÉ" if context == "privé" else "ONBEKEND"
    print(f"[{label}] Email gestart")

    if context == "werk":
        print("\u25B6 Simuleer werkinhoud voor email_module...")
    elif context == "privé":
        print("\u25C0 Simuleer privé-inhoud voor email_module...")
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
