"""Gmail integration via OAuth2."""

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from utilities.config_loader import load_google_credentials


def get_gmail_service():
    """Return an authorized Gmail service instance."""
    creds_data = load_google_credentials()
    creds = Credentials.from_authorized_user_info(info=creds_data)
    service = build("gmail", "v1", credentials=creds)
    return service


def send_email(to: str, subject: str, body: str):
    """Send an email via the Gmail API."""
    service = get_gmail_service()
    message = {
        "raw": body.encode("utf-8").decode("utf-8")
    }
    return (
        service.users()
        .messages()
        .send(userId="me", body=message)
        .execute()
    )

