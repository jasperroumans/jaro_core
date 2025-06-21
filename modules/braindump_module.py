"""Braindump module voor JARO-TOOTH.

Wordt geactiveerd in de context 'privé'. De functionaliteit is
gesimuleerd via een simpel opstartbericht.
"""


def start() -> None:
    """Initialiseer de braindump module."""
    print("\U0001F4DD Braindump module gestart")


def run(context: str = "werk") -> None:
    """Simuleer braindump functionaliteit afhankelijk van de context."""
    label = "WERK" if context == "werk" else "PRIVÉ" if context == "privé" else "ONBEKEND"
    print(f"[{label}] Braindump gestart")

    if context == "werk":
        print("\u25B6 Simuleer werkinhoud voor braindump_module...")
    elif context == "privé":
        print("\u25C0 Simuleer privé-inhoud voor braindump_module...")
    else:
        print("\u26A0 Onbekende context – toon alles.")

