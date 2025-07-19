from __future__ import annotations

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from utilities.config_loader import load_google_credentials


class GmailClient:
    """Lightweight Gmail API client."""

    def __init__(self, creds_info: dict | None = None):
        try:
            creds_data = creds_info or load_google_credentials()
        except FileNotFoundError:
            self.service = None
        else:
            creds = Credentials.from_authorized_user_info(info=creds_data)
            self.service = build("gmail", "v1", credentials=creds)

    def send_email(self, to: str, subject: str, body: str) -> dict:
        """Send an email via the Gmail API."""
        if not self.service:
            raise RuntimeError("Gmail service not initialized")
        message = {"raw": body.encode("utf-8").decode("utf-8")}
        return (
            self.service.users()
            .messages()
            .send(userId="me", body=message)
            .execute()
        )


__all__ = ["GmailClient"]
