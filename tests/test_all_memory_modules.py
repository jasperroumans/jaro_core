import json
import csv
from pathlib import Path

import pytest

from tools.memory_visualizer import generate_overview
from tools.memory_feedback_loop import update_feedback
from modules.tracker_recovery_module import run as recovery_run
from modules.task_focus_module import log_focus


def _read_json(path: Path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def test_memory_visualizer_success(tmp_path):
    log_path = tmp_path / 'log_001.json'
    log_data = {
        "memory_name": "test_memory",
        "generated": "now",
        "files": [{"path": "a", "memory_path": "a"}],
    }
    log_path.write_text(json.dumps(log_data))

    json_path, md_path = generate_overview(log_path=log_path, output_dir=tmp_path)
    assert json_path.exists()
    assert md_path.exists()

    output = _read_json(json_path)
    assert output["file_count"] == 1
    assert output["memory_name"] == "test_memory"


def test_memory_visualizer_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        generate_overview(log_path=tmp_path / 'missing.json', output_dir=tmp_path)


def test_memory_feedback_loop_success(tmp_path):
    log_file = tmp_path / 'log_002.json'
    result = update_feedback(modules_dir='modules', log_file=log_file)
    assert result == log_file
    data = _read_json(log_file)
    assert data and all("memory_path" in entry for entry in data)


def test_memory_feedback_loop_invalid_json(tmp_path):
    log_file = tmp_path / 'log_002.json'
    log_file.write_text('{ invalid')
    with pytest.raises(json.JSONDecodeError):
        update_feedback(modules_dir='modules', log_file=log_file)


def test_recovery_module_success(tmp_path):
    json_path, xlsx_path = recovery_run(output_dir=tmp_path)
    assert json_path.exists()
    assert xlsx_path.exists()

    data = _read_json(json_path)
    assert "entries" in data and isinstance(data["entries"], list)


def test_recovery_module_invalid_output_dir(tmp_path):
    file_path = tmp_path / 'dummy'
    file_path.write_text('data')
    with pytest.raises(FileExistsError):
        recovery_run(output_dir=file_path)


def test_task_focus_module_success(tmp_path):
    log_file = log_focus('test-task', 'FOCUS', 'note', log_dir=tmp_path)
    assert log_file.exists()
    with open(log_file, newline='', encoding='utf-8') as f:
        rows = list(csv.reader(f))
    assert len(rows) >= 2


def test_task_focus_module_invalid_log_dir(tmp_path):
    file_path = tmp_path / 'dummy'
    file_path.write_text('data')
    with pytest.raises(FileExistsError):
        log_focus('task', log_dir=file_path)
