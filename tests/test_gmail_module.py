from unittest.mock import MagicMock, patch

from ai_modules import gmail_module


def test_get_gmail_service(monkeypatch):
    creds_info = {"token": "abc"}
    monkeypatch.setattr(
        gmail_module, "load_google_credentials", lambda: creds_info
    )

    creds_obj = MagicMock()
    with patch.object(gmail_module.Credentials, "from_authorized_user_info", return_value=creds_obj) as cred_patch:
        with patch.object(gmail_module, "build", return_value="service") as build_patch:
            service = gmail_module.get_gmail_service()
            assert service == "service"
            cred_patch.assert_called_once_with(info=creds_info)
            build_patch.assert_called_once_with("gmail", "v1", credentials=creds_obj)


def test_send_email(monkeypatch):
    service_mock = MagicMock()
    users = service_mock.users.return_value
    messages = users.messages.return_value
    send = messages.send.return_value
    send.execute.return_value = {"id": "123"}

    monkeypatch.setattr(gmail_module, "get_gmail_service", lambda: service_mock)

    result = gmail_module.send_email("to", "subject", "body")
    assert result == {"id": "123"}
    users.messages.assert_called_once()
    messages.send.assert_called_once()
    send.execute.assert_called_once()

