from unittest.mock import MagicMock

from modules import email_module


def test_send_email_oauth(monkeypatch):
    send_mock = MagicMock(return_value={"id": "456"})
    monkeypatch.setattr(email_module.gmail_module, "send_email", send_mock)

    result = email_module.send_email_oauth("to", "subject", "body")

    assert result == {"id": "456"}
    send_mock.assert_called_once_with("to", "subject", "body")

