
import logging
import time

import requests

from src.config import DATASETS, REQUEST_TIMEOUT, MAX_RETRIES

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/json,"
        "application/xml;q=0.9,*/*;q=0.8"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.nseindia.com/",
}


def create_session():
    """Initialize an HTTP session for NSE requests."""
    session = requests.Session()
    session.headers.update(HEADERS)

    try:
        response = session.get(
            "https://www.nseindia.com/",
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
    except requests.RequestException:
        logger.exception("Could not initialize NSE session")
        session.close()
        raise

    logger.info("NSE session initialized successfully")
    return session


def fetch_page(session, dataset_name):
    """Fetch a configured NSE page with retries."""
    if dataset_name not in DATASETS:
        raise ValueError(f"Unknown dataset: {dataset_name}")

    url = DATASETS[dataset_name]["url"]

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = session.get(
                url,
                timeout=REQUEST_TIMEOUT,
            )
            response.raise_for_status()

            if not response.text.strip():
                raise ValueError("Empty response received")

            logger.info(
                "%s: HTTP %s, content type: %s",
                dataset_name,
                response.status_code,
                response.headers.get("Content-Type", "unknown"),
            )
            return response

        except (requests.RequestException, ValueError):
            logger.exception(
                "%s attempt %s/%s failed",
                dataset_name,
                attempt,
                MAX_RETRIES,
            )

            if attempt == MAX_RETRIES:
                raise

            time.sleep(2 ** attempt)

    raise RuntimeError(f"Failed to fetch {dataset_name}")
