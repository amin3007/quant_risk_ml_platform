# Quantitative Risk Analysis Platform

Python-based portfolio project for reproducible market data processing, return calculation, and historical risk analysis.

The current version is a functional risk analysis prototype. It provides a CSV-based data pipeline, core risk metrics, correlation analysis, markdown reports, and automated tests. Machine learning, dashboard functionality, and backtesting are planned extensions and are not yet implemented.

This project is for educational and portfolio purposes only. It does not provide financial advice and does not attempt to predict future market prices.

## Project Status

### Implemented

- Historical market data ingestion using `yfinance`
- Raw price storage under `data/raw/`
- Data cleaning pipeline for market price data
- Cleaned price output under `data/processed/prices_clean.csv`
- Daily simple returns and logarithmic returns
- CSV integrity validation for generated artifacts
- Risk metric calculation:
  - Total Return
  - Annualized Return
  - Annualized Volatility
  - Sharpe Ratio
  - Maximum Drawdown
  - Historical Value at Risk
  - Expected Shortfall
- Correlation matrix generation
- Markdown reports under `reports/`
- Unit and integration tests with `pytest`

### Partially Implemented

- Modular project structure under `src/`
- Reproducible pipeline stages
- Data quality reporting
- Foundation for later quantitative feature engineering
- Test coverage for core pipeline behavior and edge cases

### Planned

- Rolling volatility features
- Momentum features
- Rolling drawdown features
- Correlation and drawdown visualizations
- Rule-based market regime labels
- Baseline machine learning model with `scikit-learn`
- Model evaluation with Accuracy, F1-score, and Confusion Matrix
- Optional interactive dashboard
- Optional backtesting module

## Current Project Scope

The project currently focuses on historical risk analysis.

It answers questions such as:

- Are the raw price data files readable and clean?
- Can daily returns be calculated reproducibly?
- What are the main historical risk and performance metrics per asset?
- How strongly are assets correlated?
- Can the pipeline be tested end to end?

The project does not currently implement:

- Market prediction
- Trading signals
- Automated trading
- Backtesting
- Portfolio optimization
- A production dashboard
- A trained machine learning model

## Architecture

```text
data/
  raw/
    prices_raw.csv

  processed/
    prices_clean.csv
    returns.csv
    risk_metrics.csv
    correlation_matrix.csv

reports/
  data_quality_report.md
  returns_summary.md
  risk_report.md

src/
  config.py

  data/
    clean_data.py
    csv_integrity.py
    fetch_data.py

  features/
    returns.py

  risk/
    metrics.py

tests/
  test_artifact_paths.py
  test_clean_data_edge_cases.py
  test_csv_integrity.py
  test_pipeline_integration.py
  test_returns_artifact_pipeline.py
  test_returns_validation.py
  test_risk_metrics.py
  test_risk_metrics_extended.py
```

## Pipeline Overview

```text
Raw Market Data
      |
      v
Data Cleaning
      |
      v
Cleaned Prices CSV
      |
      v
Return Calculation
      |
      v
Returns CSV
      |
      v
Risk Metrics and Correlation Matrix
      |
      v
Markdown Reports
```

## Main Outputs

The pipeline creates the following processed data files:

```text
data/processed/prices_clean.csv
data/processed/returns.csv
data/processed/risk_metrics.csv
data/processed/correlation_matrix.csv
```

It also creates the following reports:

```text
reports/data_quality_report.md
reports/returns_summary.md
reports/risk_report.md
```

## Risk Metrics

The current risk analysis includes:

- **Total Return**  
  Historical return from the first to the last available adjusted closing price.

- **Annualized Return**  
  Total return converted to a yearly scale using the configured trading-day assumption.

- **Annualized Volatility**  
  Standard deviation of daily returns annualized with the square-root-of-time convention.

- **Sharpe Ratio**  
  Historical risk-adjusted return based on the configured risk-free rate.

- **Maximum Drawdown**  
  Largest historical peak-to-trough decline.

- **Historical Value at Risk**  
  Historical lower-tail loss estimate reported as a positive loss number.

- **Expected Shortfall**  
  Average loss beyond the Value at Risk threshold.

- **Correlation Matrix**  
  Pairwise return correlation between all assets in the dataset.

## Data and Artifact Validation

The project includes CSV integrity checks to avoid silently using broken data artifacts.

The validation checks include:

- File existence
- Readable CSV format
- Non-empty data
- Required columns
- Rejection of malformed CSV files
- Detection of unexpected index-like columns such as `Unnamed: 0`

This is important because all downstream analytics depend on valid intermediate files, especially `returns.csv`.

## Installation

Create and activate a virtual environment.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies.

```powershell
pip install -r requirements.txt
```

## How To Run The Pipeline

Run the pipeline stages in order.

```powershell
.\.venv\Scripts\python.exe -m src.data.clean_data
.\.venv\Scripts\python.exe -m src.features.returns
.\.venv\Scripts\python.exe -m src.risk.metrics
```

This regenerates the cleaned prices, returns, risk metrics, correlation matrix, and markdown reports.

## How To Run Tests

```powershell
.\.venv\Scripts\python.exe -m pytest
```

The test suite covers:

- CSV artifact integrity
- Data cleaning edge cases
- Return calculation validation
- Risk metric calculations
- Pipeline integration from cleaning to risk metrics
- Output path consistency

## Technology Stack

Currently used:

- Python
- pandas
- NumPy
- yfinance
- pytest
- tabulate

Installed or planned for later extensions:

- scikit-learn
- matplotlib
- Plotly
- Streamlit

## Roadmap

### Step 1: Stabilization

Completed focus:

- Regenerate broken `returns.csv`
- Validate CSV artifacts
- Ensure risk metrics can be calculated from saved returns

### Step 2: Project Structure Cleanup

Completed focus:

- Rename feature package to `src/features/`
- Use valid `__init__.py` files
- Clean up package structure

### Step 3: Path and Artifact Consistency

Completed focus:

- Use centralized paths from `src/config.py`
- Store processed CSV files under `data/processed/`
- Store reports under `reports/`

### Step 4: Test Coverage Expansion

Completed focus:

- Add unit tests for risk metrics
- Add edge case tests for data cleaning and return calculation
- Add integration tests for the pipeline

### Step 5: Documentation Cleanup

Current focus:

- Clearly document what is implemented
- Clearly separate implemented, partially implemented, and planned features
- Avoid overstating ML, dashboard, or backtesting functionality

### Step 6: Quant Feature Engineering

Planned:

- Rolling volatility
- Momentum
- Rolling drawdown
- Drawdown status
- Correlation and drawdown visualizations

### Step 7: Machine Learning Baseline

Planned:

- Rule-based regime labels
- Feature matrix construction
- Time-aware train-test split
- Baseline classifier with `scikit-learn`
- Evaluation with Accuracy, F1-score, and Confusion Matrix
- Clear documentation of model limitations

## Limitations

The current project is not a trading system.

It does not:

- Predict exact future stock prices
- Generate trading recommendations
- Execute trades
- Backtest trading strategies
- Optimize portfolios
- Provide investment advice

The current focus is historical risk analysis and building a stable foundation for later quantitative feature engineering and machine learning experiments.

## Portfolio Positioning

This project demonstrates the ability to build a structured Python analytics project in a financial domain.

It highlights:

- Reproducible data pipelines
- Defensive data validation
- Financial risk metric implementation
- Clear artifact organization
- Automated testing
- Honest project documentation
- A realistic roadmap toward machine learning

The strongest current positioning is:

> A reproducible Python risk analysis prototype with clean data artifacts, tested risk metrics, and a clear roadmap toward market regime classification.