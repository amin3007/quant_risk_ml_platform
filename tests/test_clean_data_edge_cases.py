import pandas as pd
import pytest

from src.data.clean_data import clean_market_data


def test_clean_market_data_rejects_missing_required_columns():
    raw_data = pd.DataFrame(
        {
            "Date": ["2024-01-01"],
            "Ticker": ["AAA"],
            "Adj Close": [100.0],
        }
    )

    with pytest.raises(ValueError, match="Missing required columns"):
        clean_market_data(raw_data)


def test_clean_market_data_drops_rows_with_invalid_dates():
    raw_data = pd.DataFrame(
        {
            "Date": ["not-a-date", "2024-01-02"],
            "Ticker": ["AAA", "AAA"],
            "Open": [100, 101],
            "High": [101, 102],
            "Low": [99, 100],
            "Close": [100, 101],
            "Adj Close": [100, 101],
            "Volume": [1000, 1100],
        }
    )

    cleaned = clean_market_data(raw_data)

    assert cleaned.shape[0] == 1
    assert cleaned["Date"].iloc[0] == pd.Timestamp("2024-01-02")


def test_clean_market_data_removes_duplicate_ticker_date_rows():
    raw_data = pd.DataFrame(
        {
            "Date": ["2024-01-01", "2024-01-01"],
            "Ticker": ["AAA", "AAA"],
            "Open": [100, 101],
            "High": [101, 102],
            "Low": [99, 100],
            "Close": [100, 101],
            "Adj Close": [100, 101],
            "Volume": [1000, 1100],
        }
    )

    cleaned = clean_market_data(raw_data)

    assert cleaned.shape[0] == 1
    assert cleaned["Adj Close"].iloc[0] == 101