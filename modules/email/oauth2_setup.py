#!/usr/bin/env python3
"""Utility to obtain Gmail OAuth2 credentials."""

from __future__ import annotations
import os
from pathlib import Path
from typing import Iterable

from google_auth_oauthlib.flow import InstalledAppFlow

DEFAULT_SCOPES = [
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.readonly",
]


def run_gmail_oauth_flow(
    *,
    client_secret_file: str | None = None,
    credentials_path: str | None = None,
    scopes: Iterable[str] | None = None,
) -> None:
    """Run the OAuth2 flow and save credentials.

    Parameters
    ----------
    client_secret_file:
        Path to the Google client secret JSON file.
        Defaults to ``GOOGLE_CLIENT_SECRET_FILE`` or ``client_secret.json``.
    credentials_path:
        Location to store the generated credentials.
        Defaults to ``GOOGLE_CREDENTIALS_PATH`` or ``credentials.json``.
    scopes:
        Iterable of OAuth scopes to request. If not provided,
        sensible Gmail scopes are used.
    """

    secret = (
        client_secret_file
        or os.getenv("GOOGLE_CLIENT_SECRET_FILE")
        or "client_secret.json"
    )
    creds_file = (
        credentials_path
        or os.getenv("GOOGLE_CREDENTIALS_PATH")
        or "credentials.json"
    )
    scopes = list(scopes or DEFAULT_SCOPES)

    flow = InstalledAppFlow.from_client_secrets_file(secret, scopes)
    creds = flow.run_local_server(port=0)

    Path(creds_file).write_text(creds.to_json())
    print(f"\u2705 Credentials saved to {creds_file}")


__all__ = ["run_gmail_oauth_flow"]
