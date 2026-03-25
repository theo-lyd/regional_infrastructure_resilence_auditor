#!/usr/bin/env python3
"""Validate raw DuckDB ingestion outputs for Phase 4."""

from __future__ import annotations

import datetime as dt
from pathlib import Path

import duckdb


ROOT_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT_DIR / "data" / "raw"
DUCKDB_PATH = ROOT_DIR / "data" / "processed" / "regional_resilience.duckdb"
REPORT_PATH = ROOT_DIR / "data" / "reports" / "raw_load_validation_report.md"

RAW_FILES = [
    "22541-01-01-4.csv",
    "22542-01-02-4.csv",
    "23111-01-04-4.csv",
]


def table_name_for(file_name: str) -> str:
    return f"raw_{file_name.replace('.csv', '').replace('-', '_')}"


def source_line_count(file_name: str) -> int:
    text = (RAW_DIR / file_name).read_text(encoding="iso-8859-1")
    return len(text.splitlines())


def source_lines(file_name: str) -> list[str]:
    text = (RAW_DIR / file_name).read_text(encoding="iso-8859-1")
    return text.splitlines()


def validate_file(conn: duckdb.DuckDBPyConnection, file_name: str) -> dict[str, str | int | bool]:
    table_name = table_name_for(file_name)

    table_exists = conn.execute(
        """
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_schema = 'raw' AND table_name = ?
        """,
        [table_name],
    ).fetchone()[0] == 1

    src_lines = source_lines(file_name)
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
        "file_name": file_name,
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
        "| File | Raw Table | Exists | Expected Rows | Loaded Rows | Row Count Match | Mojibake Rows (`�`) | Non-ASCII Source Rows | Non-ASCII Mismatches | Encoding Check |",
        "| --- | --- | --- | ---: | ---: | --- | ---: | ---: | ---: | --- |",
    ]

    for r in results:
        lines.append(
            "| {file_name} | {table_name} | {table_exists} | {expected_rows} | {loaded_rows} | {row_count_match} | {mojibake_rows} | {non_ascii_source_rows} | {non_ascii_line_mismatches} | {encoding_ok} |".format(
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
            "",
        ]
    )

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    conn = duckdb.connect(str(DUCKDB_PATH))
    try:
        results = [validate_file(conn, file_name) for file_name in RAW_FILES]
    finally:
        conn.close()

    write_report(results)
    print(f"Validation report written to: {REPORT_PATH}")


if __name__ == "__main__":
    main()
