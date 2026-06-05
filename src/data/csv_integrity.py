from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd


class CsvIntegrityError(ValueError):
    """Raised when a CSV artifact is not readable or violates its schema contract."""


def read_validate_csv(
    path: Path | str,
    required_columns: Iterable[str] | None = None,
    allow_empty: bool = False,
) -> pd.DataFrame:
    csv_path = Path(path)

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file does not exist: {csv_path}")

    try:
        data = pd.read_csv(csv_path)
    except pd.errors.EmptyDataError as exc:
        raise CsvIntegrityError(f"CSV file is empty or has no readable columns: {csv_path}") from exc
    except pd.errors.ParserError as exc:
        raise CsvIntegrityError(f"CSV file is malformed and cannot be parsed: {csv_path}") from exc
    except UnicodeDecodeError as exc:
        raise CsvIntegrityError(f"CSV file has an invalid text encoding: {csv_path}") from exc

    if not allow_empty and data.empty:
        raise CsvIntegrityError(f"CSV file contains no rows: {csv_path}")

    if required_columns is not None:
        missing_columns = [column for column in required_columns if column not in data.columns]
        if missing_columns:
            raise CsvIntegrityError(
                f"CSV file is missing required columns {missing_columns}: {csv_path}"
            )

    unnamed_columns = [
        column for column in data.columns
        if str(column).startswith("Unnamed")
    ]
    if unnamed_columns:
        raise CsvIntegrityError(
            f"CSV file contains unexpected index-like columns {unnamed_columns}. "
            f"Write CSV files with index=False: {csv_path}"
        )

    return data


def assert_csv_readable(
    path: Path | str,
    required_columns: Iterable[str] | None = None,
    allow_empty: bool = False,
) -> None:
    read_validate_csv(
        path=path,
        required_columns=required_columns,
        allow_empty=allow_empty,
    )


def write_csv_checked(
    data: pd.DataFrame,
    path: Path | str,
    required_columns: Iterable[str] | None = None,
    index: bool = False,
) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    temp_path = output_path.with_name(f"{output_path.stem}.tmp{output_path.suffix}")

    try:
        data.to_csv(temp_path, index=index)
        read_validate_csv(temp_path, required_columns=required_columns)
        temp_path.replace(output_path)
        read_validate_csv(output_path, required_columns=required_columns)
    except Exception:
        if temp_path.exists():
            temp_path.unlink()
        raise