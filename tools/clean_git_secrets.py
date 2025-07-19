#!/usr/bin/env python3
"""Detect and warn about sensitive files in the git repository."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from subprocess import run, PIPE

# Optional Gmail notification
try:
    from core.gmail_client import send_security_alert
except Exception:  # pragma: no cover - optional dependency
    send_security_alert = None

ROOT_DIR = Path(__file__).resolve().parent.parent
LOG_FILE = ROOT_DIR / "logs" / "security_log.json"

PATTERNS = [
    "credentials.json",
    "*.env",
    "*.pem",
    "*.key",
    "*.crt",
    "*token.json",
]


def _is_ignored(path: Path) -> bool:
    """Return True if path is ignored by git."""
    result = run(["git", "check-ignore", str(path)], stdout=PIPE, stderr=PIPE)
    return result.returncode == 0


def _get_staged_files() -> set[str]:
    """Return a set of staged file paths relative to the repo root."""
    result = run(
        ["git", "diff", "--cached", "--name-only"], stdout=PIPE, text=True, check=False
    )
    return set(line.strip() for line in result.stdout.splitlines() if line.strip())


def _append_log(entry: dict) -> None:
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    if LOG_FILE.exists():
        with LOG_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []
    data.append(entry)
    with LOG_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _notify_via_email() -> None:
    if not send_security_alert:
        return
    try:
        send_security_alert(
            subject="\U0001F6A8 Git Secret Detectie",
            message="Beveiligingsincident gedetecteerd – zie bijlage.",
            attachment_path=str(LOG_FILE),
        )
    except Exception as exc:  # pragma: no cover - best effort
        print(f"E-mailmelding mislukt: {exc}")


def scan_repository() -> None:
    staged = _get_staged_files()
    found = []
    for pattern in PATTERNS:
        found.extend(ROOT_DIR.rglob(pattern))

    processed = set()
    detections = []
    for path in found:
        if not path.is_file() or ".git" in path.parts:
            continue
        rel = path.relative_to(ROOT_DIR)
        if rel in processed:
            continue
        processed.add(rel)
        ignored = _is_ignored(path)
        staged_in_commit = str(rel) in staged
        if ignored and not staged_in_commit:
            continue

        status = "detected in commit" if staged_in_commit else "not ignored"
        action = f"git rm --cached {rel} && echo '{rel}' >> .gitignore"
        entry = {
            "timestamp": datetime.now().isoformat(),
            "file": str(rel),
            "status": status,
            "recommended_action": action,
        }
        detections.append(entry)
        _append_log(entry)
        print("\n\u26A0\ufe0f Verdacht bestand gevonden:", rel)
        print("  Status:", status)
        print("  Aanbevolen actie:", action)

    if detections:
        print(f"\nLog bijgewerkt: {LOG_FILE}")
        _notify_via_email()
    else:
        print("Geen verdachte bestanden gevonden.")


def main() -> None:
    scan_repository()


if __name__ == "__main__":
    main()
