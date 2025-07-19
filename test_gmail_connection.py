from modules.email.gmail_client import GmailClient


def test_connection():
    gmail = GmailClient()
    if gmail.service:
        print("✅ Gmail verbinding succesvol!")
    else:
        print("❌ Gmail verbinding mislukt.")


if __name__ == "__main__":
    test_connection()
