
import argparse
import logging
from datetime import datetime

from src.config import DATASETS, DATA_DIR, REQUIRED_FIELDS
from src.downloader import create_session, fetch_page
from src.parser import parse_dataset
from src.storage import save_records
from src.validator import validate_records
from src.logger_config import setup_logging

logger = logging.getLogger(__name__)


def main():
    setup_logging()
    parser = argparse.ArgumentParser(
        description="Download NSE market datasets into CSV files."
    )

    parser.add_argument(
        "--dataset",
        choices=list(DATASETS.keys()),
        help="Download only the selected dataset. Omit to download all datasets.",
    )

    args = parser.parse_args()

    if args.dataset:
        selected_datasets = {
            args.dataset: DATASETS[args.dataset]
        }
    else:
        selected_datasets = DATASETS

    run_date = datetime.now().strftime("%Y-%m-%d")
    session = None
    successful = 0
    failed = 0

    logger.info("NSE Market Data Downloader started.")
    logger.info("Output directory: %s", DATA_DIR)

    try:
        session = create_session()

        for dataset_name, dataset_config in selected_datasets.items():
            try:
                logger.info("Processing dataset: %s", dataset_name)

                response = fetch_page(session, dataset_name)
                records = parse_dataset(response, dataset_name)

                validation = validate_records(
                    records,
                    required_fields=REQUIRED_FIELDS[dataset_name],
                )

                logger.info(
                    "%s validation result: %s",
                    dataset_name,
                    validation,
                )

                if not validation["passed"]:
                    raise ValueError(
                        f"Data validation failed: {validation}"
                    )

                filename = (
                    f"{dataset_config['filename']}_{run_date}.csv"
                )

                saved_count = save_records(
                    records,
                    filename,
                    output_dir=str(DATA_DIR),
                )

                logger.info(
                    "%s: Successfully saved %s records to %s",
                    dataset_name,
                    saved_count,
                    DATA_DIR / filename,
                )
                successful += 1

            except Exception:
                failed += 1
                logger.exception("Dataset failed: %s", dataset_name)

    except Exception:
        failed += 1
        logger.exception("Could not initialize NSE session.")

    finally:
        if session is not None:
            session.close()

        logger.info(
            "Download process finished. Successful datasets: %s; Failed: %s",
            successful,
            failed,
        )


if __name__ == "__main__":
    main()
