
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
    "Accept": "application/json,text/plain,*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.nseindia.com/",
}


def create_session():
    """Create and initialize an NSE HTTP session."""
    session = requests.Session()
    session.headers.update(HEADERS)

    try:
        response = session.get(
            "https://www.nseindia.com/",
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
    except requests.RequestException:
        session.close()
        logger.exception("Could not initialize NSE session")
        raise

    logger.info("NSE session initialized successfully")
    return session


def fetch_url(session, url, dataset_name):
    """Fetch one API URL with retries."""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = session.get(url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()

            content_type = response.headers.get("Content-Type", "")

            if "json" not in content_type.lower():
                raise ValueError(
                    f"{dataset_name}: Expected JSON, got {content_type}"
                )

            response.json()

            logger.info(
                "%s: API request successful (HTTP %s)",
                dataset_name,
                response.status_code,
            )
            return response

        except (requests.RequestException, ValueError):
            logger.warning(
                "%s attempt %s/%s failed",
                dataset_name,
                attempt,
                MAX_RETRIES,
                exc_info=True,
            )

            if attempt == MAX_RETRIES:
                raise

            time.sleep(2 ** attempt)

    raise RuntimeError(f"{dataset_name}: API request failed")


def fetch_page(session, dataset_name):
    """Fetch the configured dataset from its API endpoint."""
    if dataset_name not in DATASETS:
        raise ValueError(f"Unknown dataset: {dataset_name}")

    if dataset_name == "top-gainers-losers":
        urls = [
            "https://www.nseindia.com/api/live-analysis-variations?index=gainers",
            "https://www.nseindia.com/api/live-analysis-variations?index=loosers",
        ]

        responses = []
        for url in urls:
            responses.append(
                fetch_url(session, url, dataset_name)
            )

        return responses

    url = DATASETS[dataset_name].get(
        "api_url",
        DATASETS[dataset_name]["url"],
    )

    return fetch_url(session, url, dataset_name)
