import re
import pandas as pd
from typing import Optional


class ParseError(Exception):
    pass


_PATTERNS = [
    {
        "name": "android_24h",
        "header": re.compile(
            r"^(\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2})\s-\s([^:]+):\s(.*)$"
        ),
        "ts_formats": ["%d/%m/%y, %H:%M", "%m/%d/%y, %H:%M"],
    },
    {
        "name": "android_12h",
        "header": re.compile(
            r"^(\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[aApP][mM])\s-\s([^:]+):\s(.*)$"
        ),
        "ts_formats": ["%d/%m/%y, %I:%M %p", "%m/%d/%y, %I:%M %p"],
    },
    {
        "name": "ios",
        "header": re.compile(
            r"^\[(\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}:\d{2})\]\s([^:]+):\s(.*)$"
        ),
        "ts_formats": ["%d/%m/%Y, %H:%M:%S", "%m/%d/%Y, %H:%M:%S"],
    },
]

_MATCH_THRESHOLD = 0.5


class ChatParser:

    def __init__(self, file_path: str):
        self.file_path = file_path

    def parse(self) -> pd.DataFrame:
        with open(self.file_path, "r", encoding="utf-8") as f:
            lines = [l.rstrip("\n") for l in f if l.strip()]

        pattern, ts_format = self._detect_pattern(lines)
        rows = self._extract_rows(lines, pattern, ts_format)

        df = pd.DataFrame(rows, columns=["Timestamp", "User", "Message"])
        df["Timestamp"] = pd.to_datetime(df["Timestamp"], format=ts_format)
        df["Date"] = df["Timestamp"].dt.strftime("%d-%b-%Y")
        df["Weekday"] = df["Timestamp"].dt.strftime("%a")
        return df

    def _detect_pattern(self, lines: list[str]):
        for pat in _PATTERNS:
            regex = pat["header"]
            matched = sum(1 for l in lines if regex.match(l))
            if matched / max(len(lines), 1) >= _MATCH_THRESHOLD:
                ts_format = self._detect_ts_format(lines, regex, pat["ts_formats"])
                return regex, ts_format
        raise ParseError(
            f"Could not detect a known WhatsApp export format in {self.file_path}. "
            "Supported formats: Android 24h, Android 12h, iOS."
        )

    def _detect_ts_format(self, lines: list[str], regex, ts_formats: list[str]) -> str:
        sample = next((l for l in lines if regex.match(l)), None)
        if sample is None:
            return ts_formats[0]
        ts_str = regex.match(sample).group(1)
        for fmt in ts_formats:
            try:
                pd.to_datetime(ts_str, format=fmt)
                return fmt
            except ValueError:
                continue
        return ts_formats[0]

    def _extract_rows(self, lines: list[str], pattern, ts_format: str) -> list[tuple]:
        rows: list[tuple] = []
        for line in lines:
            m = pattern.match(line)
            if m:
                rows.append((m.group(1), m.group(2).strip(), m.group(3)))
            elif rows:
                ts, user, msg = rows[-1]
                rows[-1] = (ts, user, msg + "\n" + line)
        return rows
