import subprocess
import sys
import os
import pytest


def run_cli(*args):
    result = subprocess.run(
        [sys.executable, "run.py"] + list(args),
        capture_output=True,
        text=True,
        cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    )
    return result


def test_missing_file_flag_exits_nonzero():
    result = run_cli()
    assert result.returncode != 0


def test_missing_file_flag_prints_error():
    result = run_cli()
    output = result.stdout + result.stderr
    assert "file" in output.lower() or "usage" in output.lower()


def test_nonexistent_file_exits_nonzero():
    result = run_cli("-f", "/tmp/does_not_exist_abc123.txt")
    assert result.returncode != 0


def test_nonexistent_file_prints_error():
    result = run_cli("-f", "/tmp/does_not_exist_abc123.txt")
    output = result.stdout + result.stderr
    assert "not found" in output.lower() or "error" in output.lower()


def test_empty_file_exits_nonzero(tmp_path):
    f = tmp_path / "empty.txt"
    f.write_text("")
    result = run_cli("-f", str(f))
    assert result.returncode != 0
