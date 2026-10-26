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
- Logs processing progress and errors to the console.
- Includes automated tests using pytest.

## Technologies Used

- Python 3.12
- Requests
- CSV and JSON
- Pytest
- Git and GitHub

## Project Structure

```text
nse-market-data-downloader/
├── src/
│   ├── config.py
│   ├── downloader.py
│   ├── logger_config.py
│   ├── parser.py
│   ├── storage.py
│   └── validator.py
├── tests/
├── data/
├── logs/
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

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

Install the dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Run the Downloader

Run all configured datasets:

```powershell
python main.py
```

The application requests data from NSE, parses the responses, validates the records, and saves successful results in the `data/` directory.
### Download All Datasets

Run the following command to download all four NSE datasets:

```powershell
python main.py
```

### Download Individual Datasets

Run any one of these commands to download only the selected dataset:

```powershell
python main.py --dataset top-gainers-losers
python main.py --dataset upper-band-hitters
python main.py --dataset volume-gainers-spurts
python main.py --dataset 52-week-high-equity-market
```

### Run Tests

```powershell
python -m pytest -v
```

### Logs

Application logs are displayed in the console and saved to `logs/nse_downloader.log`.

### Output Files

The filenames include the execution date in `YYYY-MM-DD` format. For example, on October 26, 2026:

- `top-gainers-losers_2026-10-26.csv`
- `upper-band-hitters_2026-10-26.csv`
- `volume-gainers-spurts_2026-10-26.csv`
- `52-week-high-equity-market_2026-10-26.csv`

The record counts can change based on the data available from NSE when the downloader runs. Running the downloader again on the same date overwrites the corresponding dated CSV files.

## Data Validation

The validation module checks:

- Whether the input contains a list of dictionary records.
- Whether configured required fields contain values.
- Whether duplicate symbols are present.
- Whether floating-point values include invalid values such as `NaN` or infinity.
- Whether the dataset passes validation before it is saved.

Empty or invalid responses are handled as errors rather than being treated as successful downloads.

## Error Handling

- HTTP errors and request timeouts are handled by the downloader.
- Failed requests are retried according to the configured retry settings.
- Invalid JSON responses and responses without usable records can fail parsing.
- Validation failures prevent the affected dataset from being saved.
- A failure in one dataset does not stop the remaining datasets from being processed.

## Automated Testing

Run the test suite:

```powershell
python -m pytest -v
```

The current test suite contains eight tests covering dataset selection errors, CSV storage, invalid inputs, empty records, and basic record validation.

## Limitations

- The project depends on the availability and response structure of NSE endpoints.
- NSE may change its API endpoints, response fields, or access restrictions.
- Downloaded data reflects the response received when the application runs.
- A successful HTTP response does not guarantee that every record is complete or suitable for financial analysis.
- The current entry point processes all configured datasets; individual dataset selection is not documented as a supported command.

## Disclaimer

This project is intended for educational and data-engineering practice only. It does not provide investment advice.

## Author

**Vasanthi Reddy**

GitHub: https://github.com/vasanthi988/nse-market-data-downloader
