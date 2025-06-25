#!/usr/bin/env python3
"""Create distribution ZIP for jaro_tooth project."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
import zipfile

EXCLUDE_DIRS = {'.git', '__pycache__'}
EXCLUDE_FILES = {'.DS_Store'}


def project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def zip_directory(ziph: zipfile.ZipFile, directory: Path, base: Path) -> None:
    for root, dirs, files in os.walk(directory):
        # Exclude unwanted directories
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for file in files:
            if file in EXCLUDE_FILES:
                continue
            file_path = Path(root) / file
            arcname = file_path.relative_to(base)
            ziph.write(file_path, arcname)


def generate_requirements() -> str:
    try:
        output = subprocess.check_output(
            [sys.executable, '-m', 'pip', 'freeze'], text=True
        )
    except subprocess.CalledProcessError:
        output = ''
    return output


def main() -> None:
    base = project_root()
    output_zip = base / 'jaro_tooth_release_v1.zip'

    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for item in ['core', 'modules', 'config', 'interface', 'tests']:
            path = base / item
            if path.exists():
                zip_directory(zipf, path, base)
        readme = base / 'README.md'
        if readme.exists():
            zipf.write(readme, readme.relative_to(base))
        reqs = generate_requirements()
        zipf.writestr('requirements.txt', reqs)

    print(f"Created release: {output_zip}")


if __name__ == '__main__':
    main()
