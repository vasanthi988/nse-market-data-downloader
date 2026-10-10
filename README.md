# NSE Market Data Downloader

A Python project that collects market data from the National Stock Exchange of India (NSE), saves the results as CSV files, and validates data quality.

## Features

- Fetches data from configured NSE endpoints.
- Collects top gainers and losers across multiple market categories.
- Collects upper-band, lower-band, and both-band data.
- Collects volume gainers and 52-week-high data.
- Saves downloaded records into CSV files.
- Handles request failures and retries failed requests.
- Records download activity and errors in a log file.
- Generates a download summary.
- Validates missing symbols, duplicate symbols, numeric price values, and price ranges.
- Creates a data quality report.

## Technologies Used

- Python
- Requests
- CSV and JSON
- Logging
- pathlib
- unittest / Python testing tools

## Project Structure

```text
nse-market-data-downloader/
├── data/
├── logs/
├── src/
│   ├── config.py
│   ├── downloader.py
│   ├── logger_config.py
│   ├── storage.py
│   └── validator.py
├── tests/
├── check_data_quality.py
├── download_nse_data.py
├── inspect_nse.py
├── main.py
├── test_nse_api.py
├── requirements.txt
└── README.md
```

## Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd nse-market-data-downloader
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install requests
```

### 4. Download market data

```powershell
python .\download_nse_data.py
```

Downloaded CSV files are saved in the `data/` directory.

### 5. Validate data quality

```powershell
python .\check_data_quality.py
```

The script prints validation results and saves the report to:

`data/data_quality_report.txt`

### 6. View logs

```powershell
Get-Content .\logs\nse_downloader.log -Tail 30
```

## Data Quality Results

In a validation run on October 10, 2026:

- Market-data CSV files checked: 25
- Market-data records processed: 801
- Missing symbols: 0
- Duplicate symbols: 0
- Missing applicable price values: 0
- Numeric files passed: 25/25
- Invalid numeric price values: 0
- Price-range records checked: 229
- Price-range issues: 0

Results may change with each new download.

## Error Handling and Logging

The downloader logs successful operations and failures. HTTP requests use timeouts, and the configured downloader retries failed requests. A download summary records each dataset's status, output file count, record count, and errors.

## Notes

- This project is intended for educational and data-analysis purposes.
- Availability and response formats of NSE endpoints may change.
- Network access and NSE server behavior can affect downloads.
- Always verify the data before using it for financial decisions.

## Author

Vasanthi Reddy