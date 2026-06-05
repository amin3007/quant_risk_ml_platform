import pandas as pd

from src.data.clean_data import clean_market_data
from src.features.returns import calculate_returns
from src.risk.metrics import calculate_risk_metrics, calculate_correlation_matrix


def test_cleaning_returns_and_risk_metrics_pipeline_with_synthetic_data():
    raw_data = pd.DataFrame(
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
            "Open": [100, 101, 102, 200, 198, 196],
            "High": [101, 102, 103, 201, 199, 197],
            "Low": [99, 100, 101, 199, 197, 195],
            "Close": [100, 110, 121, 200, 180, 162],
            "Adj Close": [100, 110, 121, 200, 180, 162],
            "Volume": [1000, 1100, 1200, 2000, 2100, 2200],
        }
    )

    cleaned = clean_market_data(raw_data)
    returns = calculate_returns(cleaned)
    risk_metrics = calculate_risk_metrics(returns)
    correlation_matrix = calculate_correlation_matrix(returns)

    assert cleaned.shape[0] == 6
    assert returns.shape[0] == 4
    assert set(returns["Ticker"]) == {"AAA", "BBB"}

    assert set(
        [
            "Ticker",
            "Total Return",
            "Annualized Return",
            "Annualized Volatility",
            "Sharpe Ratio",
            "Maximum Drawdown",
            "Historical VaR 95",
            "Expected Shortfall 95",
        ]
    ).issubset(risk_metrics.columns)

    assert risk_metrics.shape[0] == 2
    assert correlation_matrix.shape == (2, 2)