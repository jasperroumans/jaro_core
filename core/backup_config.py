import os
import shutil
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(BASE_DIR)
USER_CONFIG_FILE = os.path.join(BASE_DIR, "user_config.json")
BACKUP_DIR = os.path.join(REPO_DIR, "backups")


def backup_user_config() -> None:
    """Maak een back-up van user_config.json."""
    if not os.path.exists(USER_CONFIG_FILE):
        print("Fout: user_config.json niet gevonden.")
        return
    try:
        os.makedirs(BACKUP_DIR, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"user_config_backup_{timestamp}.json"
        backup_path = os.path.join(BACKUP_DIR, backup_name)
        shutil.copy2(USER_CONFIG_FILE, backup_path)
        rel_path = os.path.relpath(backup_path, REPO_DIR)
        print(f"\U0001f5c2 Back-up opgeslagen: {rel_path}")
    except (OSError, PermissionError) as exc:
        print(f"Fout bij het maken van de back-up: {exc}")


if __name__ == "__main__":
    backup_user_config()
