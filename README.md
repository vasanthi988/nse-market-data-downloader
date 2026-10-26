# NSE Market Data Downloader

A Python project that downloads selected market datasets from the National Stock Exchange of India (NSE), saves the data as CSV files, and supports data validation and automated testing.

## Features

- Downloads top gainers and losers.
- Downloads upper-band market data.
- Downloads volume gainers and spurts.
- Downloads 52-week-high equity-market data.
- Handles HTTP requests, retries, and errors.
- Parses JSON responses and removes duplicate records.
- Saves downloaded records to CSV files.
- Includes logging and automated tests.

## Technologies Used

- Python 3.12
- Requests
- Pandas
- CSV and JSON
- Pytest
- Git and GitHub

## Installation

Clone the repository:

```bash
git clone https://github.com/vasanthi988/nse-market-data-downloader.git
cd nse-market-data-downloader
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Run the Downloader

```powershell
python main.py
```

The downloaded CSV files are saved in the `data/` directory.

Expected output filenames:

- `top-gainers-losers.csv`
- `upper-band-hitters.csv`
- `volume-gainers-spurts.csv`
- `52-week-high-equity-market.csv`

The number of records may change depending on the data returned by NSE.

## Run Automated Tests

```powershell
python -m pytest -v
```

## Disclaimer

This project is intended for educational and data-engineering practice. NSE endpoints and data availability may change. This project does not provide investment advice.

## Author

Vasanthi Reddy

GitHub: https://github.com/vasanthi988/nse-market-data-downloader