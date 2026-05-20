# Quantitative Risk & ML Portfolio Intelligence Platform

Python-based quantitative finance project for historical market data processing, return analysis and portfolio risk evaluation.

The project builds a reproducible data pipeline for financial market data, calculates daily and log returns, and derives core quantitative risk metrics such as annualized return, annualized volatility, Sharpe Ratio, Maximum Drawdown, historical Value at Risk, Expected Shortfall and asset correlations.

The goal is not to predict exact future stock prices. The current focus is on historical risk analysis and building a structured foundation for later market regime classification and machine learning experiments.

## Current Status

Implemented:

- Historical market data download with `yfinance`
- Raw market data storage as CSV
- Data cleaning and validation pipeline
- Processed price dataset generation
- Daily return calculation
- Log return calculation
- Returns summary report
- Quantitative risk metrics calculation
- Correlation matrix generation
- Risk report generation

Planned next steps:

- Feature engineering for machine learning
- Rule-based market regime labeling
- ML model training and evaluation
- Streamlit dashboard
- Backtesting module
- Unit tests for core financial calculations

## Tech Stack

- Python
- pandas
- NumPy
- yfinance
- scikit-learn
- Streamlit
- Plotly or matplotlib
- pytest
- Git and GitHub

## Project Structure

```text
quant_risk_ml_platform/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── reports/
│   └── figures/
│
├── src/
│   ├── data/
│   │   ├── fetch_data.py
│   │   └── clean_data.py
│   │
│   ├── features/
│   │   └── returns.py
│   │
│   └── risk/
│       └── metrics.py
│
├── tests/
│
├── README.md
├── requirements.txt
└── PROJECT_SCOPE.md
```

## Core Functionality

### 1. Market Data Pipeline

The project downloads historical OHLCV market data for selected assets and stores the raw dataset in `data/raw/`.

### 2. Data Cleaning

The cleaning pipeline validates required columns, converts data types, handles missing values, removes duplicate records and stores the processed dataset in `data/processed/`.

### 3. Return Calculation

The project calculates simple daily returns and logarithmic returns based on adjusted closing prices. These returns are used as the foundation for risk metrics and later machine learning features.

### 4. Risk Metrics

The risk module calculates:

- Total Return
- Annualized Return
- Annualized Volatility
- Sharpe Ratio
- Maximum Drawdown
- Historical Value at Risk
- Expected Shortfall
- Correlation Matrix

## How to Run

Create and activate a virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Run the market data download:

```powershell
python -m src.data.fetch_data
```

Run the cleaning pipeline:

```powershell
python -m src.data.clean_data
```

Calculate returns:

```powershell
python -m src.features.returns
```

Calculate risk metrics:

```powershell
python -m src.risk.metrics
```

## Output Files

```text
data/raw/prices_raw.csv
data/processed/prices_clean.csv
data/processed/returns.csv
data/processed/risk_metrics.csv
data/processed/correlation_matrix.csv
reports/data_quality_report.md
reports/returns_summary.md
reports/risk_report.md
```

## Methodology

The project uses adjusted closing prices as the basis for return calculations. Daily returns are used to compute historical risk metrics. Annualized metrics assume 252 trading days per year.

Value at Risk is calculated using the historical distribution of daily returns. Expected Shortfall is included as an additional downside-risk metric that measures the average loss beyond the VaR threshold.

The current version is based on historical analysis only. It does not provide financial advice, does not execute trades and does not claim to predict future market prices.

## Next Development Steps

1. Add rolling return, volatility and momentum features
2. Define rule-based market regime labels
3. Train classification models for market regime detection
4. Evaluate models with F1-score and confusion matrix
5. Build a Streamlit dashboard for interactive analysis
6. Add unit tests for return and risk metric calculations
7. Add a basic backtesting module

## Disclaimer

This project is for educational and portfolio purposes only. It is not financial advice and should not be used for real investment decisions.