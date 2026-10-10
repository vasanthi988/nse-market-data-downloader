
import logging

from src.config import DATASETS
from src.downloader import create_session, fetch_page


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


def main():
    try:
        session = create_session()
    except Exception as exc:
        logging.error("Could not initialize NSE session: %s", exc)
        return

    for dataset_name in DATASETS:
        try:
            response = fetch_page(session, dataset_name)

            print(f"\nDataset: {dataset_name}")
            print(f"HTTP status: {response.status_code}")
            print(
                "Content type:",
                response.headers.get("Content-Type", "unknown"),
            )
            print("Response preview:")
            print(response.text[:250].replace("\n", " "))

        except Exception as exc:
            logging.error("%s failed: %s", dataset_name, exc)
            continue


if __name__ == "__main__":
    main()