# NSE Market Data Downloader

A Python project that downloads selected market datasets from the National Stock Exchange of India (NSE), validates the returned records, and saves the results as CSV files.

## Features

- Downloads four NSE market datasets:
  - Top Gainers and Losers
  - Upper Band Hitters
  - Volume Gainers and Spurts
  - 52-Week High — Equity Market
- Uses HTTP requests with timeouts and retry handling.
- Parses JSON responses into structured records.
- Removes exact duplicate records during parsing.
- Validates required fields, duplicate symbols, and invalid numeric values.
- Saves datasets as separate, date-stamped CSV files.
- Continues processing other datasets if one dataset fails.
- Logs processing progress and errors to the console and `logs/nse_downloader.log`.
- Supports downloading all datasets or selecting one dataset.
- Includes automated tests using pytest.

## Technologies Used

- Python 3.12
- Requests
- CSV and JSON
- Pytest
- Git and GitHub

## Installation

Clone the repository:

```bash
git clone https://github.com/vasanthi988/nse-market-data-downloader.git
cd nse-market-data-downloader
```

Create and activate a virtual environment on Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Run the Downloader

### Download all datasets

```powershell
python main.py
```

### Download an individual dataset

Run any one of the following commands:

```powershell
python main.py --dataset top-gainers-losers
python main.py --dataset upper-band-hitters
python main.py --dataset volume-gainers-spurts
python main.py --dataset 52-week-high-equity-market
```

Successful downloads are saved in the `data/` directory. Output filenames include the execution date in `YYYY-MM-DD` format.

For example:

- `top-gainers-losers_2026-10-26.csv`
- `upper-band-hitters_2026-10-26.csv`
- `volume-gainers-spurts_2026-10-26.csv`
- `52-week-high-equity-market_2026-10-26.csv`

Running the downloader again on the same date overwrites the corresponding dated CSV files. Record counts may vary depending on the data available from NSE.

## Data Validation

The validation module checks:

- Whether input consists of a list of dictionary records.
- Whether configured required fields contain values.
- Whether duplicate symbols are present.
- Whether floating-point values include invalid values such as `NaN` or infinity.
- Whether each dataset passes validation before it is saved.

Empty or invalid API responses are handled as errors rather than successful downloads.

## Error Handling

- HTTP errors and request timeouts are handled by the downloader.
- Failed requests are retried according to the configured retry settings.
- Invalid JSON responses and responses without usable records can fail parsing.
- Validation failures prevent the affected dataset from being saved.
- A failure in one dataset does not stop the remaining datasets from being processed.

## Logging

Application logs are displayed in the console and written to:

```text
logs/nse_downloader.log
```

## Automated Testing

Run the test suite:

```powershell
python -m pytest -v
```

The current test suite contains 13 tests covering dataset selection errors, retry behavior, invalid JSON, empty responses, CSV storage, invalid inputs, and record validation.

## Limitations

- The project depends on the availability and response structure of NSE endpoints.
- NSE may change its API endpoints, response fields, or access restrictions.
- Downloaded data reflects the response received when the application runs.
- A successful HTTP response does not guarantee that every record is complete or suitable for financial analysis.
- Automated tests use simulated responses for network error scenarios; they do not guarantee that NSE endpoints will always be available.

## Disclaimer

This project is intended for educational and data-engineering practice only. It does not provide investment advice.

## Author

**Vasanthi Reddy**

GitHub: https://github.com/vasanthi988/nse-market-data-downloader
