#!/usr/bin/env python3
"""CLI om JARO-CORE te starten met voorafgaande secrets-check."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
SECRETS_SCRIPT = ROOT_DIR / "tools" / "clean_git_secrets.py"


def _run_secrets_check() -> bool:
    """Run het clean_git_secrets script indien aanwezig.

    Returns
    -------
    bool
        True als het veilig is om door te gaan, False als de gebruiker annuleert.
    """
    if not SECRETS_SCRIPT.is_file():
        return True

    print("\U0001F50E Controleren op git secrets...")
    try:
        result = subprocess.run(
            [sys.executable, str(SECRETS_SCRIPT)],
            check=False,
            capture_output=True,
            text=True,
        )
    except Exception as exc:  # pragma: no cover - best effort
        print(f"Fout bij uitvoeren van secrets-check: {exc}")
        return True

    output = result.stdout.lower()
    if result.stderr:
        print(result.stderr)
    if output:
        print(output)

    if "secrets gevonden" in output or "verdacht bestand" in output:
        antwoord = input(
            "\u26A0\ufe0f Mogelijke secrets aangetroffen. Doorgaan? [y/N]: "
        ).strip().lower()
        return antwoord == "y"

    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Start JARO-CORE agent")
    parser.add_argument(
        "--skip-secrets-check",
        action="store_true",
        help="Sla controle op git secrets over",
    )
    args = parser.parse_args()

    if not args.skip_secrets_check:
        if not _run_secrets_check():
            print("Actie afgebroken door gebruiker.")
            return

    from core import jaro_link_agent

    agent = jaro_link_agent.JaroLinkAgent()
    agent.run()


if __name__ == "__main__":
    main()
