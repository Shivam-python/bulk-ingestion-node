# app/utils/csv_parser.py
import csv
from io import StringIO


def parse_csv(content: str):
    reader = csv.DictReader(StringIO(content))
    rows = list(reader)

    if len(rows) > 20:
        raise ValueError("CSV exceeds 20 hospital limit")

    return rows
