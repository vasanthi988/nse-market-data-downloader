
import logging

logger = logging.getLogger(__name__)


def parse_dataset(response, dataset_name):
    """Extract records from NSE JSON responses."""
    responses = response if isinstance(response, list) else [response]
    records = []

    def collect_records(payload):
        if isinstance(payload, list):
            for item in payload:
                if isinstance(item, dict):
                    records.append(item)
                else:
                    collect_records(item)

        elif isinstance(payload, dict):
            # NSE often returns groups such as NIFTY and BANKNIFTY,
            # each containing a "data" list.
            if isinstance(payload.get("data"), list):
                collect_records(payload["data"])
            else:
                for key, value in payload.items():
                    if key != "legends":
                        collect_records(value)

    for item in responses:
        try:
            payload = item.json()
        except ValueError as exc:
            raise ValueError(
                f"{dataset_name}: Response is not valid JSON"
            ) from exc

        collect_records(payload)

    # Remove exact duplicate records.
    unique_records = []
    seen = set()

    for record in records:
        marker = tuple(
            sorted((str(key), repr(value))
                   for key, value in record.items())
        )
        if marker not in seen:
            seen.add(marker)
            unique_records.append(record)

    if not unique_records:
        raise ValueError(
            f"{dataset_name}: No records found in API response"
        )

    logger.info(
        "%s: Parsed %s unique records",
        dataset_name,
        len(unique_records),
    )

    return unique_records
