
from pathlib import Path

# Project folders
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"

# NSE market-data pages
DATASETS = {
    "top-gainers-losers": {
        "url": "https://www.nseindia.com/market-data/top-gainers-losers",
        "filename": "top-gainers-losers",
    },
    "upper-band-hitters": {
        "url": "https://www.nseindia.com/market-data/upper-band-hitters",
        "filename": "upper-band-hitters",
    },
    "volume-gainers-spurts": {
        "url": "https://www.nseindia.com/market-data/volume-gainers-spurts",
        "filename": "volume-gainers-spurts",
    },
    "52-week-high-equity-market": {
        "url": "https://www.nseindia.com/market-data/52-week-high-equity-market",
        "filename": "52-week-high-equity-market",
    },
}

REQUEST_TIMEOUT = 30
MAX_RETRIES = 3