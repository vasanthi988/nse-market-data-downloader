
import csv
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def save_records(records, filename, output_dir="data"):
    """Save a list of dictionaries to a CSV file."""
    if not isinstance(records, list):
        raise ValueError("Expected records to be a list.")

    if not all(isinstance(record, dict) for record in records):
        raise ValueError("Every record must be a dictionary.")

    if not records:
        logger.warning("No records to save for %s", filename)
        return 0

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    file_path = output_path / filename
    fieldnames = list(
        dict.fromkeys(
            key for record in records for key in record.keys()
        )
    )

    with file_path.open(
        "w", newline="", encoding="utf-8-sig"
    ) as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=fieldnames,
            extrasaction="ignore",
        )
        writer.writeheader()
        writer.writerows(records)

    logger.info("Saved %s records to %s", len(records), file_path)
    return len(records)
