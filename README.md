# NSE Market Data Downloader & Data Quality Validator

A Python-based data engineering project that collects market data from the National Stock Exchange of India (NSE), stores it in CSV files, and validates the downloaded data for quality issues.

## Project Overview

This project automates the collection of selected NSE market datasets through HTTP API requests. It organizes the downloaded records into CSV files, validates records, logs execution details, and generates a data quality report.

## Features

- Downloads NSE top gainers and top losers.
- Collects upper-band, lower-band, and both-band market data.
- Downloads volume gainers and 52-week-high data.
- Saves records to CSV files.
- Validates record structure, duplicate symbols, and invalid floating-point values.
- Checks missing symbols, numeric price values, and applicable price ranges.
- Maintains download summaries and execution logs.
- Includes automated tests using pytest.
- Supports automated testing through GitHub Actions.

## Technologies Used

- Python 3.12
- Requests
- CSV and JSON
- Pytest
- Logging
- Git and GitHub
- GitHub Actions

## Project Structure

```text
nse-market-data-downloader/
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── downloader.py
│   ├── logger_config.py
│   ├── storage.py
│   └── validator.py
├── tests/
│   └── test_project.py
├── .github/
│   └── workflows/
│       └── main.yml
├── check_data_quality.py
├── download_nse_data.py
├── inspect_nse.py
├── main.py
├── requirements.txt
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/vasanthi988/nse-market-data-downloader.git
cd nse-market-data-downloader
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Download market data

```bash
python download_nse_data.py
```

### 5. Run data quality checks

```bash
python check_data_quality.py
```

### 6. Run automated tests

```bash
python -m pytest -v
```

## Output

The application generates CSV files in the `data/` directory, a download summary, a data quality report, and execution logs.

Example from a verified run:

- Market-data CSV files: 25
- Downloaded market-data records: 801
- Missing symbols detected: 0
- Duplicate symbols detected: 0
- Invalid numeric price values: 0
- Price-range issues: 0
- Automated tests: 8 passed

*These are results from one execution and may change as NSE data changes.*

## Learning Outcomes

- Working with HTTP APIs and JSON responses.
- Handling exceptions and logging application activity.
- Organizing Python code into reusable modules.
- Writing CSV files and validating downloaded data.
- Creating automated tests with pytest.
- Automating test execution using GitHub Actions.

## Disclaimer

This project is intended for educational and data-engineering practice. Market data availability and API responses may change. It does not provide investment advice or guarantee real-time data availability.

## Author

Vasanthi Reddy

[GitHub Repository](https://github.com/vasanthi988/nse-market-data-downloader)
