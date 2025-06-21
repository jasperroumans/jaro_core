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
        self.context_mode = "werk"
        self.previous_context = "werk"
        self._load_profile()

    def _load_profile(self):
        """Lees profieldata uit user_config.json."""
        if os.path.exists(USER_CONFIG_FILE):
            with open(USER_CONFIG_FILE, "r", encoding="utf-8") as f:
                try:
                    self.profile = json.load(f)
                    self.status = self.profile.get("status", STATUS_OFF)
                    self.context_mode = self.profile.get("context_mode", "werk")
                    self.previous_context = self.profile.get(
                        "previous_context", self.context_mode
                    )
                    if "context_mode" not in self.profile:
                        print(
                            "Waarschuwing: context_mode ontbreekt in configuratie. Gebruik 'werk'."
                        )
                        self.profile["context_mode"] = self.context_mode
                        self.profile["previous_context"] = self.previous_context
                        self._save_profile()
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

    def _save_profile(self):
        """Schrijf de huidige profieldata weg naar user_config.json."""
        self.profile["status"] = self.status
        self.profile["context_mode"] = self.context_mode
        self.profile["previous_context"] = self.previous_context
        with open(USER_CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(self.profile, f, indent=2, ensure_ascii=False)

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

    def _activate_modules(self):
        """Laad alle modules uit de modules-map en voer ze uit."""
        module_names = [
            "calendar_module",
            "email_module",
            "habit_tracker_module",
            "notities_module",
            "braindump_module",
            "highlight_module",
            "files_module",
        ]

        self.modules = []
        if MODULES_DIR not in sys.path:
            sys.path.insert(0, MODULES_DIR)

        for mod_name in module_names:
            try:
                module = importlib.import_module(mod_name)
                self.modules.append(module)
                self._log(f"Module {mod_name} geactiveerd")
            except ImportError:
                self._log(f"Module {mod_name} niet gevonden")
                continue

            run_fn = getattr(module, "run", None)
            if callable(run_fn):
                try:
                    self._log(
                        f"Voer {mod_name}.run() uit met context {self.context_mode}"
                    )
                    run_fn(context=self.context_mode)
                except Exception as exc:
                    self._log(f"Fout bij uitvoeren van {mod_name}: {exc}")
            else:
                self._log(f"run() ontbreekt in {mod_name}")

    def switch_context(self, new_context: str) -> None:
        """Wijzig de context en sla dit op."""
        if new_context not in {"werk", "privé"}:
            print("Ongeldige context. Kies 'werk' of 'privé'.")
            return
        if new_context == self.context_mode:
            print(f"Context is al '{new_context}'.")
            return
        self.previous_context = self.context_mode
        self.context_mode = new_context
        self._save_profile()
        self._log(f"Context gewijzigd naar {new_context}")
        print(f"Context gewijzigd naar {new_context}")

    def revert_context(self) -> None:
        """Zet de context terug naar de vorige."""
        if self.previous_context == self.context_mode:
            print("Geen vorige context beschikbaar om naar terug te keren.")
            return
        self.context_mode, self.previous_context = (
            self.previous_context,
            self.context_mode,
        )
        self._save_profile()
        self._log(f"Context teruggezet naar {self.context_mode}")
        print(f"Context teruggezet naar {self.context_mode}")

    def run(self):
        """Start de agent alleen wanneer status AAN is."""
        print(f"Actieve context: {self.context_mode}")
        if self.status != STATUS_ON:
            self._log("Agent staat niet op AAN en wordt gestopt")
            return
        self._log("Agent gestart")
        self._activate_modules()
        self._log("Agent klaar")

if __name__ == "__main__":
    agent = JaroLinkAgent()
    if len(sys.argv) >= 2:
        cmd = sys.argv[1]
        if cmd == "switch_context" and len(sys.argv) >= 3:
            agent.switch_context(sys.argv[2])
        elif cmd == "revert_context":
            agent.revert_context()
        else:
            print("Onbekend commando")
    else:
        agent.run()
