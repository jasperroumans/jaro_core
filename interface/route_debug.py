import os
import sys

REPO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, REPO_DIR)

from core.module_router import get_active_modules


def main() -> None:
    """Print de modules die de router activeert."""
    mods = get_active_modules()
    print("Actieve modules volgens module_router:")
    for mod in mods:
        print(f"- {mod}")


if __name__ == "__main__":
    main()

