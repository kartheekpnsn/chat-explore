import pytest
import pandas as pd
from src.core.parser import ChatParser, ParseError
from tests.conftest import ANDROID_24H_CHAT, GARBAGE_CHAT


def test_android_24h_returns_dataframe(tmp_path):
    f = tmp_path / "chat.txt"
    f.write_text(ANDROID_24H_CHAT, encoding="utf-8")
    df = ChatParser(str(f)).parse()
    assert isinstance(df, pd.DataFrame)


def test_android_24h_columns(tmp_path):
    f = tmp_path / "chat.txt"
    f.write_text(ANDROID_24H_CHAT, encoding="utf-8")
    df = ChatParser(str(f)).parse()
    assert set(df.columns) >= {"Timestamp", "User", "Message", "Date", "Weekday"}


def test_android_24h_row_count(tmp_path):
    f = tmp_path / "chat.txt"
    f.write_text(ANDROID_24H_CHAT, encoding="utf-8")
    df = ChatParser(str(f)).parse()
    assert len(df) == 4


def test_android_24h_users(tmp_path):
    f = tmp_path / "chat.txt"
    f.write_text(ANDROID_24H_CHAT, encoding="utf-8")
    df = ChatParser(str(f)).parse()
    assert set(df["User"].unique()) == {"Alice", "Bob"}


def test_android_24h_message_with_hyphen(tmp_path):
    f = tmp_path / "chat.txt"
    f.write_text(ANDROID_24H_CHAT, encoding="utf-8")
    df = ChatParser(str(f)).parse()
    assert "Good, thanks - what about you?" in df["Message"].values


def test_garbage_raises_parse_error(tmp_path):
    f = tmp_path / "chat.txt"
    f.write_text(GARBAGE_CHAT, encoding="utf-8")
    with pytest.raises(ParseError):
        ChatParser(str(f)).parse()
