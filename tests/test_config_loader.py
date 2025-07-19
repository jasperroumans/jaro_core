import os
import sys
import pytest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from utilities import config_loader


def test_load_notion_config(monkeypatch):
    monkeypatch.setenv("NOTION_KEY", "key123")
    monkeypatch.setenv("NOTION_DATABASE_ID_TASKS", "db1")

    cfg = config_loader.load_notion_config()
    assert cfg["notion_key"] == "key123"
    assert cfg["database_ids"]["NOTION_DATABASE_ID_TASKS"] == "db1"


def test_load_notion_config_missing_key(monkeypatch):
    monkeypatch.delenv("NOTION_KEY", raising=False)
    with pytest.raises(EnvironmentError):
        config_loader.load_notion_config()
