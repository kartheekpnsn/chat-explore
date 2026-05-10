import pandas as pd
import pytest

from src.core.response import Response


def _make_df(rows):
    """rows: list of (timestamp_str, user, message)"""
    df = pd.DataFrame(rows, columns=["Timestamp", "User", "Message"])
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    df["Date"] = df["Timestamp"].dt.strftime("%d-%b-%Y")
    df["Weekday"] = df["Timestamp"].dt.strftime("%a")
    return df


def test_normal_conversation_returns_stats():
    df = _make_df(
        [
            ("2023-01-12 09:00", "Alice", "hi"),
            ("2023-01-12 09:05", "Bob", "hey"),  # Bob responds 5 min after Alice
            (
                "2023-01-12 09:10",
                "Alice",
                "how are you",
            ),  # Alice responds 5 min after Bob
            ("2023-01-12 09:20", "Bob", "good"),  # Bob responds 10 min after Alice
        ]
    )
    stats = Response(df).compute()
    assert "Alice" in stats
    assert "Bob" in stats
    assert stats["Bob"]["n_responses"] == 2
    assert stats["Alice"]["n_responses"] == 1
    assert stats["Bob"]["median_response_min"] == pytest.approx(7.5, abs=0.1)
    assert stats["Alice"]["median_response_min"] == pytest.approx(5.0, abs=0.1)


def test_single_user_no_responses():
    df = _make_df(
        [
            ("2023-01-12 09:00", "Alice", "hi"),
            ("2023-01-12 09:05", "Alice", "hello?"),
        ]
    )
    stats = Response(df).compute()
    assert stats["Alice"]["n_responses"] == 0
    assert stats["Alice"]["median_response_min"] is None


def test_empty_dataframe_returns_empty():
    df = _make_df([])
    stats = Response(df).compute()
    assert stats == {}


def test_longest_conversation_date():
    df = _make_df(
        [
            ("2023-01-12 09:00", "Alice", "hi"),
            ("2023-01-12 09:01", "Bob", "hey"),
            ("2023-01-13 09:00", "Alice", "hi again"),
            ("2023-01-13 09:05", "Bob", "hey again"),
            ("2023-01-13 09:10", "Alice", "lots more messages"),
            ("2023-01-13 09:11", "Bob", "yes"),
        ]
    )
    date = Response(df).get_the_longest_conversation_date()
    assert date == "13-Jan-2023"


def test_burst_messages_use_last_ts_for_gap():
    """When A sends 3 messages in a row, Bob's response time is measured
    from the *last* of Alice's messages, not the first."""
    df = _make_df(
        [
            ("2023-01-12 09:00", "Alice", "msg1"),
            ("2023-01-12 09:02", "Alice", "msg2"),
            ("2023-01-12 09:04", "Alice", "msg3"),  # last Alice msg
            ("2023-01-12 09:10", "Bob", "reply"),  # 6 min from 09:04, not 10 from 09:00
        ]
    )
    stats = Response(df).compute()
    assert stats["Bob"]["n_responses"] == 1
    assert stats["Bob"]["median_response_min"] == pytest.approx(6.0, abs=0.1)
