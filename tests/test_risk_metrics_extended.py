import numpy as np
import pandas as pd

from src.risk.metrics import (
    calculate_annualized_return,
    calculate_annualized_volatility,
    calculate_sharpe_ratio,
    calculate_expected_shortfall,
    calculate_correlation_matrix,
)


def test_calculate_annualized_return():
    data = pd.DataFrame(
        {
            "Adj Close": [100.0, 121.0],
            "Daily Return": [0.10, 0.10],
        }
    )

    result = calculate_annualized_return(data, trading_days_per_year=2)

    assert np.isclose(result, 0.21)


def test_calculate_annualized_volatility():
    data = pd.DataFrame(
        {
            "Daily Return": [0.01, -0.01, 0.01, -0.01],
        }
    )

    result = calculate_annualized_volatility(data, trading_days_per_year=4)

    expected = data["Daily Return"].std() * np.sqrt(4)

    assert np.isclose(result, expected)


def test_calculate_sharpe_ratio():
    result = calculate_sharpe_ratio(
        annualized_return=0.12,
        annualized_volatility=0.20,
        risk_free_rate=0.02,
    )

    assert np.isclose(result, 0.5)


def test_calculate_sharpe_ratio_returns_nan_for_zero_volatility():
    result = calculate_sharpe_ratio(
        annualized_return=0.12,
        annualized_volatility=0.0,
        risk_free_rate=0.02,
    )

    assert np.isnan(result)


def test_calculate_expected_shortfall():
    data = pd.DataFrame(
        {
            "Daily Return": [-0.10, -0.05, 0.01, 0.02, 0.03],
        }
    )

    result = calculate_expected_shortfall(data, confidence_level=0.80)

    assert result > 0
    assert np.isclose(result, 0.10)


def test_calculate_correlation_matrix():
    data = pd.DataFrame(
        {
            "Date": [
                "2024-01-01",
                "2024-01-02",
                "2024-01-03",
                "2024-01-01",
                "2024-01-02",
                "2024-01-03",
            ],
            "Ticker": ["AAA", "AAA", "AAA", "BBB", "BBB", "BBB"],
            "Adj Close": [100, 101, 102, 200, 198, 196],
            "Daily Return": [0.01, 0.01, 0.01, -0.01, -0.01, -0.01],
        }
    )

    result = calculate_correlation_matrix(data)

    assert result.shape == (2, 2)
    assert set(result.columns) == {"AAA", "BBB"}
    assert set(result.index) == {"AAA", "BBB"}