from src.risk.metrics import (
    calculate_correlation_matrix,
    calculate_risk_metrics,
    load_returns,
)


def test_saved_returns_csv_can_feed_risk_metrics():
    returns_data = load_returns()

    risk_metrics = calculate_risk_metrics(returns_data)
    correlation_matrix = calculate_correlation_matrix(returns_data)

    assert not risk_metrics.empty
    assert set(risk_metrics["Ticker"]) == set(returns_data["Ticker"].unique())
    assert correlation_matrix.shape[0] == correlation_matrix.shape[1]
    assert correlation_matrix.shape[0] == returns_data["Ticker"].nunique()