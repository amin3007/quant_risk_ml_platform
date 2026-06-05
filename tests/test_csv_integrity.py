import pandas as pd
import pytest

from src.config import DATA_PROCESSED_DIR
from src.data.csv_integrity import (
    CsvIntegrityError,
    read_validate_csv,
    write_csv_checked,
)
from src.features.returns import RETURNS_REQUIRED_COLUMNS


def test_malformed_csv_is_rejected(tmp_path):
    csv_file = tmp_path / "broken.csv"
    csv_file.write_text("a,b\n1,2\n3,4,5\n", encoding="utf-8")

    with pytest.raises(CsvIntegrityError, match="malformed"):
        read_validate_csv(csv_file)


def test_missing_required_columns_are_rejected(tmp_path):
    csv_file = tmp_path / "missing_columns.csv"
    csv_file.write_text("Date,Ticker\n2024-01-01,AAPL\n", encoding="utf-8")

    with pytest.raises(CsvIntegrityError, match="missing required columns"):
        read_validate_csv(
            csv_file,
            required_columns=["Date", "Ticker", "Daily Return"],
        )


def test_write_csv_checked_creates_parseable_csv(tmp_path):
    csv_file = tmp_path / "returns.csv"

    data = pd.DataFrame(
        {
            "Date": ["2024-01-02"],
            "Ticker": ["AAPL"],
            "Adj Close": [101.0],
            "Daily Return": [0.01],
            "Log Return": [0.00995],
        }
    )

    write_csv_checked(
        data,
        csv_file,
        required_columns=RETURNS_REQUIRED_COLUMNS,
    )

    loaded = read_validate_csv(
        csv_file,
        required_columns=RETURNS_REQUIRED_COLUMNS,
    )

    assert loaded.shape == (1, 5)


def test_processed_returns_csv_is_readable():
    returns_file = DATA_PROCESSED_DIR / "returns.csv"

    loaded = read_validate_csv(
        returns_file,
        required_columns=RETURNS_REQUIRED_COLUMNS,
    )

    assert not loaded.empty