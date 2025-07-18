import os
import json
import csv
from pathlib import Path

import pytest

from tools.memory_visualizer import generate_overview
from tools.memory_feedback_loop import update_feedback
from modules.tracker_recovery_module import run as recovery_run
from modules.task_focus_module import log_focus


def test_memory_visualizer(tmp_path):
    json_path, md_path = generate_overview(
        log_path=Path('data') / 'log_001.json',
        output_dir=tmp_path,
    )
    assert json_path.exists()
    assert md_path.exists()


def test_memory_feedback_loop(tmp_path):
    log_file = tmp_path / 'log_002.json'
    update_feedback(modules_dir='modules', log_file=log_file)
    assert log_file.exists()
    data = json.loads(log_file.read_text())
    assert data


def test_recovery_module(tmp_path):
    json_path, xlsx_path = recovery_run(output_dir=tmp_path)
    assert json_path.exists()
    assert xlsx_path.exists()


def test_task_focus_module(tmp_path):
    log_file = log_focus('test', 'FOCUS', 'note', log_dir=tmp_path)
    assert log_file.exists()
    with open(log_file, newline='', encoding='utf-8') as f:
        rows = list(csv.reader(f))
    assert len(rows) >= 2
