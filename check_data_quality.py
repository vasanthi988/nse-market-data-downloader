
import csv
import math
from pathlib import Path

data_dir = Path("data")

if not data_dir.exists():
    print("ERROR: data directory not found.")
    raise SystemExit(1)

csv_files = sorted(
    file for file in data_dir.glob("*.csv")
    if file.name != "download_summary.csv"
)

price_fields = [
    "open_price", "high_price", "low_price", "ltp",
    "new52WHL", "prev52WHL", "prevClose",
    "highPrice", "lowPrice", "yearHigh", "yearLow"
]

total_records = 0
missing_symbols = 0
duplicate_symbols = 0
missing_price_values = 0

numeric_errors = 0
numeric_files_passed = 0
numeric_files_checked = 0

range_errors = 0
range_checks = 0

print("\nNSE MARKET DATA QUALITY CHECK")
print("=" * 70)
print(f"Market-data CSV files found: {len(csv_files)}")

for file in csv_files:
    with file.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        columns = reader.fieldnames or []

    total_records += len(rows)

    # Check missing symbols
    symbols = [
        (row.get("symbol") or "").strip()
        for row in rows
    ]

    missing_symbols += sum(1 for symbol in symbols if not symbol)

    # Check duplicate non-empty symbols within each file
    valid_symbols = [symbol for symbol in symbols if symbol]
    duplicate_symbols += len(valid_symbols) - len(set(valid_symbols))

    # Check missing applicable price values
    fields = [field for field in price_fields if field in columns]

    for row in rows:
        for field in fields:
            if not (row.get(field) or "").strip():
                missing_price_values += 1

    # Numeric price validation
    invalid_values = []

    for row_number, row in enumerate(rows, start=2):
        for field in fields:
            value = (row.get(field) or "").strip()

            if not value:
                continue

            try:
                number = float(value)

                if not math.isfinite(number) or number < 0:
                    invalid_values.append((row_number, field, value))

            except ValueError:
                invalid_values.append((row_number, field, value))

    if fields:
        numeric_files_checked += 1

        if invalid_values:
            numeric_errors += len(invalid_values)
            print(
                f"NUMERIC CHECK: {file.name} - "
                f"{len(invalid_values)} invalid value(s)"
            )

            for item in invalid_values[:5]:
                print(
                    f"  Row {item[0]}, column {item[1]}: {item[2]}"
                )
        else:
            numeric_files_passed += 1
            print(f"NUMERIC CHECK: {file.name} - PASS")

    # Price-range validation
    if all(field in columns for field in ["high_price", "low_price", "ltp"]):
        for row_number, row in enumerate(rows, start=2):
            try:
                high = float(row["high_price"])
                low = float(row["low_price"])
                ltp = float(row["ltp"])

                range_checks += 1

                if low > high or ltp < low or ltp > high:
                    range_errors += 1
                    print(
                        f"RANGE CHECK: {file.name}, row {row_number} - "
                        f"high={high}, low={low}, ltp={ltp}"
                    )

            except (ValueError, TypeError):
                # Numeric validation reports invalid values separately
                pass

# Overall results
overall_pass = (
    missing_symbols == 0
    and duplicate_symbols == 0
    and missing_price_values == 0
    and numeric_errors == 0
    and numeric_files_checked > 0
    and numeric_files_passed == numeric_files_checked
    and range_errors == 0
)

print("\nCOMPLETENESS CHECK")
print("-" * 70)
print(f"Total market-data records: {total_records}")
print(f"Missing symbols: {missing_symbols}")
print(f"Duplicate symbols: {duplicate_symbols}")
print(f"Missing applicable price values: {missing_price_values}")

print("\nNUMERIC PRICE VALIDATION")
print("-" * 70)
print(f"Numeric files passed: {numeric_files_passed}/{numeric_files_checked}")
print(f"Invalid numeric price values: {numeric_errors}")

print("\nPRICE RANGE VALIDATION")
print("-" * 70)
print(f"Price-range records checked: {range_checks}")
print(f"Price-range issues: {range_errors}")

print("\nOVERALL STATUS")
print("-" * 70)
print("PASSED" if overall_pass else "CHECK REQUIRED")

# Save report
report_path = data_dir / "data_quality_report.txt"

with report_path.open("w", encoding="utf-8") as report:
    report.write("NSE MARKET DATA - QUALITY REPORT\n")
    report.write("=" * 60 + "\n\n")
    report.write(f"Market-data CSV files: {len(csv_files)}\n")
    report.write(f"Total market-data records: {total_records}\n")
    report.write(f"Missing symbols: {missing_symbols}\n")
    report.write(f"Duplicate symbols: {duplicate_symbols}\n")
    report.write(f"Missing applicable price values: {missing_price_values}\n")
    report.write(
        f"Numeric files passed: {numeric_files_passed}/{numeric_files_checked}\n"
    )
    report.write(f"Invalid numeric price values: {numeric_errors}\n")
    report.write(f"Price-range records checked: {range_checks}\n")
    report.write(f"Price-range issues: {range_errors}\n\n")
    report.write(
        f"OVERALL STATUS: {'PASSED' if overall_pass else 'CHECK REQUIRED'}\n"
    )

print(f"\nQuality report saved to: {report_path}")
