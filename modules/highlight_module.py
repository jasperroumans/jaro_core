"""Highlight module voor JARO-TOOTH.

Deze eenvoudige variant drukt enkel een bevestiging bij het starten
en kan later uitgebreid worden met echte functionaliteit.
"""


def start() -> None:
    """Start de highlight module."""
    print("\U0001F3A5 Highlight module gestart")


def run(context: str = "werk") -> None:
    """Simuleer highlight-functionaliteit op basis van de context."""
    print(f"[{context.upper()}] highlight_module gestart.")

    if context == "werk":
        print("\u25B6 Simuleer werkinhoud voor highlight_module...")
    elif context == "privé":
        print("\u25C0 Simuleer privé-inhoud voor highlight_module...")
    else:
        print("\u26A0 Onbekende context – toon alles.")

