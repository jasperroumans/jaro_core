"""
Bevat Notion API-functies zoals paginacreatie, updaten en ophalen.
Maakt gebruik van NOTION_KEY in .env.
"""
from __future__ import annotations

import logging
import os
from typing import Dict, List, Optional

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


def query_database(database_id: str) -> List[dict]:
    """Ophalen van items uit een Notion-database."""
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    resp = requests.post(url, headers=HEADERS)
    if resp.status_code != 200:
        logger.error("Failed to query database %s: %s", database_id, resp.text)
        return []
    return resp.json().get("results", [])


def create_page(database_id: str, properties: Dict) -> Optional[dict]:
    """Maak een pagina aan in een Notion-database."""
    url = "https://api.notion.com/v1/pages"
    payload = {"parent": {"database_id": database_id}, "properties": properties}
    resp = requests.post(url, headers=HEADERS, json=payload)
    if resp.status_code != 200:
        logger.error("Failed to create page: %s", resp.text)
        return None
    return resp.json()


def update_page(page_id: str, properties: Dict) -> bool:
    """Werk een Notion-pagina bij."""
    url = f"https://api.notion.com/v1/pages/{page_id}"
    resp = requests.patch(url, headers=HEADERS, json={"properties": properties})
    return resp.status_code == 200


def get_page(page_id: str) -> Optional[dict]:
    """Haal één Notion-pagina op."""
    url = f"https://api.notion.com/v1/pages/{page_id}"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code != 200:
        logger.error("Failed to fetch page: %s", resp.text)
        return None
    return resp.json()
