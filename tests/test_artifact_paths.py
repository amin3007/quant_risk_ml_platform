from src.config import DATA_PROCESSED_DIR, REPORTS_DIR
from src.data.clean_data import (
    DATA_QUALITY_REPORT_FILE,
    PROCESSED_OUTPUT_FILE,
)
from src.features.returns import (
    RETURNS_OUTPUT_FILE,
    RETURNS_SUMMARY_FILE,
)
from src.risk.metrics import (
    RISK_METRICS_OUTPUT_FILE,
    CORRELATION_OUTPUT_FILE,
    RISK_REPORT_FILE,
)


def test_processed_csv_outputs_are_under_data_processed():
    assert PROCESSED_OUTPUT_FILE.parent == DATA_PROCESSED_DIR
    assert RETURNS_OUTPUT_FILE.parent == DATA_PROCESSED_DIR
    assert RISK_METRICS_OUTPUT_FILE.parent == DATA_PROCESSED_DIR
    assert CORRELATION_OUTPUT_FILE.parent == DATA_PROCESSED_DIR


def test_report_outputs_are_under_reports_dir():
    assert DATA_QUALITY_REPORT_FILE.parent == REPORTS_DIR
    assert RETURNS_SUMMARY_FILE.parent == REPORTS_DIR
    assert RISK_REPORT_FILE.parent == REPORTS_DIR


def test_data_quality_report_is_written_to_project_reports_dir():
    assert DATA_QUALITY_REPORT_FILE == REPORTS_DIR / "data_quality_report.md"