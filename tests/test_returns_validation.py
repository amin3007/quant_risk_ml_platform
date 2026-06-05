import pandas as pd
import pytest
import numpy as np

from src.features.returns import calculate_returns, validate_price_data


def test_validate_price_data_rejects_missing_columns():
    data = pd.DataFrame(
        {
            "Date": ["2024-01-01"],
            "Ticker": ["AAA"],
        }
    )

    with pytest.raises(ValueError, match="Missing required columns"):
        validate_price_data(data)


def test_validate_price_data_rejects_negative_prices():
    data = pd.DataFrame(
        {
            "Date": ["2024-01-01"],
            "Ticker": ["AAA"],
            "Adj Close": [-100.0],
        }
    )

    with pytest.raises(ValueError, match="non-positive prices"):
        validate_price_data(data)


def test_calculate_returns_with_one_observation_per_ticker_returns_empty_dataframe():
    data = pd.DataFrame(
        {
            "Date": ["2024-01-01", "2024-01-01"],
            "Ticker": ["AAA", "BBB"],
            "Adj Close": [100.0, 200.0],
        }
    )

    result = calculate_returns(data)

    assert result.empty
    assert "Daily Return" in result.columns
    assert "Log Return" in result.columns


def test_calculate_returns_sorts_by_ticker_and_date():
    data = pd.DataFrame(
        {
            "Date": ["2024-01-02", "2024-01-01", "2024-01-02", "2024-01-01"],
            "Ticker": ["AAA", "AAA", "BBB", "BBB"],
            "Adj Close": [110.0, 100.0, 180.0, 200.0],
        }
    )

    result = calculate_returns(data)

    aaa_return = result.loc[result["Ticker"] == "AAA", "Daily Return"].iloc[0]
    bbb_return = result.loc[result["Ticker"] == "BBB", "Daily Return"].iloc[0]

    assert np.isclose(aaa_return, 0.10)
    assert np.isclose(bbb_return, -0.10)