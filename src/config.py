from pathlib import Path

# Shared project paths keep the data pipeline independent of the current
# terminal location and make generated files land in predictable folders.
PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_RAW_DIR = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

REPORTS_DIR = PROJECT_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"

START_DATE = "2018-01-01"
END_DATE = None

# Risk metric assumptions used to annualize daily returns and calculate
# risk-adjusted performance consistently across the project.
TRADING_DAYS_PER_YEAR = 252
RISK_FREE_RATE = 0.0

# Initial portfolio universe used throughout the MVP for market data download,
# return calculation, and later risk analytics.
ASSETS = {
    "AAPL": "Apple",
    "MSFT": "Microsoft",
    "SAP.DE": "SAP",
    "DB1.DE": "Deutsche Boerse",
    "^GSPC": "S&P 500",
    "^GDAXI": "DAX",
}
