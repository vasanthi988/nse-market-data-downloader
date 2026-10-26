
import logging

from src.config import DATASETS, DATA_DIR
from src.downloader import create_session, fetch_page
from src.parser import parse_dataset
from src.storage import save_records


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


def main():
    session = None

    try:
        session = create_session()

        for dataset_name, dataset_config in DATASETS.items():
            try:
                logging.info("Processing dataset: %s", dataset_name)

                response = fetch_page(session, dataset_name)
                records = parse_dataset(response, dataset_name)

                filename = f"{dataset_config['filename']}.csv"

                saved_count = save_records(
                    records,
                    filename,
                    output_dir=str(DATA_DIR),
                )

                logging.info(
                    "%s: Successfully saved %s records to %s",
                    dataset_name,
                    saved_count,
                    filename,
                )

            except Exception as exc:
                logging.error(
                    "%s failed: %s",
                    dataset_name,
                    exc,
                )
                continue

    except Exception as exc:
        logging.error("Could not initialize NSE session: %s", exc)

    finally:
        if session is not None:
            session.close()


if __name__ == "__main__":
    main()
