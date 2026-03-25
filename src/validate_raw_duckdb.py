#!/usr/bin/env python3
"""Validate raw DuckDB ingestion outputs for Phase 4."""

from __future__ import annotations

import datetime as dt
import re
from pathlib import Path

import duckdb
import pandas as pd

from ingestion.source_registry import SourceSpec, load_source_registry


ROOT_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT_DIR / "data" / "raw"
DUCKDB_PATH = ROOT_DIR / "data" / "processed" / "regional_resilience.duckdb"
REPORT_PATH = ROOT_DIR / "data" / "reports" / "raw_load_validation_report.md"

def table_name_for(file_name: str) -> str:
    stem = Path(file_name).stem
    normalized = re.sub(r"[^a-zA-Z0-9]+", "_", stem).strip("_").lower()
    return f"raw_{normalized}"


def source_line_count(spec: SourceSpec) -> int:
    if spec.source_format == "csv":
        text = (RAW_DIR / spec.file_name).read_text(encoding=spec.encoding)
        return len(text.splitlines())

    if spec.source_format == "xlsx":
        df = pd.read_excel((RAW_DIR / spec.file_name), header=None, dtype=str, sheet_name=spec.sheet_name)
        return int(df.shape[0])

    raise ValueError(f"Unsupported source format for validation: {spec.source_format}")


def source_lines(spec: SourceSpec) -> list[str]:
    if spec.source_format == "csv":
        text = (RAW_DIR / spec.file_name).read_text(encoding=spec.encoding)
        return text.splitlines()

    if spec.source_format == "xlsx":
        df = pd.read_excel((RAW_DIR / spec.file_name), header=None, dtype=str, sheet_name=spec.sheet_name)
        df = df.where(pd.notnull(df), "")
        return [";".join(str(x) for x in row) for row in df.values.tolist()]

    raise ValueError(f"Unsupported source format for validation: {spec.source_format}")


def validate_file(conn: duckdb.DuckDBPyConnection, spec: SourceSpec) -> dict[str, str | int | bool]:
    table_name = table_name_for(spec.file_name)

    table_exists = conn.execute(
        """
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_schema = 'raw' AND table_name = ?
        """,
        [table_name],
    ).fetchone()[0] == 1

    src_lines = source_lines(spec)
    expected_rows = len(src_lines)
    loaded_rows = 0
    mojibake_rows = 0
    non_ascii_source_rows = sum(1 for line in src_lines if any(ord(ch) > 127 for ch in line))
    non_ascii_line_mismatches = 0

    if table_exists:
        loaded_rows = int(conn.execute(f"SELECT COUNT(*) FROM raw.{table_name}").fetchone()[0])
        mojibake_rows = int(
            conn.execute(f"SELECT COUNT(*) FROM raw.{table_name} WHERE raw_line LIKE '%�%'").fetchone()[0]
        )
        if non_ascii_source_rows > 0:
            db_rows = conn.execute(
                f"SELECT line_number, raw_line FROM raw.{table_name}"
            ).fetchall()
            db_map = {int(line_number): raw_line for line_number, raw_line in db_rows}

            for idx, src_line in enumerate(src_lines, start=1):
                if any(ord(ch) > 127 for ch in src_line):
                    if db_map.get(idx) != src_line:
                        non_ascii_line_mismatches += 1

    row_count_match = table_exists and (loaded_rows == expected_rows)
    encoding_ok = table_exists and (mojibake_rows == 0) and (non_ascii_line_mismatches == 0)

    return {
        "file_name": spec.file_name,
        "source_format": spec.source_format,
        "table_name": table_name,
        "table_exists": table_exists,
        "expected_rows": expected_rows,
        "loaded_rows": loaded_rows,
        "row_count_match": row_count_match,
        "mojibake_rows": mojibake_rows,
        "non_ascii_source_rows": non_ascii_source_rows,
        "non_ascii_line_mismatches": non_ascii_line_mismatches,
        "encoding_ok": encoding_ok,
    }


def write_report(results: list[dict[str, str | int | bool]]) -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    overall_ok = all(
        r["table_exists"] and r["row_count_match"] and r["encoding_ok"] for r in results
    )

    lines = [
        "# Raw Load Validation Report",
        "",
        f"Generated at (UTC): {dt.datetime.now(dt.timezone.utc).isoformat()}",
        "",
        "## Overall Result",
        "",
        f"- Status: {'PASS' if overall_ok else 'FAIL'}",
        "",
        "## File-Level Checks",
        "",
        "| File | Format | Raw Table | Exists | Expected Rows | Loaded Rows | Row Count Match | Mojibake Rows (`�`) | Non-ASCII Source Rows | Non-ASCII Mismatches | Encoding Check |",
        "| --- | --- | --- | --- | ---: | ---: | --- | ---: | ---: | ---: | --- |",
    ]

    for r in results:
        lines.append(
            "| {file_name} | {source_format} | {table_name} | {table_exists} | {expected_rows} | {loaded_rows} | {row_count_match} | {mojibake_rows} | {non_ascii_source_rows} | {non_ascii_line_mismatches} | {encoding_ok} |".format(
                **r
            )
        )

    lines.extend(
        [
            "",
            "## Validation Logic",
            "",
            "1. Raw table exists in schema `raw`.",
            "2. Loaded row count equals source line count from CSV file.",
            "3. Encoding corruption check: no replacement-char rows (`�`).",
            "4. Non-ASCII integrity check: source non-ASCII lines match `raw_line` exactly by line number.",
            "5. For XLSX sources, row-count and line-preservation checks are approximated via sheet row extraction.",
            "",
        ]
    )

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    specs = load_source_registry()
    conn = duckdb.connect(str(DUCKDB_PATH))
    try:
        results = [validate_file(conn, spec) for spec in specs]
    finally:
        conn.close()

    write_report(results)
    print(f"Validation report written to: {REPORT_PATH}")


if __name__ == "__main__":
    main()
