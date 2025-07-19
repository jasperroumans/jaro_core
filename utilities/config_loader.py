import os
import json
from dotenv import load_dotenv


# Load environment variables from a .env file if present
load_dotenv()


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


def load_notion_config() -> dict:
    """Laad en valideer Notion configuratie uit omgevingsvariabelen."""
    notion_key = os.getenv("NOTION_KEY")
    if not notion_key:
        raise EnvironmentError("NOTION_KEY ontbreekt in .env of omgeving")

    database_ids = {
        key: value
        for key, value in os.environ.items()
        if key.startswith("NOTION_DATABASE_ID") and value
    }

    return {
        "notion_key": notion_key,
        "database_ids": database_ids,
    }
