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


def start():
    """Initialize the calendar module."""
    print("\U0001F4C5 Calendar module succesvol gestart")


def dagstart():
    """Trigger daily planning startup."""
    print("\U0001F31E Dagplanning geladen: klaar om te starten")


def run(context: str = "werk") -> None:
    """Voer de kalenderfunctionaliteit contextbewust uit."""
    label = "WERK" if context == "werk" else "PRIVÉ" if context == "privé" else "ONBEKEND"
    print(f"[{label}] Calendar gestart")

    if context == "werk":
        print("\u25B6 Simuleer werkinhoud voor calendar_module...")
    elif context == "privé":
        print("\u25C0 Simuleer privé-inhoud voor calendar_module...")
    else:
        print("\u26A0 Onbekende context – toon alles.")
