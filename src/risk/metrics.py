import numpy as np
import pandas as pd

from src.config import (
    DATA_PROCESSED_DIR,
    REPORTS_DIR,
    TRADING_DAYS_PER_YEAR,
    RISK_FREE_RATE,
)


RETURNS_INPUT_FILE = DATA_PROCESSED_DIR / "returns.csv"
RISK_METRICS_OUTPUT_FILE = DATA_PROCESSED_DIR / "risk_metrics.csv"
CORRELATION_OUTPUT_FILE = DATA_PROCESSED_DIR / "correlation_matrix.csv"
RISK_REPORT_FILE = REPORTS_DIR / "risk_report.md"

REQUIRED_COLUMNS = [
    "Date",
    "Ticker",
    "Adj Close",
    "Daily Return",
]


# Ensures the risk metrics CSV, correlation matrix, and markdown report can be
# written when the pipeline runs on a fresh project checkout.
def ensure_output_directories() -> None:
    DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)


# Loads the returns dataset produced by the return-calculation pipeline.
def load_returns(input_file=RETURNS_INPUT_FILE) -> pd.DataFrame:
    if not input_file.exists():
        raise FileNotFoundError(f"Returns file not found: {input_file}")

    data = pd.read_csv(input_file)

    if data.empty:
        raise ValueError("Returns file is empty.")

    return data


