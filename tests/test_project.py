
import csv
import logging

import pytest

from src.downloader import fetch_page
from download_nse_data import save_csv


def test_fetch_page_rejects_unknown_dataset():
    """Unknown dataset names should raise a clear error."""
    with pytest.raises(ValueError, match="Unknown dataset"):
        fetch_page(None, "unknown-dataset")


def test_save_csv_writes_records(tmp_path, monkeypatch):
    """Records should be saved correctly to a CSV file."""
    monkeypatch.setattr("download_nse_data.OUTPUT_DIR", tmp_path)

    records = [
        {"symbol": "ABC", "price": 100},
        {"symbol": "XYZ", "price": 200},
    ]

    count = save_csv("sample.csv", records)

    assert count == 2

    output_file = tmp_path / "sample.csv"
    assert output_file.exists()

    with output_file.open(
        "r", encoding="utf-8-sig", newline=""
    ) as file:
        rows = list(csv.DictReader(file))

    assert len(rows) == 2
    assert rows[0]["symbol"] == "ABC"
    assert rows[1]["price"] == "200"


def test_save_csv_rejects_non_list_records(tmp_path, monkeypatch):
    """Invalid input should raise ValueError."""
    monkeypatch.setattr("download_nse_data.OUTPUT_DIR", tmp_path)

    with pytest.raises(ValueError, match="Expected a list"):
        save_csv("invalid.csv", {"symbol": "ABC"})


def test_save_csv_rejects_invalid_record(tmp_path, monkeypatch):
    """Every record must be a dictionary."""
    monkeypatch.setattr("download_nse_data.OUTPUT_DIR", tmp_path)

    with pytest.raises(ValueError, match="Invalid record format"):
        save_csv("invalid.csv", [{"symbol": "ABC"}, "invalid"])


def test_save_csv_handles_empty_records(tmp_path, monkeypatch, caplog):
    """Empty data should return zero and remove an old file."""
    monkeypatch.setattr("download_nse_data.OUTPUT_DIR", tmp_path)

    output_file = tmp_path / "sample.csv"
    output_file.write_text("symbol\nOLD\n", encoding="utf-8")

    with caplog.at_level(logging.WARNING):
        count = save_csv("sample.csv", [])

    assert count == 0
    assert not output_file.exists()
    assert "No records returned" in caplog.text
from src.storage import save_records
from src.validator import validate_records


def test_save_records_writes_csv(tmp_path):
    records = [
        {"symbol": "ABC", "price": 100},
        {"symbol": "XYZ", "price": 200},
    ]

    count = save_records(records, "sample.csv", tmp_path)

    assert count == 2
    assert (tmp_path / "sample.csv").exists()


def test_validate_records_passes_valid_data():
    records = [
        {"symbol": "ABC", "price": 100.0},
        {"symbol": "XYZ", "price": 200.0},
    ]

    result = validate_records(records, required_fields=["symbol"])

    assert result["passed"] is True
    assert result["total_records"] == 2


def test_validate_records_detects_duplicate_symbols():
    records = [
        {"symbol": "ABC"},
        {"symbol": "ABC"},
    ]

    result = validate_records(records)

    assert result["duplicate_records"] == 1
    assert result["passed"] is False
