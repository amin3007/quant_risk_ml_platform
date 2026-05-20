import pandas as pd

from src.risk.metrics import (
    calculate_total_return,
    calculate_max_drawdown,
    calculate_historical_var,
)


# Verifies that total return uses the first and last adjusted close prices,
# which is the headline performance metric for each asset.
def test_calculate_total_return():
    data = pd.DataFrame(
        {
            "Adj Close": [100, 110, 121],
            "Daily Return": [0.10, 0.10, 0.10],
        }
    )

    result = calculate_total_return(data)

    assert round(result, 2) == 0.21


# Verifies that drawdown captures the worst peak-to-trough loss, an important
# risk measure that return averages can hide.
def test_calculate_max_drawdown():
    data = pd.DataFrame(
        {
            "Daily Return": [0.10, -0.20, 0.05],
        }
    )

    result = calculate_max_drawdown(data)

    assert round(result, 2) == -0.20


# Verifies that historical VaR is reported as a positive loss number, matching
# the convention used in the generated risk report.
def test_calculate_historical_var():
    data = pd.DataFrame(
        {
            "Daily Return": [-0.05, -0.02, 0.01, 0.02, 0.03],
        }
    )

    result = calculate_historical_var(data, confidence_level=0.80)

    assert result > 0
