# Returns Summary

## Methodology

Daily returns are calculated using adjusted closing prices.

Simple daily return:

`Return_t = Price_t / Price_(t-1) - 1`

Log return:

`LogReturn_t = ln(Price_t / Price_(t-1))`

## Summary Table

| Ticker   | Start Date   | End Date   |   Rows |   Mean Daily Return |   Daily Volatility |   Min Daily Return |   Max Daily Return |
|:---------|:-------------|:-----------|-------:|--------------------:|-------------------:|-------------------:|-------------------:|
| AAPL     | 2018-01-03   | 2026-05-19 |   2105 |         0.0011349   |          0.0192305 |          -0.128647 |          0.153288  |
| DB1.DE   | 2018-01-03   | 2026-05-19 |   2125 |         0.000646561 |          0.0138643 |          -0.118372 |          0.131044  |
| MSFT     | 2018-01-03   | 2026-05-19 |   2105 |         0.000956442 |          0.0179687 |          -0.14739  |          0.142169  |
| SAP.DE   | 2018-01-03   | 2026-05-19 |   2125 |         0.000472178 |          0.0175464 |          -0.219376 |          0.125491  |
| ^GDAXI   | 2018-01-03   | 2026-05-19 |   2124 |         0.000374429 |          0.0120218 |          -0.122386 |          0.109759  |
| ^GSPC    | 2018-01-03   | 2026-05-19 |   2105 |         0.000551506 |          0.0122058 |          -0.119841 |          0.0951539 |

## Notes

- The first observation per ticker is removed because no previous price exists for return calculation.
- Adjusted closing prices are used as the basis for return calculation.
- These returns will be used later for risk metrics, feature engineering and model training.