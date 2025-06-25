import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from modules import braindump_module
from core.user_config import get_user_value
from core.jaro_manifest import get_manifest_value


def test_debug_output_runs():
    braindump_module.debug_output()


def test_config_values_valid():
    reflectie = get_user_value("reflectie")
    manifest_value = get_manifest_value("stress_gedrag.mag_overbelasting_benoemen")
    assert reflectie is not None
    assert isinstance(reflectie, bool)
    assert manifest_value is not None
    assert isinstance(manifest_value, bool)
