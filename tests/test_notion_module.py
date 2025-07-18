import os
import sys
import json
from pathlib import Path
from unittest.mock import MagicMock, patch

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from ai_modules import notion_module


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
