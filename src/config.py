from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_RAW_DIR = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

START_DATE = "2018-01-01"
END_DATE = None

ASSETS = {
    "AAPL": "Apple",
    "MSFT": "Microsoft",
    "SAP.DE": "SAP",
    "DB1.DE": "Deutsche Boerse",
    "^GSPC": "S&P 500",
    "^GDAXI": "DAX",
}