# Enforces the return-data contract needed for risk metrics. Valid adjusted
# close prices and daily returns are required for performance, volatility, and
# downside-risk calculations.
def validate_returns_data(data: pd.DataFrame) -> None:
    missing_columns = [
        column for column in REQUIRED_COLUMNS if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    if data["Daily Return"].isna().any():
        raise ValueError("Column 'Daily Return' contains missing values.")

    if data["Adj Close"].isna().any():
        raise ValueError("Column 'Adj Close' contains missing values.")

    if (data["Adj Close"] <= 0).any():
        raise ValueError("Column 'Adj Close' contains non-positive prices.")


# Calculates the cumulative price return for one ticker over the available
# history, using adjusted close prices to account for splits and dividends.
def calculate_total_return(ticker_data: pd.DataFrame) -> float:
    start_price = ticker_data["Adj Close"].iloc[0]
    end_price = ticker_data["Adj Close"].iloc[-1]

    return end_price / start_price - 1


# Converts the observed total return into an annualized return so assets with
# different history lengths can be compared on the same scale.
def calculate_annualized_return(
    ticker_data: pd.DataFrame,
    trading_days_per_year: int = TRADING_DAYS_PER_YEAR,
) -> float:
    total_return = calculate_total_return(ticker_data)
    number_of_days = len(ticker_data)

    # A zero-length series cannot produce a meaningful annualized result.
    if number_of_days <= 0:
        return np.nan

    return (1 + total_return) ** (trading_days_per_year / number_of_days) - 1


# Annualizes daily return volatility using the square-root-of-time convention
# commonly used in financial risk analysis.
def calculate_annualized_volatility(
    ticker_data: pd.DataFrame,
    trading_days_per_year: int = TRADING_DAYS_PER_YEAR,
) -> float:
    daily_volatility = ticker_data["Daily Return"].std()

    return daily_volatility * np.sqrt(trading_days_per_year)


# Measures historical excess return per unit of annualized volatility under the
# configured risk-free-rate assumption.
def calculate_sharpe_ratio(
    annualized_return: float,
    annualized_volatility: float,
    risk_free_rate: float = RISK_FREE_RATE,
) -> float:
    # A zero or missing volatility would make the Sharpe Ratio undefined.
    if annualized_volatility == 0 or np.isnan(annualized_volatility):
        return np.nan

    return (annualized_return - risk_free_rate) / annualized_volatility


# Calculates the largest historical peak-to-trough decline for one ticker.
def calculate_max_drawdown(ticker_data: pd.DataFrame) -> float:
    cumulative_returns = (1 + ticker_data["Daily Return"]).cumprod()
    running_max = cumulative_returns.cummax()
    drawdowns = cumulative_returns / running_max - 1

    return drawdowns.min()


# Estimates historical Value at Risk from the lower tail of daily returns and
# reports it as a positive loss number for easier comparison in reports.
def calculate_historical_var(
    ticker_data: pd.DataFrame,
    confidence_level: float = 0.95,
) -> float:
    """
    Returns VaR as a positive loss number.

    Example:
        If the 5% return quantile is -0.03,
        the 95% historical VaR is returned as 0.03.
    """
    tail_probability = 1 - confidence_level
    return_quantile = ticker_data["Daily Return"].quantile(tail_probability)

    return -return_quantile


# Calculates the average loss on days beyond the VaR threshold, capturing tail
# severity that VaR alone does not describe.
def calculate_expected_shortfall(
    ticker_data: pd.DataFrame,
    confidence_level: float = 0.95,
) -> float:
    """
    Optional extension:
    Expected Shortfall is the average loss beyond the VaR threshold.
    Returned as a positive loss number.
    """
    tail_probability = 1 - confidence_level
    return_quantile = ticker_data["Daily Return"].quantile(tail_probability)

    tail_losses = ticker_data.loc[
        ticker_data["Daily Return"] <= return_quantile,
        "Daily Return",
    ]

    if tail_losses.empty:
        return np.nan

    return -tail_losses.mean()


# Aggregates the main risk and performance statistics for every ticker in the
# returns dataset, producing the table consumed by reports and dashboards.
def calculate_risk_metrics(data: pd.DataFrame) -> pd.DataFrame:
    validate_returns_data(data)

    risk_rows = []

    data = data.copy()
    data["Date"] = pd.to_datetime(data["Date"])
    data = data.sort_values(["Ticker", "Date"]).reset_index(drop=True)

    # Metrics are calculated per ticker to keep each asset's price path and
    # return distribution independent.
    for ticker in sorted(data["Ticker"].unique()):
        ticker_data = data[data["Ticker"] == ticker].copy()

        total_return = calculate_total_return(ticker_data)
        annualized_return = calculate_annualized_return(ticker_data)
        annualized_volatility = calculate_annualized_volatility(ticker_data)
        sharpe_ratio = calculate_sharpe_ratio(
            annualized_return=annualized_return,
            annualized_volatility=annualized_volatility,
        )
        max_drawdown = calculate_max_drawdown(ticker_data)
        historical_var_95 = calculate_historical_var(ticker_data, confidence_level=0.95)
        historical_var_99 = calculate_historical_var(ticker_data, confidence_level=0.99)
        expected_shortfall_95 = calculate_expected_shortfall(
            ticker_data,
            confidence_level=0.95,
        )

        risk_rows.append(
            {
                "Ticker": ticker,
                "Start Date": ticker_data["Date"].min().date(),
                "End Date": ticker_data["Date"].max().date(),
                "Observations": len(ticker_data),
                "Total Return": total_return,
                "Annualized Return": annualized_return,
                "Annualized Volatility": annualized_volatility,
                "Sharpe Ratio": sharpe_ratio,
                "Maximum Drawdown": max_drawdown,
                "Historical VaR 95": historical_var_95,
                "Historical VaR 99": historical_var_99,
                "Expected Shortfall 95": expected_shortfall_95,
            }
        )

    return pd.DataFrame(risk_rows)


# Builds a ticker-by-ticker return correlation matrix for diversification and
# co-movement analysis.
def calculate_correlation_matrix(data: pd.DataFrame) -> pd.DataFrame:
    validate_returns_data(data)

    returns_pivot = data.pivot_table(
        index="Date",
        columns="Ticker",
        values="Daily Return",
    )

    correlation_matrix = returns_pivot.corr()

    return correlation_matrix


# Creates a markdown report that combines methodology, risk metrics, and
# correlation output in a reviewer-friendly format.
def create_risk_report(
    risk_metrics: pd.DataFrame,
    correlation_matrix: pd.DataFrame,
) -> str:
    report_metrics = risk_metrics.copy()

    percentage_columns = [
        "Total Return",
        "Annualized Return",
        "Annualized Volatility",
        "Maximum Drawdown",
        "Historical VaR 95",
        "Historical VaR 99",
        "Expected Shortfall 95",
    ]

    # Percent formatting keeps the report readable while leaving the saved CSV
    # outputs numeric for future analysis.
    for column in percentage_columns:
        report_metrics[column] = report_metrics[column].map(lambda x: f"{x:.2%}")

    report_metrics["Sharpe Ratio"] = report_metrics["Sharpe Ratio"].map(
        lambda x: f"{x:.2f}" if pd.notna(x) else "n/a"
    )

    report = [
        "# Risk Metrics Report",
        "",
        "## Methodology",
        "",
        f"- Trading days per year assumption: {TRADING_DAYS_PER_YEAR}",
        f"- Risk-free rate assumption: {RISK_FREE_RATE:.2%}",
        "- Daily returns are based on adjusted closing prices.",
        "- VaR is reported as a positive loss number.",
        "- Expected Shortfall is included as an optional downside-risk extension.",
        "",
        "## Risk Metrics",
        "",
        report_metrics.to_markdown(index=False),
        "",
        "## Correlation Matrix",
        "",
        correlation_matrix.round(3).to_markdown(),
        "",
        "## Interpretation Notes",
        "",
        "- Higher annualized return is positive, but it should not be interpreted without volatility and drawdown.",
        "- Higher annualized volatility means stronger historical fluctuation.",
        "- Higher Sharpe Ratio indicates better historical risk-adjusted return under the chosen assumptions.",
        "- More negative Maximum Drawdown indicates a stronger historical loss phase.",
        "- VaR estimates a historical loss threshold, but it does not describe how severe losses beyond that threshold can become.",
        "- Correlation shows linear co-movement between assets and is relevant for diversification analysis.",
    ]

    return "\n".join(report)


# Persists all risk-stage artifacts: numeric metrics, correlation matrix, and
# the markdown explanation report.
def save_outputs(
    risk_metrics: pd.DataFrame,
    correlation_matrix: pd.DataFrame,
    report: str,
) -> None:
    ensure_output_directories()

    risk_metrics.to_csv(RISK_METRICS_OUTPUT_FILE, index=False)
    correlation_matrix.to_csv(CORRELATION_OUTPUT_FILE)
    RISK_REPORT_FILE.write_text(report, encoding="utf-8")

    print(f"Risk metrics saved to: {RISK_METRICS_OUTPUT_FILE}")
    print(f"Correlation matrix saved to: {CORRELATION_OUTPUT_FILE}")
    print(f"Risk report saved to: {RISK_REPORT_FILE}")


# Runs the complete risk analytics stage after returns have been calculated.
def run_risk_metrics_pipeline() -> tuple[pd.DataFrame, pd.DataFrame]:
    print("Loading returns data...")
    returns_data = load_returns()

    print("Calculating risk metrics...")
    risk_metrics = calculate_risk_metrics(returns_data)

    print("Calculating correlation matrix...")
    correlation_matrix = calculate_correlation_matrix(returns_data)

    print("Creating risk report...")
    report = create_risk_report(risk_metrics, correlation_matrix)

    print("Saving outputs...")
    save_outputs(risk_metrics, correlation_matrix, report)

    print("Risk metrics pipeline completed.")
    print(risk_metrics[["Ticker", "Annualized Return", "Annualized Volatility", "Sharpe Ratio", "Maximum Drawdown"]])

    return risk_metrics, correlation_matrix


if __name__ == "__main__":
    run_risk_metrics_pipeline()
