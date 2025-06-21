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


def start():
    """Initialize the email module."""
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
    print(f"\u2709\ufe0f Simulatie: E-mail verzonden naar {ontvanger} met onderwerp: '{onderwerp}'")
    print(f"Inhoud:\n{bericht}")


def run(context: str = "werk") -> None:
    """Start de e-mailfunctionaliteit en toon de juiste inbox."""
    start()
    if context == "werk":
        print("\U0001F4E5 Werkinbox geopend")
    else:
        print("\U0001F4EC Privéinbox geopend")
