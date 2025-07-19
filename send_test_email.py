from modules.email.gmail_client import GmailClient

if __name__ == "__main__":
    gmail = GmailClient()
    gmail.send_email(
        to="jouw@gmail.com",
        subject="\U0001F9EA Test e-mail vanuit JARO_CORE",
        body="Als je dit leest, werkt je Gmail integratie via OAuth2!"
    )
