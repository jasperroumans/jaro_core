#!/usr/bin/env python3
"""Sync jaro_core repository with GPT memory via codex_sync."""

from __future__ import annotations

from pathlib import Path

from codex_sync import sync_repo_with_gpt_memory


def main() -> None:
    base = Path(__file__).resolve().parent.parent
    sync_repo_with_gpt_memory(
        repo_path=str(base),
        memory_store="jasper_vonk_core",
        reference_format="snake_case",
        log_output=str(base / "data" / "log_001.json"),
        include_dirs=["modules", "core", "data", "tools", "interface"],
        export_formats=[".json", ".md", ".csv"],
    )


if __name__ == "__main__":
    main()
