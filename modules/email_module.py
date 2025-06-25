"""Simple email module for JARO-TOOTH.

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
