#!/usr/bin/env python3
"""Generate a Markdown and JSON overview of the current memory log."""

from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime
from typing import Tuple


def generate_overview(
    log_path: str | Path = Path(__file__).resolve().parent.parent
    / "data" / "log_001.json",
    output_dir: str | Path = Path(__file__).resolve().parent.parent / "data",
) -> Tuple[Path, Path]:
    """Create overview files from a memory log.

    Parameters
    ----------
    log_path : str | Path
        Path to the JSON log describing the memory contents.
    output_dir : str | Path
        Directory where the overview files will be written.
    """
    log_path = Path(log_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(log_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    memory_name = data.get("memory_name", "unknown")
    generated = data.get("generated")
    files = data.get("files", [])

    overview_json = output_dir / "memory_overview.json"
    overview_md = output_dir / "memory_overview.md"

    json_data = {
        "memory_name": memory_name,
        "generated": generated,
        "file_count": len(files),
        "files": files,
    }
    with open(overview_json, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)

    with open(overview_md, "w", encoding="utf-8") as f:
        f.write(f"# Memory overview for {memory_name}\n")
        if generated:
            f.write(f"Generated: {generated}\n\n")
        f.write(f"Total files: {len(files)}\n\n")
        f.write("| Path | Memory Path |\n")
        f.write("| ---- | ----------- |\n")
        for item in files:
            f.write(f"| {item['path']} | {item['memory_path']} |\n")

    print(f"Overview generated at {overview_md} and {overview_json}")
    return overview_json, overview_md


def main() -> None:
    generate_overview()


if __name__ == "__main__":
    main()
