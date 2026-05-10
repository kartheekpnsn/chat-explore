import os
import subprocess
import sys


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


def test_write_data_creates_missing_directory(tmp_path):
    from unittest.mock import MagicMock

    import pandas as pd

    from src.core.preprocess import Preprocess

    p = Preprocess(input_file="fake.txt", logger=MagicMock())
    p.pd_data = pd.DataFrame(
        {
            "Timestamp": pd.to_datetime(["2023-01-12 09:00"]),
            "User": ["Alice"],
            "Message": ["hi"],
            "Date": ["12-Jan-2023"],
            "Weekday": ["Thu"],
        }
    )
    out_path = str(tmp_path / "nested" / "deep" / "output.xlsx")
    p.write_data(path=out_path)
    assert os.path.exists(out_path)
