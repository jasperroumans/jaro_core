"""Module voor interactie met Notion API.

Synchroniseert taken, notities en events met opgegeven Notion database-ID's.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Dict, List

from ai_modules.helpers import notion_helper

logger = logging.getLogger(__name__)

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
    logger.debug("Reading Notion database %s", database_id)
    results = notion_helper.query_database(database_id)
    _append_log("read_database", {"database_id": database_id, "count": len(results)})
    return results


def update_notion_page(page_id: str, properties: Dict) -> bool:
    """Update a Notion page with new properties."""
    logger.debug("Updating Notion page %s", page_id)
    success = notion_helper.update_page(page_id, properties)
    if not success:
        logger.error("Failed to update Notion page %s", page_id)
    _append_log("update_page", {"page_id": page_id, "success": success})
    return success


def sync_databases(tasks_db: str, notes_db: str, events_db: str) -> Dict[str, List[dict]]:
    """Synchroniseer taken, notities en events met Notion."""
    return {
        "taken": read_notion_database(tasks_db),
        "notities": read_notion_database(notes_db),
        "events": read_notion_database(events_db),
    }
