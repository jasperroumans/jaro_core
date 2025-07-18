from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import List, Dict

import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

NOTION_KEY = os.environ.get("NOTION_KEY", "")
HEADERS = {
    "Authorization": f"Bearer {NOTION_KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}

LOG_FILE = Path(__file__).resolve().parent.parent / "data" / "log_002.json"


def _append_log(action: str, info: Dict) -> None:
    """Append an entry to the feedback log under a note reference."""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    try:
        entries = json.loads(LOG_FILE.read_text()) if LOG_FILE.exists() else []
    except json.JSONDecodeError:
        entries = []
    note_id = f"note_{len(entries) + 1:03d}"
    entries.append({"note_ref": note_id, "action": action, "info": info})
    LOG_FILE.write_text(json.dumps(entries, indent=2, ensure_ascii=False))


def read_notion_database(database_id: str) -> List[dict]:
    """Return items from a Notion database."""
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    logger.debug("Reading Notion database %s", database_id)
    response = requests.post(url, headers=HEADERS)
    if response.status_code != 200:
        logger.error("Failed to read Notion database: %s", response.text)
        _append_log("read_failed", {"database_id": database_id, "status": response.status_code})
        return []
    results = response.json().get("results", [])
    _append_log("read_database", {"database_id": database_id, "count": len(results)})
    return results


def update_notion_page(page_id: str, properties: Dict) -> bool:
    """Update a Notion page with new properties."""
    url = f"https://api.notion.com/v1/pages/{page_id}"
    logger.debug("Updating Notion page %s", page_id)
    response = requests.patch(url, headers=HEADERS, json={"properties": properties})
    success = response.status_code == 200
    if not success:
        logger.error("Failed to update Notion page: %s", response.text)
    _append_log("update_page", {"page_id": page_id, "success": success})
    return success
