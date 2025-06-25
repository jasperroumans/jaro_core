from __future__ import annotations

from typing import List

from core.user_config import get_user_value, is_user_enabled
from core.jaro_manifest import get_manifest_value


def get_active_modules() -> List[str]:
    """Bepaal welke modules actief moeten zijn op basis van configuratie."""
    context = get_user_value("active_context") or "werk"
    reflectie = is_user_enabled("reflectie")
    role_types = get_manifest_value("rol_en_karakter.type") or []

    modules: list[str] = []

    if context == "werk" and "observator" in role_types:
        modules.extend(["calendar", "notities", "files"])

    if context == "privé" and reflectie:
        modules.extend(["habit_tracker", "braindump"])

    if not modules:
        modules = get_user_value("modules") or []

    return modules

