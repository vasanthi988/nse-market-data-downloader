
import logging
import math

logger = logging.getLogger(__name__)


def validate_records(records, required_fields=None):
    """Validate records for structure, required fields, and duplicates."""
    if not isinstance(records, list):
        raise ValueError("Expected records to be a list.")

    if not all(isinstance(record, dict) for record in records):
        raise ValueError("Every record must be a dictionary.")

    if not records:
        logger.warning("No records supplied for validation.")
        return {
            "total_records": 0,
            "missing_required_fields": 0,
            "duplicate_records": 0,
            "invalid_numeric_values": 0,
            "passed": True,
        }

    required_fields = required_fields or []
    missing_required_fields = 0
    duplicate_records = 0
    invalid_numeric_values = 0
    seen = set()

    for record in records:
        for field in required_fields:
            value = record.get(field)
            if value is None or str(value).strip() == "":
                missing_required_fields += 1

        symbol = record.get("symbol")
        if symbol is not None and str(symbol).strip():
            normalized_symbol = str(symbol).strip().upper()
            if normalized_symbol in seen:
                duplicate_records += 1
            else:
                seen.add(normalized_symbol)

        for value in record.values():
            if isinstance(value, float) and not math.isfinite(value):
                invalid_numeric_values += 1

    passed = (
        missing_required_fields == 0
        and duplicate_records == 0
        and invalid_numeric_values == 0
    )

    result = {
        "total_records": len(records),
        "missing_required_fields": missing_required_fields,
        "duplicate_records": duplicate_records,
        "invalid_numeric_values": invalid_numeric_values,
        "passed": passed,
    }

    logger.info("Validation result: %s", result)
    return result
