from pathlib import Path

import pandas as pd

from src.config import DATA_RAW_DIR, DATA_PROCESSED_DIR


RAW_INPUT_FILE = DATA_RAW_DIR / "prices_raw.csv"
PROCESSED_OUTPUT_FILE = DATA_PROCESSED_DIR / "prices_clean.csv"

REQUIRED_COLUMNS = [
    "Date",
    "Ticker",
    "Open",
    "High",
    "Low",
    "Close",
    "Adj Close",
    "Volume",
]

NUMERIC_COLUMNS = [
    "Open",
    "High",
    "Low",
    "Close",
    "Adj Close",
    "Volume",
]


def ensure_output_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def load_raw_data(input_file: Path) -> pd.DataFrame:
    if not input_file.exists():
        raise FileNotFoundError(f"Raw data file not found: {input_file}")

    data = pd.read_csv(input_file)

    if data.empty:
        raise ValueError("Raw data file is empty.")

    return data


def validate_required_columns(data: pd.DataFrame) -> None:
    missing_columns = [
        column for column in REQUIRED_COLUMNS if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")


def clean_market_data(data: pd.DataFrame) -> pd.DataFrame:
    validate_required_columns(data)

    cleaned_data = data.copy()

    cleaned_data["Date"] = pd.to_datetime(cleaned_data["Date"], errors="coerce")

    for column in NUMERIC_COLUMNS:
        cleaned_data[column] = pd.to_numeric(cleaned_data[column], errors="coerce")

    cleaned_data = cleaned_data.dropna(subset=["Date", "Ticker", "Adj Close"])

    cleaned_data = cleaned_data.drop_duplicates(
        subset=["Date", "Ticker"],
        keep="last",
    )

    cleaned_data = cleaned_data.sort_values(
        by=["Ticker", "Date"],
    ).reset_index(drop=True)

    cleaned_data[NUMERIC_COLUMNS] = cleaned_data.groupby("Ticker")[NUMERIC_COLUMNS].ffill()

    cleaned_data = cleaned_data.dropna(subset=NUMERIC_COLUMNS)

    cleaned_data = cleaned_data[REQUIRED_COLUMNS]

    return cleaned_data


def create_data_quality_report(raw_data: pd.DataFrame, cleaned_data: pd.DataFrame) -> str:
    raw_rows = len(raw_data)
    cleaned_rows = len(cleaned_data)
    removed_rows = raw_rows - cleaned_rows

    tickers = sorted(cleaned_data["Ticker"].unique())

    missing_values = cleaned_data.isna().sum()

    report = [
        "# Data Quality Report",
        "",
        "## Summary",
        "",
        f"- Raw rows: {raw_rows}",
        f"- Cleaned rows: {cleaned_rows}",
        f"- Removed rows: {removed_rows}",
        f"- Number of tickers: {len(tickers)}",
        f"- Tickers: {', '.join(tickers)}",
        "",
        "## Date Range per Ticker",
        "",
    ]

    for ticker in tickers:
        ticker_data = cleaned_data[cleaned_data["Ticker"] == ticker]
        min_date = ticker_data["Date"].min().date()
        max_date = ticker_data["Date"].max().date()
        row_count = len(ticker_data)

        report.append(f"- {ticker}: {min_date} to {max_date}, rows: {row_count}")

    report.extend(
        [
            "",
            "## Missing Values After Cleaning",
            "",
        ]
    )

    for column, count in missing_values.items():
        report.append(f"- {column}: {count}")

    return "\n".join(report)


def save_cleaned_data(data: pd.DataFrame, output_file: Path) -> None:
    ensure_output_directory(output_file.parent)
    data.to_csv(output_file, index=False)
    print(f"Cleaned market data saved to: {output_file}")


def save_quality_report(report: str) -> None:
    reports_dir = Path("reports")
    ensure_output_directory(reports_dir)

    output_file = reports_dir / "data_quality_report.md"
    output_file.write_text(report, encoding="utf-8")

    print(f"Data quality report saved to: {output_file}")


def run_cleaning_pipeline() -> pd.DataFrame:
    print("Loading raw market data...")
    raw_data = load_raw_data(RAW_INPUT_FILE)

    print("Cleaning market data...")
    cleaned_data = clean_market_data(raw_data)

    print("Saving cleaned market data...")
    save_cleaned_data(cleaned_data, PROCESSED_OUTPUT_FILE)

    print("Creating data quality report...")
    report = create_data_quality_report(raw_data, cleaned_data)
    save_quality_report(report)

    print("Cleaning pipeline completed.")
    print(f"Rows before cleaning: {len(raw_data)}")
    print(f"Rows after cleaning: {len(cleaned_data)}")
    print(f"Tickers: {sorted(cleaned_data['Ticker'].unique())}")

    return cleaned_data


if __name__ == "__main__":
    run_cleaning_pipeline()