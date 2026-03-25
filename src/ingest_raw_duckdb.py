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
import pandas as pd

from ingestion.source_registry import SourceSpec, load_source_registry


ROOT_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT_DIR / "data" / "raw"
REPORTS_DIR = ROOT_DIR / "data" / "reports"
DUCKDB_PATH = ROOT_DIR / "data" / "processed" / "regional_resilience.duckdb"
LOG_PATH = REPORTS_DIR / "raw_ingestion_log.csv"
SCHEMA_DRIFT_REPORT_PATH = REPORTS_DIR / "schema_drift_report.md"

DATE_RE = re.compile(r"^\d{2}\.\d{2}\.\d{4}$")


def table_name_for(file_name: str) -> str:
    stem = Path(file_name).stem
    normalized = re.sub(r"[^a-zA-Z0-9]+", "_", stem).strip("_").lower()
    return f"raw_{normalized}"


def analyze_structure(lines: list[str], delimiter: str) -> dict[str, int]:
    first_data_idx = -1
    last_data_idx = -1
    data_like_rows = 0

    for idx, line in enumerate(lines):
        first_col = line.split(delimiter, 1)[0] if line else ""
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


def read_source_rows(spec: SourceSpec) -> tuple[list[str], list[list[str]]]:
    if spec.source_format == "csv":
        text = spec.file_path.read_text(encoding=spec.encoding)
        lines = text.splitlines()
        parsed = [line.split(spec.delimiter) for line in lines]
        return lines, parsed

    if spec.source_format == "xlsx":
        df = pd.read_excel(spec.file_path, header=None, dtype=str, sheet_name=spec.sheet_name)
        df = df.where(pd.notnull(df), None)
        parsed: list[list[str]] = []
        lines: list[str] = []
        for row in df.values.tolist():
            normalized = ["" if value is None else str(value) for value in row]
            parsed.append(normalized)
            lines.append(spec.delimiter.join(normalized))
        return lines, parsed

    raise ValueError(f"Unsupported source format: {spec.source_format}")


def evaluate_schema_drift(spec: SourceSpec, observed_columns: int) -> tuple[str, str]:
    min_cols = spec.expected_min_columns
    max_cols = spec.expected_max_columns
    if min_cols is None and max_cols is None:
        return "no_expectation", "No expected column range configured"

    if min_cols is not None and observed_columns < min_cols:
        return "fail", f"Observed max columns {observed_columns} below expected minimum {min_cols}"
    if max_cols is not None and observed_columns > max_cols:
        return "fail", f"Observed max columns {observed_columns} above expected maximum {max_cols}"

    if min_cols is None:
        return "ok", f"Observed max columns {observed_columns} within <= {max_cols}"
    if max_cols is None:
        return "ok", f"Observed max columns {observed_columns} within >= {min_cols}"
    return "ok", f"Observed max columns {observed_columns} within [{min_cols}, {max_cols}]"


def ingest_file(conn: duckdb.DuckDBPyConnection, spec: SourceSpec) -> dict[str, str | int]:
    ingested_at = dt.datetime.now(dt.timezone.utc).isoformat()
    table_name = table_name_for(spec.file_name)

    result: dict[str, str | int] = {
        "ingested_at_utc": ingested_at,
        "file_name": spec.file_name,
        "source_format": spec.source_format,
        "encoding": spec.encoding,
        "delimiter": spec.delimiter,
        "table_name": table_name,
        "source_row_count": 0,
        "max_column_count": 0,
        "loaded_row_count": 0,
        "metadata_rows": 0,
        "data_like_rows": 0,
        "footer_rows": 0,
        "schema_drift_status": "unknown",
        "schema_drift_detail": "",
        "error": "",
    }

    try:
        lines, parsed = read_source_rows(spec)
        max_cols = max((len(parts) for parts in parsed), default=0)

        structure = analyze_structure(lines, spec.delimiter)
        drift_status, drift_detail = evaluate_schema_drift(spec, max_cols)

        result["source_row_count"] = len(lines)
        result["max_column_count"] = max_cols
        result["metadata_rows"] = structure["metadata_rows"]
        result["data_like_rows"] = structure["data_like_rows"]
        result["footer_rows"] = structure["footer_rows"]
        result["schema_drift_status"] = drift_status
        result["schema_drift_detail"] = drift_detail

        if spec.fail_on_schema_drift and drift_status == "fail":
            raise ValueError(f"Schema drift detected: {drift_detail}")

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
            fields = parsed[idx - 1] if idx - 1 < len(parsed) else line.split(spec.delimiter)
            padded = fields + [None] * (max_cols - len(fields))
            rows.append((idx, line, len(fields), *padded, spec.file_name, ingested_at))

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
        "source_format",
        "encoding",
        "delimiter",
        "table_name",
        "source_row_count",
        "max_column_count",
        "loaded_row_count",
        "metadata_rows",
        "data_like_rows",
        "footer_rows",
        "schema_drift_status",
        "schema_drift_detail",
        "error",
    ]

    with LOG_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(log_rows)


def write_schema_drift_report(log_rows: list[dict[str, str | int]]) -> None:
    lines = [
        "# Schema Drift Report",
        "",
        f"Generated at (UTC): {dt.datetime.now(dt.timezone.utc).isoformat()}",
        "",
        "| File | Format | Observed Max Columns | Drift Status | Detail |",
        "| --- | --- | ---: | --- | --- |",
    ]

    for row in log_rows:
        lines.append(
            "| {file_name} | {source_format} | {max_column_count} | {schema_drift_status} | {schema_drift_detail} |".format(
                **row
            )
        )

    SCHEMA_DRIFT_REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    DUCKDB_PATH.parent.mkdir(parents=True, exist_ok=True)
    sources = load_source_registry()

    conn = duckdb.connect(str(DUCKDB_PATH))
    try:
        logs = [ingest_file(conn, source) for source in sources]
        write_log(logs)
        write_schema_drift_report(logs)
    finally:
        conn.close()

    print(f"Raw ingestion completed. Log written to: {LOG_PATH}")


if __name__ == "__main__":
    main()
