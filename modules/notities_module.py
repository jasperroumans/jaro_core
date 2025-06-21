"""Notities module voor JARO-TOOTH.

Deze minimale implementatie wordt gebruikt om context switching te
demonstreren. Bij het starten toont de module enkel een bericht.
"""


def start() -> None:
    """Start de notities module."""
    print("\U0001F4D1 Notities module gestart")


def run(context: str = "werk") -> None:
    """Toon gesimuleerde notities afhankelijk van de context."""
    label = "WERK" if context == "werk" else "PRIVÉ" if context == "privé" else "ONBEKEND"
    print(f"[{label}] Notities gestart")

    if context == "werk":
        print("\u25B6 Simuleer werkinhoud voor notities_module...")
    elif context == "privé":
        print("\u25C0 Simuleer privé-inhoud voor notities_module...")
    else:
        print("\u26A0 Onbekende context – toon alles.")

