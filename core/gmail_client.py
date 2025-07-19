from __future__ import annotations

import base64
import json
from datetime import datetime
from email.message import EmailMessage
from pathlib import Path

from modules.email.gmail_client import GmailClient

ROOT_DIR = Path(__file__).resolve().parent.parent
LOG_FILE = ROOT_DIR / "logs" / "security_log.json"


def _append_log(entry: dict) -> None:
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    if LOG_FILE.exists():
        try:
            data = json.loads(LOG_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            data = []
    else:
        data = []
    data.append(entry)
    LOG_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False))


def send_security_alert(subject: str, message: str, attachment_path: str | None = None) -> dict:
    """Send a security alert email via Gmail OAuth2 and log the event."""
    gmail = GmailClient()
    if not gmail.service:
        raise RuntimeError("Gmail service not initialized")

    email_msg = EmailMessage()
    email_msg["To"] = "me"
    email_msg["Subject"] = subject
    email_msg.set_content(message)

    if attachment_path:
        path = Path(attachment_path)
        if path.is_file():
            email_msg.add_attachment(
                path.read_bytes(),
                maintype="application",
                subtype="octet-stream",
                filename=path.name,
            )

    encoded = base64.urlsafe_b64encode(email_msg.as_bytes()).decode()
    response = (
        gmail.service.users()
        .messages()
        .send(userId="me", body={"raw": encoded})
        .execute()
    )

    _append_log(
        {
            "timestamp": datetime.now().isoformat(),
            "event": "security_alert_sent",
            "subject": subject,
            "attachment": str(attachment_path) if attachment_path else None,
        }
    )
    return response


__all__ = ["send_security_alert"]
