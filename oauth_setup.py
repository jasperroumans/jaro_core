import os
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def setup_gmail_oauth() -> None:
    """Run OAuth2 flow using credentials.json and save the token."""
    creds_path = os.getenv("GOOGLE_CREDENTIALS_PATH")
    if not creds_path or not os.path.exists(creds_path):
        raise FileNotFoundError("❌ credentials.json niet gevonden.")

    flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
    creds = flow.run_local_server(port=0)

    with open("token_gmail.json", "w") as token:
        token.write(creds.to_json())

    print("✅ Gmail OAuth2 gekoppeld en token opgeslagen als token_gmail.json.")


if __name__ == "__main__":
    setup_gmail_oauth()
