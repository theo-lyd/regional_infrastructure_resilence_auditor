#!/usr/bin/env python3
"""Raw CSV ingestion into DuckDB without normalization.

This script intentionally preserves raw values and raw lines exactly as read
from source files (after decoding with the configured file encoding).
"""

from __future__ import annotations

import csv
import datetime as dt
import re
from pathlib import Path

import duckdb


ROOT_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT_DIR / "data" / "raw"
REPORTS_DIR = ROOT_DIR / "data" / "reports"
DUCKDB_PATH = ROOT_DIR / "data" / "processed" / "regional_resilience.duckdb"
LOG_PATH = REPORTS_DIR / "raw_ingestion_log.csv"

RAW_FILES = [
    "22541-01-01-4.csv",
    "22542-01-02-4.csv",
    "23111-01-04-4.csv",
]

DATE_RE = re.compile(r"^\d{2}\.\d{2}\.\d{4}$")


def table_name_for(file_name: str) -> str:
    return f"raw_{file_name.replace('.csv', '').replace('-', '_')}"


def analyze_structure(lines: list[str]) -> dict[str, int]:
    first_data_idx = -1
    last_data_idx = -1
    data_like_rows = 0

    for idx, line in enumerate(lines):
        first_col = line.split(";", 1)[0] if line else ""
        if DATE_RE.match(first_col):
            data_like_rows += 1
            if first_data_idx == -1:
                first_data_idx = idx
            last_data_idx = idx

    if first_data_idx == -1:
        return {
            "metadata_rows": len(lines),
            "data_like_rows": 0,
            "footer_rows": 0,
        }

    metadata_rows = first_data_idx
    footer_rows = max(0, len(lines) - (last_data_idx + 1))

    return {
        "metadata_rows": metadata_rows,
        "data_like_rows": data_like_rows,
        "footer_rows": footer_rows,
    }


def ingest_file(conn: duckdb.DuckDBPyConnection, file_name: str) -> dict[str, str | int]:
    file_path = RAW_DIR / file_name
    encoding = "iso-8859-1"
    ingested_at = dt.datetime.now(dt.timezone.utc).isoformat()
    table_name = table_name_for(file_name)

    result: dict[str, str | int] = {
        "ingested_at_utc": ingested_at,
        "file_name": file_name,
        "encoding": encoding,
        "delimiter": ";",
        "table_name": table_name,
        "source_row_count": 0,
        "max_column_count": 0,
        "loaded_row_count": 0,
        "metadata_rows": 0,
        "data_like_rows": 0,
        "footer_rows": 0,
        "error": "",
    }

    try:
        text = file_path.read_text(encoding=encoding)
        lines = text.splitlines()
        parsed = [line.split(";") for line in lines]
        max_cols = max((len(parts) for parts in parsed), default=0)

        structure = analyze_structure(lines)

        result["source_row_count"] = len(lines)
        result["max_column_count"] = max_cols
        result["metadata_rows"] = structure["metadata_rows"]
        result["data_like_rows"] = structure["data_like_rows"]
        result["footer_rows"] = structure["footer_rows"]

        value_columns = [f"col_{idx}" for idx in range(1, max_cols + 1)]
        all_columns = [
            "line_number",
            "raw_line",
            "field_count",
            *value_columns,
            "source_file",
            "ingested_at_utc",
        ]

        conn.execute("CREATE SCHEMA IF NOT EXISTS raw")
        conn.execute(f"DROP TABLE IF EXISTS raw.{table_name}")

        col_defs = ["line_number BIGINT", "raw_line VARCHAR", "field_count INTEGER"]
        col_defs.extend([f"{col} VARCHAR" for col in value_columns])
        col_defs.extend(["source_file VARCHAR", "ingested_at_utc VARCHAR"])

        conn.execute(f"CREATE TABLE raw.{table_name} ({', '.join(col_defs)})")

        insert_sql = (
            f"INSERT INTO raw.{table_name} ({', '.join(all_columns)}) "
            f"VALUES ({', '.join(['?'] * len(all_columns))})"
        )

        rows = []
        for idx, line in enumerate(lines, start=1):
            fields = line.split(";")
            padded = fields + [None] * (max_cols - len(fields))
            rows.append((idx, line, len(fields), *padded, file_name, ingested_at))

        if rows:
            conn.executemany(insert_sql, rows)

        loaded_count = conn.execute(f"SELECT COUNT(*) FROM raw.{table_name}").fetchone()[0]
        result["loaded_row_count"] = int(loaded_count)

    except Exception as exc:  # pragma: no cover - operational path
        result["error"] = str(exc)

    return result


def write_log(log_rows: list[dict[str, str | int]]) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "ingested_at_utc",
        "file_name",
        "encoding",
        "delimiter",
        "table_name",
        "source_row_count",
        "max_column_count",
        "loaded_row_count",
        "metadata_rows",
        "data_like_rows",
        "footer_rows",
        "error",
    ]

    with LOG_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(log_rows)


def main() -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    DUCKDB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = duckdb.connect(str(DUCKDB_PATH))
    try:
        logs = [ingest_file(conn, file_name) for file_name in RAW_FILES]
        write_log(logs)
    finally:
        conn.close()

    print(f"Raw ingestion completed. Log written to: {LOG_PATH}")


if __name__ == "__main__":
    main()
