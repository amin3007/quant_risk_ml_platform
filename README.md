# Quantitative Risk & ML Portfolio Intelligence Platform

This is a Python portfolio project focused on quantitative finance, risk analytics, and machine learning preparation. It builds a reproducible workflow for downloading historical market data, cleaning price series, calculating returns, and producing core portfolio risk metrics.

The project is designed as a CV project to demonstrate practical data engineering, financial analysis, clean Python structure, testing, and a clear path toward machine learning-based market regime classification.

This project does not provide financial advice and does not attempt to predict exact future stock prices. The focus is historical risk analysis, transparent methodology, and professional project structure.

## Project Goal

The platform is being built for a fictional portfolio risk analyst who wants to understand asset performance, downside risk, and cross-asset relationships before moving into market regime classification.

Current outputs include:

- Cleaned historical price data
- Daily and logarithmic returns
- Total and annualized return
- Annualized volatility
- Sharpe Ratio
- Maximum Drawdown
- Historical Value at Risk
- Expected Shortfall
- Asset correlation matrix
- Markdown reports explaining the methodology and results

## Current Progress

Implemented so far:

- Config-driven asset universe and date range
- Historical market data download using `yfinance`
- Raw and processed CSV data outputs
- Data cleaning and validation pipeline
- Daily and log return calculation
- Returns summary report
- Risk metrics module
- Correlation matrix generation
- Risk metrics report
- Unit tests for selected core risk calculations

The current version already demonstrates a working end-to-end analysis pipeline from market data ingestion to risk reporting.

## What This Project Demonstrates

- Python data pipeline development
- pandas-based data cleaning and transformation
- Financial return and risk metric calculation
- Reproducible project structure
- Defensive validation for data quality
- Report generation for transparent analysis
- Basic automated testing with `pytest`
- A structured roadmap toward machine learning and dashboard development

## Tech Stack

- Python
- pandas
- NumPy
- yfinance
- pytest
- Markdown reports

Planned additions:

- scikit-learn
- Streamlit
- Plotly or matplotlib

## Repository Highlights

- Source code is organized into data processing, return calculation, and risk analytics modules.
- Generated CSV outputs are stored under `data/`.
- Markdown reports are stored under `reports/`.
- Tests are stored under `tests/`.

## Next Steps

Next features to implement:

1. Add rolling volatility, momentum, drawdown, and trend features.
2. Create rule-based market regime labels such as bullish, bearish, volatile, and sideways.
3. Train a baseline machine learning classifier for regime detection.
4. Evaluate model performance with F1-score, confusion matrix, and clear limitations.
5. Build a Streamlit dashboard for interactive portfolio and regime analysis.
6. Expand test coverage for return calculations, validation rules, and risk metrics.
7. Improve documentation with screenshots once the dashboard is available.

## Portfolio Positioning

This project is intended to show the ability to turn an applied finance idea into a structured technical product. It connects financial domain knowledge with Python implementation, data validation, analytical reporting, and a realistic machine learning roadmap.

The current stage is suitable for demonstrating data processing, risk analytics, and software project organization. The next stage will add feature engineering, classification models, and an interactive dashboard to make the project stronger for data science, quantitative analytics, or financial technology roles.
