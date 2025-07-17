"""Simulatiescript voor het wisselen van contexten in JARO-CORE.

Het script demonstreert de nieuwe CLI-commando's ``switch_context`` en
``revert_context`` en toont welke modules per context worden gestart.
"""

from __future__ import annotations

import os
import subprocess
import sys
import json


REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AGENT_PATH = os.path.join(REPO_DIR, "core", "jaro_link_agent.py")
CONFIG_PATH = os.path.join(REPO_DIR, "core", "user_config.json")


def _run_agent(args: list[str] | None = None) -> None:
    cmd = [sys.executable, AGENT_PATH]
    if args:
        cmd.extend(args)
    print("$", " ".join(cmd))
    subprocess.run(cmd, check=False)


def main() -> None:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)
    orig_status = config.get("status", "UIT")
    config["status"] = "AAN"
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    print("Start agent met standaardcontext:\n")
    _run_agent([])

    print("\nSchakel naar context 'privé':\n")
    _run_agent(["switch_context", "privé"])

    print("\nStart agent opnieuw:\n")
    _run_agent([])

    print("\nRollback naar vorige context:\n")
    _run_agent(["revert_context"])

    print("\nStart agent nogmaals:\n")
    _run_agent([])

    config["status"] = orig_status
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()

