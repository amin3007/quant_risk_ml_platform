from pathlib import Path

import pandas as pd
import yfinance as yf

from src.config import ASSETS, DATA_RAW_DIR, START_DATE, END_DATE


RAW_OUTPUT_FILE = DATA_RAW_DIR / "prices_raw.csv"


# Creates parent folders before writing pipeline outputs to disk.
def ensure_output_directory(path: Path) -> None:
    """
    Ensures that the output directory exists.
    """
    path.mkdir(parents=True, exist_ok=True)


def download_market_data(
    tickers: list[str],
    start_date: str,
    end_date: str | None = None,
) -> pd.DataFrame:
    """
    Downloads historical OHLCV market data for multiple tickers.

    Parameters:
        tickers: List of ticker symbols.
        start_date: Start date in YYYY-MM-DD format.
        end_date: Optional end date in YYYY-MM-DD format.

    Returns:
        Raw yfinance DataFrame with MultiIndex columns.
    """
    # Empty ticker input is a data-quality issue because yfinance would return
    # no useful market history for the downstream pipeline.
    if not tickers:
        raise ValueError("Ticker list must not be empty.")

    # yfinance returns one column group per ticker; normalization below converts
    # that vendor-specific shape into a project-friendly tabular format.
    data = yf.download(
        tickers=tickers,
        start=start_date,
        end=end_date,
        group_by="ticker",
        auto_adjust=False,
        threads=True,
        progress=False,
    )

    # Failing fast here prevents later cleaning steps from producing misleading
    # empty CSV files when the date range or ticker symbols are invalid.
    if data.empty:
        raise ValueError("No market data was downloaded. Check tickers or date range.")

    return data


def normalize_market_data(raw_data: pd.DataFrame, tickers: list[str]) -> pd.DataFrame:
    """
    Converts yfinance output into a clean long-format DataFrame.

    Output columns:
        Date, Ticker, Open, High, Low, Close, Adj Close, Volume
    """
    normalized_frames = []

    # Each ticker is extracted independently so a missing or malformed asset can
    # be skipped without discarding all successfully downloaded market data.
    for ticker in tickers:
        if ticker not in raw_data.columns.get_level_values(0):
            print(f"Warning: No data found for ticker {ticker}. Skipping.")
            continue

        ticker_data = raw_data[ticker].copy()
        ticker_data = ticker_data.reset_index()
        ticker_data["Ticker"] = ticker

        expected_columns = [
            "Date",
            "Ticker",
            "Open",
            "High",
            "Low",
            "Close",
            "Adj Close",
            "Volume",
        ]

        missing_columns = [
            column for column in expected_columns if column not in ticker_data.columns
        ]

        # The downstream cleaning and return calculations rely on this exact
        # schema, especially adjusted close prices for total-return accuracy.
        if missing_columns:
            print(
                f"Warning: Ticker {ticker} is missing columns: {missing_columns}. "
                "Skipping."
            )
            continue

        ticker_data = ticker_data[expected_columns]
        normalized_frames.append(ticker_data)

    if not normalized_frames:
        raise ValueError("No ticker data could be normalized.")

    normalized_data = pd.concat(normalized_frames, ignore_index=True)

    normalized_data["Date"] = pd.to_datetime(normalized_data["Date"])
    normalized_data = normalized_data.sort_values(["Ticker", "Date"]).reset_index(
        drop=True
    )

    return normalized_data


# Persists the normalized raw market data as the first reproducible pipeline
# artifact before cleaning and feature calculations are applied.
def save_raw_data(data: pd.DataFrame, output_file: Path) -> None:
    """
    Saves downloaded market data as CSV.
    """
    ensure_output_directory(output_file.parent)
    data.to_csv(output_file, index=False)
    print(f"Raw market data saved to: {output_file}")


def fetch_and_save_market_data() -> pd.DataFrame:
    """
    Main pipeline function:
    1. Reads tickers from config.
    2. Downloads market data.
    3. Normalizes the output.
    4. Saves the raw long-format CSV.
    """
    # The config dictionary is the single source of truth for the MVP asset
    # universe, keeping data download aligned with later analytics.
    tickers = list(ASSETS.keys())

    print("Starting market data download...")
    print(f"Tickers: {tickers}")
    print(f"Start date: {START_DATE}")
    print(f"End date: {END_DATE if END_DATE else 'latest available'}")

    raw_data = download_market_data(
        tickers=tickers,
        start_date=START_DATE,
        end_date=END_DATE,
    )

    normalized_data = normalize_market_data(raw_data, tickers)

    save_raw_data(normalized_data, RAW_OUTPUT_FILE)

    print("Market data download completed.")
    print(f"Rows: {len(normalized_data)}")
    print(f"Tickers downloaded: {normalized_data['Ticker'].nunique()}")

    return normalized_data


if __name__ == "__main__":
    fetch_and_save_market_data()
