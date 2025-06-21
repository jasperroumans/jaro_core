from __future__ import annotations

import importlib
import os
import sys
import logging
from contextlib import redirect_stdout
from io import StringIO

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODULE_DIR = os.path.join(REPO_DIR, "modules")
LOG_DIR = os.path.join(REPO_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "context_simulation.log")

os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)


def simulate() -> None:
    """Doorloop alle modules en voer run(context) uit."""
    modules = [m[:-3] for m in os.listdir(MODULE_DIR) if m.endswith("_module.py")]
    sys.path.insert(0, MODULE_DIR)
    contexts = ["werk", "privé"]

    for mod_name in modules:
        try:
            module = importlib.import_module(mod_name)
        except Exception as exc:
            msg = f"Kon module {mod_name} niet laden: {exc}"
            print(msg)
            logging.error(msg)
            continue

        run_fn = getattr(module, "run", None)
        for ctx in contexts:
            header = f"----- {mod_name} ({ctx}) -----"
            print(header)
            logging.info(header)
            if callable(run_fn):
                buf = StringIO()
                with redirect_stdout(buf):
                    try:
                        run_fn(context=ctx)
                    except Exception as exc:
                        print(f"Fout bij uitvoeren van {mod_name}: {exc}")
                output = buf.getvalue()
                buf.close()
                print(output, end="")
                for line in output.rstrip().splitlines():
                    logging.info(line)
            else:
                warn = f"Waarschuwing: run() ontbreekt in {mod_name}"
                print(warn)
                logging.warning(warn)

    logging.info("Simulatie afgerond")


if __name__ == "__main__":
    simulate()
