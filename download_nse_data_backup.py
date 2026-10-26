
import csv
import json
import logging

from src.logger_config import setup_logging
from datetime import datetime
from pathlib import Path

from requests.exceptions import RequestException
from src.downloader import create_session

BASE_URL = "https://www.nseindia.com"
OUTPUT_DIR = Path("data")
TIMEOUT = 30

ENDPOINTS = {
    "top-gainers": "/api/live-analysis-variations?index=gainers",
    "top-losers": "/api/live-analysis-variations?index=loosers",
    "upper-band-hitters": "/api/live-analysis-price-band-hitter",
    "volume-gainers": "/api/live-analysis-volume-gainers",
    "52-week-high": "/api/live-analysis-data-52weekhighstock",
}

setup_logging()


def save_csv(filename, records):
    """Save records and return the actual number of CSV data rows."""
    if not isinstance(records, list):
        raise ValueError(f"Expected a list of records: {filename}")

    filepath = OUTPUT_DIR / filename

    if not records:
        # Remove stale data so an old file isn't mistaken for fresh data.
        if filepath.exists():
            filepath.unlink()
        logging.warning("No records returned for %s", filename)
        return 0

    if not all(isinstance(record, dict) for record in records):
        raise ValueError(f"Invalid record format in {filename}")

    columns = list(dict.fromkeys(
        key for record in records for key in record.keys()
    ))

    if not columns:
        raise ValueError(f"No columns found in {filename}")

    with filepath.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()

        for record in records:
            row = {}
            for key in columns:
                value = record.get(key, "")
                if isinstance(value, (dict, list)):
                    value = json.dumps(value, ensure_ascii=False)
                row[key] = value
            writer.writerow(row)

    # Verify the number of rows actually written.
    with filepath.open("r", newline="", encoding="utf-8-sig") as file:
        actual_count = max(sum(1 for _ in csv.reader(file)) - 1, 0)

    if actual_count != len(records):
        raise IOError(
            f"CSV row count mismatch for {filename}: "
            f"expected {len(records)}, found {actual_count}"
        )

    logging.info("Saved %s records -> %s", actual_count, filepath)
    return actual_count


def save_gainers_losers(dataset_name, payload):
    """Save each gainers/losers category separately."""
    if not isinstance(payload, dict):
        raise ValueError("Expected a JSON object for gainers/losers")

    saved = []

    for category, details in payload.items():
        if not isinstance(details, dict) or "data" not in details:
            continue

        records = details["data"]
        if not isinstance(records, list):
            raise ValueError(f"Invalid data list for category {category}")

        if records:
            filename = f"{dataset_name}_{category.lower()}.csv"
            count = save_csv(filename, records)
            saved.append({"file": filename, "records": count})

    if not saved:
        raise ValueError(f"No records found for {dataset_name}")

    return saved


def save_upper_band(payload):
    """Save upper, lower, and both price-band categories."""
    if not isinstance(payload, dict):
        raise ValueError("Expected a JSON object for upper-band data")

    saved = []

    for band_type in ("upper", "lower", "both"):
        band = payload.get(band_type, {})
        if not isinstance(band, dict):
            continue

        for category, details in band.items():
            if not isinstance(details, dict) or "data" not in details:
                continue

            records = details["data"]
            if not isinstance(records, list):
                raise ValueError(
                    f"Invalid records for {band_type}/{category}"
                )

            if records:
                filename = (
                    f"upper-band-{band_type}_{category.lower()}.csv"
                )
                count = save_csv(filename, records)
                saved.append({"file": filename, "records": count})

    if not saved:
        raise ValueError("No upper-band records found")

    return saved


def fetch_json(session, endpoint):
    """Fetch an API response and validate its JSON structure."""
    response = session.get(
        BASE_URL + endpoint,
        headers={
            "Referer": BASE_URL + "/",
            "Accept": "application/json, text/plain, */*",
        },
        timeout=TIMEOUT,
    )
    response.raise_for_status()

    try:
        payload = response.json()
    except ValueError as exc:
        preview = response.text[:160].replace("\n", " ")
        raise ValueError(
            f"Invalid JSON response. Preview: {preview}"
        ) from exc

    if not isinstance(payload, dict):
        raise ValueError("Expected the API response to be a JSON object")

    return payload


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    session = create_session()
    run_time = datetime.now().astimezone().isoformat(timespec="seconds")
    summary = []

    # Initialize the NSE session.
    try:
        response = session.get(BASE_URL, timeout=TIMEOUT)
        response.raise_for_status()
        logging.info("NSE homepage status: %s", response.status_code)

    except RequestException as exc:
        logging.error("Could not initialize NSE session: %s", exc)

        for name in ENDPOINTS:
            summary.append({
                "dataset": name,
                "status": "FAILED",
                "files": 0,
                "records": 0,
                "error": str(exc),
                "fetched_at": run_time,
            })

        save_csv("download_summary.csv", summary)
        return

    for name, endpoint in ENDPOINTS.items():
        logging.info("Downloading dataset: %s", name)

        try:
            payload = fetch_json(session, endpoint)

            if name in ("top-gainers", "top-losers"):
                saved_files = save_gainers_losers(name, payload)

            elif name == "upper-band-hitters":
                saved_files = save_upper_band(payload)

            else:
                records = payload.get("data")
                if not isinstance(records, list):
                    raise ValueError(
                        "Expected a list in the API 'data' field"
                    )

                filename = f"{name}.csv"
                count = save_csv(filename, records)
                saved_files = [{"file": filename, "records": count}]

            file_count = len(saved_files)
            record_count = sum(
                item["records"] for item in saved_files
            )

            summary.append({
                "dataset": name,
                "status": "SUCCESS",
                "files": file_count,
                "records": record_count,
                "error": "",
                "fetched_at": run_time,
            })

            logging.info(
                "%s completed: %s files, %s records",
                name, file_count, record_count
            )

        except Exception as exc:
            # One failed endpoint should not stop the remaining downloads.
            logging.exception("Failed to download %s", name)

            summary.append({
                "dataset": name,
                "status": "FAILED",
                "files": 0,
                "records": 0,
                "error": str(exc),
                "fetched_at": run_time,
            })

    try:
        save_csv("download_summary.csv", summary)
    except (OSError, ValueError) as exc:
        logging.exception("Could not save summary: %s", exc)

    logging.info("Download process completed.")
    logging.info("Output directory: %s", OUTPUT_DIR.resolve())


if __name__ == "__main__":
    main()