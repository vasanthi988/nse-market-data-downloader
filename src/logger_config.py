
import logging
from pathlib import Path


def setup_logging():
    """Configure logging to write to both console and a log file."""
    project_dir = Path(__file__).resolve().parent.parent
    log_dir = project_dir / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / "nse_downloader.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(),
        ],
        force=True,
    )

    logging.info("Logging initialized.")
    logging.info("Log file: %s", log_file)
