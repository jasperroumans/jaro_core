"""Security monitoring module for JARO-CORE.

This lightweight module logs security events and provides
an overview of enabled GitHub security features.
"""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime

__all__ = []

logger = logging.getLogger(__name__)

LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "security_log.json")


def start() -> None:
    """Initialize the security module."""
    logger.debug("Security module start() called")
    print("\U0001F6E1\uFE0F Security module gestart")


def log_event(message: str) -> None:
    """Append a security event to ``security_log.json``."""
    entry = {"timestamp": datetime.utcnow().isoformat() + "Z", "message": message}
    logs = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                logs = json.load(f)
        except (json.JSONDecodeError, OSError):
            logs = []
    logs.append(entry)
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)


def show_overview() -> None:
    """Print a summary of GitHub security features in use."""
    print(
        "Security features: Security Policy, CodeQL scanning, Private Vulnerability Reporting, Secret scanning."
    )
