# Quantitative Risk & ML Portfolio Intelligence Platform

## 1. Project Goal

This project analyzes historical financial market data, computes quantitative risk metrics and uses machine learning to classify market regimes in order to support portfolio risk analysis.

The focus is not on predicting exact future stock prices, but on risk analytics, market regime classification and transparent model evaluation.

## 2. Main Research Question

Can historical return, volatility, momentum and drawdown features be used to classify financial market regimes and support portfolio risk analysis?

## 3. Target User

The platform is designed for a fictional financial analyst or portfolio risk team that wants to understand asset performance, portfolio risk and historical market regimes.

## 4. MVP Scope

Version 1 includes:

- loading historical market data
- cleaning and transforming price data
- calculating daily returns
- calculating volatility, Sharpe Ratio, Maximum Drawdown and Value at Risk
- creating correlation analysis
- defining rule-based market regime labels
- training a machine learning classifier
- evaluating the model with classification metrics
- visualizing results in a Streamlit dashboard
- documenting methodology and limitations

## 5. Out of Scope for Version 1

Version 1 does not include:

- real trading
- financial advice
- live trading
- exact stock price prediction
- deep learning
- cloud deployment
- complex portfolio optimization
- production-grade risk management

## 6. Selected Assets

Initial asset universe:

- Apple
- Microsoft
- SAP
- Deutsche Börse
- S&P 500
- DAX
- MSCI World ETF optional

Initial time period:

- 2018-01-01 to present

## 7. Market Regime Classes

The project uses the following market regime labels:

- bullish
- bearish
- volatile
- sideways

The labels are rule-based and derived from return, volatility and drawdown thresholds.

## 8. Success Criteria

Version 1 is considered successful when:

- historical market data can be loaded and processed
- risk metrics are computed correctly
- market regimes are generated
- at least one baseline model and one stronger classifier are trained
- model performance is evaluated using F1-score and confusion matrix
- results are visible in a Streamlit dashboard
- the README explains the methodology, architecture and limitations
- core calculations are covered by tests

## 9. Technology Stack

Version 1 uses:

- Python
- pandas
- NumPy
- scikit-learn
- Plotly or matplotlib
- Streamlit
- pytest
- Git and GitHub

Optional later extensions:

- FastAPI
- Docker
- GitHub Actions
- MLflow
- statsmodels

## 10. Project Positioning

This project is positioned as a quantitative finance and machine learning portfolio project.

It demonstrates:

- Python programming
- data analysis
- feature engineering
- machine learning classification
- financial risk analysis
- model evaluation
- dashboard development
- software project structure