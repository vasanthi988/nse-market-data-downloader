
from pathlib import Path

# Project folders
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"

# NSE market-data pages

# NSE market-data pages and their data API endpoints
DATASETS = {
    "top-gainers-losers": {
        "url": "https://www.nseindia.com/market-data/top-gainers-losers",
        "api_url": "https://www.nseindia.com/api/live-analysis-variations?index=gainers",
        "filename": "top-gainers-losers",
    },
    
"upper-band-hitters": {
    "url": "https://www.nseindia.com/market-data/upper-band-hitters",
    "api_url": "https://www.nseindia.com/api/live-analysis-price-band-hitter",
    "filename": "upper-band-hitters",
},
    "volume-gainers-spurts": {
        "url": "https://www.nseindia.com/market-data/volume-gainers-spurts",
        "api_url": "https://www.nseindia.com/api/live-analysis-volume-gainers",
        "filename": "volume-gainers-spurts",
    },
"52-week-high-equity-market": {
    "url": "https://www.nseindia.com/market-data/52-week-high-equity-market",
    "api_url": "https://www.nseindia.com/api/live-analysis-data-52weekhighstock",
    "filename": "52-week-high-equity-market",
},

}

REQUEST_TIMEOUT = 30
MAX_RETRIES = 3
