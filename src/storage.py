
import csv
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def save_records(records, filename, output_dir="data"):
    """Validate and save dictionary records to a CSV file."""
    if not isinstance(records, list):
        raise ValueError("Expected records to be a list.")

    if not all(isinstance(record, dict) for record in records):
        raise ValueError("Every record must be a dictionary.")

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    file_path = output_path / filename

    if not records:
        if file_path.exists():
            file_path.unlink()
        logger.warning("No records returned for %s", filename)
        return 0

    columns = list(
        dict.fromkeys(
            key for record in records for key in record.keys()
        )
    )

    if not columns:
        raise ValueError(f"No columns found in {filename}")

    with file_path.open(
        "w", newline="", encoding="utf-8-sig"
    ) as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=columns)
        writer.writeheader()

        for record in records:
            row = {}
            for key in columns:
                value = record.get(key, "")
                if isinstance(value, (dict, list)):
                    value = json.dumps(value, ensure_ascii=False)
                row[key] = value
            writer.writerow(row)

    with file_path.open(
        "r", newline="", encoding="utf-8-sig"
    ) as csv_file:
        actual_count = max(
            sum(1 for _ in csv.reader(csv_file)) - 1, 0
        )

    if actual_count != len(records):
        raise IOError(
            f"CSV row count mismatch for {filename}: "
            f"expected {len(records)}, found {actual_count}"
        )

    logger.info("Saved %s records to %s", actual_count, file_path)
    return actual_count
