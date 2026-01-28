import csv
from io import StringIO
from typing import List, Dict

from app.core.custom_exceptions import CSVValidationException

REQUIRED_HEADERS = {"name", "address"}
OPTIONAL_HEADERS = {"phone"}
MAX_ROWS = 20


def validate_csv(content: str) -> Dict:
    try:
        reader = csv.DictReader(StringIO(content))
    except Exception:
        raise CSVValidationException("Invalid CSV format")

    headers = set(reader.fieldnames or [])
    expected_headers = REQUIRED_HEADERS | OPTIONAL_HEADERS

    if not REQUIRED_HEADERS.issubset(headers):
        raise CSVValidationException(
            f"Missing required headers: {REQUIRED_HEADERS - headers}"
        )

    if not headers.issubset(expected_headers):
        raise CSVValidationException(
            f"Unexpected headers: {headers - expected_headers}"
        )

    rows = list(reader)

    if len(rows) == 0:
        raise CSVValidationException("CSV contains no hospital records")

    if len(rows) > MAX_ROWS:
        raise CSVValidationException("Maximum 20 hospitals allowed per CSV")

    errors = []
    seen = set()

    for idx, row in enumerate(rows, start=1):
        name = (row.get("name") or "").strip()
        address = (row.get("address") or "").strip()
        phone = (row.get("phone") or "").strip()

        if not name:
            errors.append(f"Row {idx}: 'name' is required")
        if not address:
            errors.append(f"Row {idx}: 'address' is required")

        # Duplicate detection
        key = (name.lower(), address.lower())
        if key in seen:
            errors.append(f"Row {idx}: Duplicate hospital entry")
        seen.add(key)

        # Optional phone sanity check
        if phone and len(phone) < 7:
            errors.append(f"Row {idx}: Phone number looks invalid")

    return {
        "valid": len(errors) == 0,
        "total_rows": len(rows),
        "errors": errors
    }
