import sys
from types import SimpleNamespace
from unittest.mock import MagicMock

import pandas as pd
import pytest

from src.analysis.sentiment_analysis import Sentiment
from src.core.user import User


@pytest.fixture(autouse=True)
def reset_sentiment_pipeline():
    Sentiment._pipeline = None
    yield
    Sentiment._pipeline = None


def test_positive_label_returns_positive_score():
    predictions = [
        [
            {"label": "Negative", "score": 0.05},
            {"label": "Neutral", "score": 0.10},
            {"label": "Positive", "score": 0.85},
        ]
    ]

    assert Sentiment.get_polarity_score(predictions) == pytest.approx(0.80)


def test_negative_label_returns_negative_score():
    predictions = [
        [
            {"label": "Negative", "score": 0.70},
            {"label": "Neutral", "score": 0.20},
            {"label": "Positive", "score": 0.10},
        ]
    ]

    assert Sentiment.get_polarity_score(predictions) == pytest.approx(-0.60)


def test_neutral_label_returns_zero_score():
    predictions = [[{"label": "Neutral", "score": 0.95}]]

    assert Sentiment.get_polarity_score(predictions) == 0.0


def test_empty_text_returns_zero_without_calling_model(monkeypatch):
    build_pipeline = MagicMock()
    monkeypatch.setattr(Sentiment, "_build_pipeline", build_pipeline)

    assert Sentiment.huggingface("   ") == 0.0
    build_pipeline.assert_not_called()


def test_pipeline_is_cached(monkeypatch):
    build_pipeline = MagicMock(
        return_value=MagicMock(
            return_value=[
                [
                    {"label": "Negative", "score": 0.10},
                    {"label": "Neutral", "score": 0.20},
                    {"label": "Positive", "score": 0.70},
                ]
            ]
        )
    )
    monkeypatch.setattr(Sentiment, "_build_pipeline", build_pipeline)

    assert Sentiment.huggingface("good") == pytest.approx(0.60)
    assert Sentiment.huggingface("great") == pytest.approx(0.60)
    build_pipeline.assert_called_once()


def test_build_pipeline_uses_available_device(monkeypatch):
    pipeline = MagicMock()
    monkeypatch.setattr(Sentiment, "_get_device", lambda: "mps")
    monkeypatch.setitem(sys.modules, "transformers", SimpleNamespace(pipeline=pipeline))

    Sentiment._build_pipeline()

    pipeline.assert_called_once_with(
        "sentiment-analysis",
        model=Sentiment.MODEL_ID,
        tokenizer=Sentiment.MODEL_ID,
        device="mps",
        top_k=None,
    )


def test_get_message_sentiment_writes_polarity_score(monkeypatch):
    logger = MagicMock()
    user = User(
        user_name="Alice",
        messages=pd.Series(["bagundi", "bad"]),
        timestamp=pd.to_datetime(pd.Series(["2023-01-12 09:00", "2023-01-12 09:01"])),
        logger=logger,
    )
    user.data["Clean Message"] = pd.Series(["bagundi", "bad"])
    monkeypatch.setattr(Sentiment, "huggingface", lambda text: 0.5 if text else 0.0)

    user.get_message_sentiment()

    assert user.data["Polarity Score"].tolist() == [0.5, 0.5]
