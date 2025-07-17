#!/usr/bin/python3
"""Index repository files for potential memory sync."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_FILE = REPO_ROOT / "data" / "log_001.json"
FILE_TYPES = {".py", ".json", ".md", ".csv", ".xlsx", ".ics"}

SYNC_MAP = {
    "config": "config_profiles",
    "core": "core_logic",
    "data": "data_storage",
    "interface": "interface_layer",
    "modules": "ai_modules",
    "tests": "test_routines",
    "tools": "utilities",
}


def index_repo() -> List[Dict[str, str]]:
    entries: List[Dict[str, str]] = []
    for path in REPO_ROOT.rglob("*"):
        if any(part.startswith(".") for part in path.parts):
            continue
        if path.is_file() and path.suffix.lower() in FILE_TYPES:
            rel = path.relative_to(REPO_ROOT)
            parts = rel.parts
            if parts:
                top = parts[0]
                memory_dir = SYNC_MAP.get(top)
                if memory_dir:
                    memory_path = Path(memory_dir).joinpath(*parts[1:])
                else:
                    memory_path = rel
            else:
                memory_path = rel
            entries.append({"path": str(rel), "memory_path": str(memory_path)})
    return entries


def main() -> None:
    data = {
        "memory_name": "jasper_vonk_core",
        "generated": datetime.utcnow().isoformat() + "Z",
        "files": index_repo(),
    }
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Index saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
