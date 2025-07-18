import os
import json


def load_credentials():
    credentials = {
        "openai_key": os.getenv("OPENAI_API_KEY"),
        "gmail_token": os.getenv("GMAIL_TOKEN"),
        "notion_key": os.getenv("NOTION_KEY"),
        "google_credentials_path": os.getenv("GOOGLE_CREDENTIALS_PATH")
    }
    return credentials


def load_google_credentials():
    path = os.getenv("GOOGLE_CREDENTIALS_PATH")
    if not path or not os.path.exists(path):
        raise FileNotFoundError("Google credentials JSON-bestand niet gevonden.")
    with open(path, 'r') as f:
        return json.load(f)
