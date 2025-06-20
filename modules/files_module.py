"""Bestandsmodule voor JARO-TOOTH.

Dit module biedt functionaliteit om bestanden in de datamap te sorteren op basis van hun extensie. De implementatie blijft bewust eenvoudig en uitbreidbaar zodat nieuwe bestandssoorten of acties later kunnen worden toegevoegd.

Functies
--------
start()
    Print een bevestiging dat de bestandsmodule is gestart.
auto_sort(doelmap="data")
    Sorteer bestanden naar submappen op basis van extensie.
"""

from __future__ import annotations

import os
import shutil


def start() -> None:
    """Initialiseer de bestandsmodule."""
    print("\U0001F5C2 Bestandsmodule gestart")


def _bepaal_submap(ext: str) -> str:
    """Geef de naam van de submap passend bij een extensie."""
    ext = ext.lower()
    mapping = {
        ".pdf": "pdf",
        ".jpg": "img",
        ".jpeg": "img",
        ".png": "img",
        ".docx": "docs",
        ".txt": "docs",
    }
    return mapping.get(ext, "other")


def _icon_for(ext: str) -> str:
    """Kies een icoon passend bij het bestandstype."""
    icons = {
        "pdf": "\U0001F4C4",  # 📄
        "img": "\U0001F5BC",  # 🖼
        "docs": "\U0001F4DD",  # 📝
        "other": "\U0001F4C1",  # 📁
    }
    return icons.get(_bepaal_submap(ext), "\U0001F4C1")


def auto_sort(doelmap: str = "data") -> None:
    """Sorteer bestanden in ``doelmap`` naar submappen op basis van extensie.

    Parameters
    ----------
    doelmap : str, optional
        De naam van de map binnen het project waarin gezocht wordt. Standaard
        ``"data"``.
    """
    repo_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    data_dir = os.path.join(repo_dir, doelmap)

    if not os.path.isdir(data_dir):
        print(f"Map '{data_dir}' bestaat niet")
        return

    for naam in os.listdir(data_dir):
        pad = os.path.join(data_dir, naam)
        if os.path.isdir(pad):
            continue
        ext = os.path.splitext(naam)[1]
        submap = _bepaal_submap(ext)
        target_dir = os.path.join(data_dir, submap)
        os.makedirs(target_dir, exist_ok=True)
        dest = os.path.join(target_dir, naam)
        icoon = _icon_for(ext)
        try:
            shutil.move(pad, dest)
            status = "verplaatst"
        except (OSError, shutil.Error) as exc:
            status = f"overgeslagen ({exc})"
        rel_dest = os.path.relpath(dest, repo_dir)
        print(f"{icoon} {naam} → {rel_dest} ({status})")

