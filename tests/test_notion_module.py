import os
import sys
import json
from pathlib import Path
from unittest.mock import MagicMock, patch

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from ai_modules import notion_module
from ai_modules.helpers import notion_helper


def test_read_notion_database(tmp_path, monkeypatch):
    monkeypatch.setenv("NOTION_KEY", "test-key")
    log_file = tmp_path / "log_002.json"
    monkeypatch.setattr(notion_module, "LOG_FILE", log_file)

    resp = MagicMock()
    resp.status_code = 200
    resp.json.return_value = {"results": [{"id": "123"}]}

    with patch("requests.post", return_value=resp) as post:
        data = notion_module.read_notion_database("dbid")
        assert data == [{"id": "123"}]
        post.assert_called_once()

    logged = json.loads(log_file.read_text())
    assert logged and logged[0]["note_ref"] == "note_001"


def test_update_notion_page(tmp_path, monkeypatch):
    monkeypatch.setenv("NOTION_KEY", "test-key")
    log_file = tmp_path / "log_002.json"
    monkeypatch.setattr(notion_module, "LOG_FILE", log_file)

    resp = MagicMock()
    resp.status_code = 200

    with patch("requests.patch", return_value=resp) as pat:
        success = notion_module.update_notion_page("pageid", {"Title": {}})
        assert success
        pat.assert_called_once()

    logged = json.loads(log_file.read_text())
    assert logged and logged[0]["note_ref"] == "note_001"


def test_create_page(monkeypatch):
    monkeypatch.setenv("NOTION_KEY", "test-key")
    resp = MagicMock()
    resp.status_code = 200
    resp.json.return_value = {"id": "456"}

    with patch("requests.post", return_value=resp) as post:
        result = notion_helper.create_page("dbid", {"Title": {"title": []}})
        assert result == {"id": "456"}
        post.assert_called_once()


def test_update_page(monkeypatch):
    monkeypatch.setenv("NOTION_KEY", "test-key")
    resp = MagicMock()
    resp.status_code = 200

    with patch("requests.patch", return_value=resp) as pat:
        ok = notion_helper.update_page("pid", {"Title": {}})
        assert ok is True
        pat.assert_called_once()


def test_fetch_all_tasks(monkeypatch):
    monkeypatch.setenv("NOTION_DATABASE_ID_TASKS", "tasksdb")
    monkeypatch.setenv("NOTION_KEY", "test-key")

    with patch(
        "ai_modules.helpers.notion_helper.query_database", return_value=[{"t": 1}]
    ) as qd:
        tasks = notion_helper.fetch_all_tasks()
        assert tasks == [{"t": 1}]
        qd.assert_called_once_with("tasksdb")
