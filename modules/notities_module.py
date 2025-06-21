"""Notities module voor JARO-TOOTH.

Deze minimale implementatie wordt gebruikt om context switching te
demonstreren. Bij het starten toont de module enkel een bericht.
"""


def start() -> None:
    """Start de notities module."""
    print("\U0001F4D1 Notities module gestart")


def run(context: str = "werk") -> None:
    """Toon notities gefilterd op basis van de huidige context."""
    start()
    print(f"\U0001F4D1 Filter notities voor context: {context}")

