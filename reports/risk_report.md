# Risk Metrics Report

## Methodology

- Trading days per year assumption: 252
- Risk-free rate assumption: 0.00%
- Daily returns are based on adjusted closing prices.
- VaR is reported as a positive loss number.
- Expected Shortfall is included as an optional downside-risk extension.

## Risk Metrics

| Ticker   | Start Date   | End Date   |   Observations | Total Return   | Annualized Return   | Annualized Volatility   |   Sharpe Ratio | Maximum Drawdown   | Historical VaR 95   | Historical VaR 99   | Expected Shortfall 95   |
|:---------|:-------------|:-----------|---------------:|:---------------|:--------------------|:------------------------|---------------:|:-------------------|:--------------------|:--------------------|:------------------------|
| AAPL     | 2018-01-03   | 2026-05-19 |           2105 | 638.68%        | 27.05%              | 30.53%                  |           0.89 | -38.52%            | 2.97%               | 4.98%               | 4.36%                   |
| DB1.DE   | 2018-01-03   | 2026-05-19 |           2125 | 219.15%        | 14.75%              | 22.01%                  |           0.67 | -36.97%            | 2.02%               | 3.42%               | 3.10%                   |
| MSFT     | 2018-01-03   | 2026-05-19 |           2105 | 430.23%        | 22.10%              | 28.52%                  |           0.77 | -37.15%            | 2.78%               | 4.53%               | 4.04%                   |
| SAP.DE   | 2018-01-03   | 2026-05-19 |           2125 | 93.02%         | 8.11%               | 27.85%                  |           0.29 | -50.12%            | 2.68%               | 4.32%               | 4.06%                   |
| ^GDAXI   | 2018-01-03   | 2026-05-19 |           2124 | 88.32%         | 7.80%               | 19.08%                  |           0.41 | -38.78%            | 1.77%               | 3.61%               | 2.86%                   |
| ^GSPC    | 2018-01-03   | 2026-05-19 |           2105 | 171.02%        | 12.68%              | 19.38%                  |           0.65 | -33.92%            | 1.79%               | 3.39%               | 2.94%                   |

## Correlation Matrix

| Ticker   |   AAPL |   DB1.DE |   MSFT |   SAP.DE |   ^GDAXI |   ^GSPC |
|:---------|-------:|---------:|-------:|---------:|---------:|--------:|
| AAPL     |  1     |    0.176 |  0.675 |    0.27  |    0.348 |   0.768 |
| DB1.DE   |  0.176 |    1     |  0.223 |    0.4   |    0.512 |   0.269 |
| MSFT     |  0.675 |    0.223 |  1     |    0.365 |    0.365 |   0.794 |
| SAP.DE   |  0.27  |    0.4   |  0.365 |    1     |    0.667 |   0.372 |
| ^GDAXI   |  0.348 |    0.512 |  0.365 |    0.667 |    1     |   0.546 |
| ^GSPC    |  0.768 |    0.269 |  0.794 |    0.372 |    0.546 |   1     |

## Interpretation Notes

- Higher annualized return is positive, but it should not be interpreted without volatility and drawdown.
- Higher annualized volatility means stronger historical fluctuation.
- Higher Sharpe Ratio indicates better historical risk-adjusted return under the chosen assumptions.
- More negative Maximum Drawdown indicates a stronger historical loss phase.
- VaR estimates a historical loss threshold, but it does not describe how severe losses beyond that threshold can become.
- Correlation shows linear co-movement between assets and is relevant for diversification analysis.