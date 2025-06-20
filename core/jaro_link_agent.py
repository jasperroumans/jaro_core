import json
import importlib
import os
import sys
from datetime import datetime

# Constants for status labels in Dutch
STATUS_ON = "AAN"
STATUS_OFF = "UIT"
STATUS_ACTIVE = "ACTIEF"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USER_CONFIG_FILE = os.path.join(BASE_DIR, "user_config.json")
LOG_FILE = os.path.join(BASE_DIR, "activity_log.json")
MODULES_DIR = os.path.join(BASE_DIR, "..", "modules")

class JaroLinkAgent:
    """Kernscript van de AI-agent."""

    def __init__(self):
        self.status = STATUS_OFF
        self.profile = {}
        self.modules = []
        self._load_profile()

    def _load_profile(self):
        """Lees profieldata uit user_config.json."""
        if os.path.exists(USER_CONFIG_FILE):
            with open(USER_CONFIG_FILE, "r", encoding="utf-8") as f:
                try:
                    self.profile = json.load(f)
                    self.status = self.profile.get("status", STATUS_OFF)
                except json.JSONDecodeError:
                    self._log("Fout bij het lezen van user_config.json")
        else:
            self._log("Geen user_config.json gevonden")

    def _log(self, message):
        """Schrijf een logbericht naar activity_log.json."""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "message": message,
        }
        logs = []
        if os.path.exists(LOG_FILE):
            try:
                with open(LOG_FILE, "r", encoding="utf-8") as f:
                    logs = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        logs.append(entry)
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(logs, f, indent=2)

    def register_module(self, module_name):
        """Registreer een module vanuit de modules-directory."""
        if MODULES_DIR not in sys.path:
            sys.path.insert(0, MODULES_DIR)
        try:
            module = importlib.import_module(module_name)
            self.modules.append(module)
            self._log(f"Module {module_name} geregistreerd")
        except ImportError:
            self._log(f"Kon module {module_name} niet importeren")

    def start_modules(self):
        """Start alle geregistreerde modules indien mogelijk."""
        for module in self.modules:
            start_fn = getattr(module, "start", None)
            if callable(start_fn):
                try:
                    start_fn()
                    self._log(f"Module {module.__name__} gestart")
                except Exception as exc:
                    self._log(f"Fout bij starten van {module.__name__}: {exc}")

    def run(self):
        """Start de agent alleen wanneer status AAN is."""
        if self.status != STATUS_ON:
            self._log("Agent staat niet op AAN en wordt gestopt")
            return
        self._log("Agent gestart")
        for mod_name in self.profile.get("modules", []):
            self.register_module(mod_name)
        self.start_modules()
        self._log("Agent klaar")

if __name__ == "__main__":
    agent = JaroLinkAgent()
    agent.run()
