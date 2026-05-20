import numpy as np
import pandas as pd

from src.config import DATA_PROCESSED_DIR, REPORTS_DIR


PRICES_INPUT_FILE = DATA_PROCESSED_DIR / "prices_clean.csv"
RETURNS_OUTPUT_FILE = DATA_PROCESSED_DIR / "returns.csv"
RETURNS_SUMMARY_FILE = REPORTS_DIR / "returns_summary.md"

REQUIRED_COLUMNS = [
    "Date",
    "Ticker",
    "Adj Close",
]


# Ensures both machine-readable returns and human-readable summaries have valid
# destinations before the pipeline writes artifacts.
def ensure_output_directories() -> None:
    DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)


# Loads the cleaned price dataset produced by the data-cleaning pipeline.
def load_clean_prices(input_file=PRICES_INPUT_FILE) -> pd.DataFrame:
    if not input_file.exists():
        raise FileNotFoundError(f"Clean price file not found: {input_file}")

    data = pd.read_csv(input_file)

    if data.empty:
        raise ValueError("Clean price file is empty.")

    return data


# Validates the price data needed for return calculations. Adjusted close must
# be complete and positive because percentage and log returns are undefined or
# misleading for missing, zero, or negative prices.
def validate_price_data(data: pd.DataFrame) -> None:
    missing_columns = [
        column for column in REQUIRED_COLUMNS if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    if data["Adj Close"].isna().any():
        raise ValueError("Column 'Adj Close' contains missing values.")

    if (data["Adj Close"] <= 0).any():
        raise ValueError("Column 'Adj Close' contains non-positive prices.")


# Calculates simple and log daily returns per ticker from adjusted closing
# prices, producing the feature base for later risk metrics and ML modeling.
def calculate_returns(data: pd.DataFrame) -> pd.DataFrame:
    validate_price_data(data)

    returns_data = data.copy()

    # Sorting within each ticker guarantees that previous-day comparisons use
    # chronological observations rather than the input file order.
    returns_data["Date"] = pd.to_datetime(returns_data["Date"])
    returns_data = returns_data.sort_values(["Ticker", "Date"]).reset_index(drop=True)

    returns_data["Daily Return"] = (
        returns_data.groupby("Ticker")["Adj Close"].pct_change()
    )

    returns_data["Log Return"] = (
        returns_data.groupby("Ticker")["Adj Close"]
        .transform(lambda prices: np.log(prices / prices.shift(1)))
    )

    # The first row per ticker has no previous price, so it cannot have a valid
    # daily or log return.
    returns_data = returns_data.dropna(
        subset=["Daily Return", "Log Return"]
    ).reset_index(drop=True)

    return returns_data


# Creates a compact methodology and descriptive-statistics report that explains
# how returns were calculated and summarizes each asset's historical behavior.
def create_returns_summary(returns_data: pd.DataFrame) -> str:
    summary_rows = []

    for ticker in sorted(returns_data["Ticker"].unique()):
        ticker_data = returns_data[returns_data["Ticker"] == ticker]

        start_date = ticker_data["Date"].min().date()
        end_date = ticker_data["Date"].max().date()

        mean_daily_return = ticker_data["Daily Return"].mean()
        std_daily_return = ticker_data["Daily Return"].std()
        min_daily_return = ticker_data["Daily Return"].min()
        max_daily_return = ticker_data["Daily Return"].max()

        summary_rows.append(
            {
                "Ticker": ticker,
                "Start Date": start_date,
                "End Date": end_date,
                "Rows": len(ticker_data),
                "Mean Daily Return": mean_daily_return,
                "Daily Volatility": std_daily_return,
                "Min Daily Return": min_daily_return,
                "Max Daily Return": max_daily_return,
            }
        )

    summary_df = pd.DataFrame(summary_rows)

    report = [
        "# Returns Summary",
        "",
        "## Methodology",
        "",
        "Daily returns are calculated using adjusted closing prices.",
        "",
        "Simple daily return:",
        "",
        "`Return_t = Price_t / Price_(t-1) - 1`",
        "",
        "Log return:",
        "",
        "`LogReturn_t = ln(Price_t / Price_(t-1))`",
        "",
        "## Summary Table",
        "",
        summary_df.to_markdown(index=False),
        "",
        "## Notes",
        "",
        "- The first observation per ticker is removed because no previous price exists for return calculation.",
        "- Adjusted closing prices are used as the basis for return calculation.",
        "- These returns will be used later for risk metrics, feature engineering and model training.",
    ]

    return "\n".join(report)


# Writes the return series used by future portfolio-risk and modeling stages.
def save_returns(returns_data: pd.DataFrame) -> None:
    ensure_output_directories()
    returns_data.to_csv(RETURNS_OUTPUT_FILE, index=False)
    print(f"Returns saved to: {RETURNS_OUTPUT_FILE}")


# Writes a .md summary so the project has a recruiter-friendly explanation
# of the calculation method and output coverage.
def save_returns_summary(report: str) -> None:
    ensure_output_directories()
    RETURNS_SUMMARY_FILE.write_text(report, encoding="utf-8")
    print(f"Returns summary saved to: {RETURNS_SUMMARY_FILE}")


# Runs the complete returns stage: load cleaned prices, calculate return
# features, save the dataset, and generate the methodology report.
def run_returns_pipeline() -> pd.DataFrame:
    print("Loading cleaned price data...")
    price_data = load_clean_prices()

    print("Calculating returns...")
    returns_data = calculate_returns(price_data)

    print("Saving returns...")
    save_returns(returns_data)

    print("Creating returns summary...")
    report = create_returns_summary(returns_data)
    save_returns_summary(report)

    print("Returns pipeline completed.")
    print(f"Rows: {len(returns_data)}")
    print(f"Tickers: {sorted(returns_data['Ticker'].unique())}")

    return returns_data


if __name__ == "__main__":
    run_returns_pipeline()
