import json
from unittest.mock import MagicMock

from core import gmail_client


def test_send_security_alert(tmp_path, monkeypatch):
    service_mock = MagicMock()
    users = service_mock.users.return_value
    messages = users.messages.return_value
    send = messages.send.return_value
    send.execute.return_value = {"id": "1"}

    class DummyClient:
        def __init__(self):
            self.service = service_mock

    monkeypatch.setattr(gmail_client, "GmailClient", DummyClient)
    log_file = tmp_path / "security.json"
    monkeypatch.setattr(gmail_client, "LOG_FILE", log_file)

    res = gmail_client.send_security_alert("subject", "msg")
    assert res == {"id": "1"}
    send.execute.assert_called_once()

    logged = json.loads(log_file.read_text())
    assert logged and logged[0]["event"] == "security_alert_sent"
