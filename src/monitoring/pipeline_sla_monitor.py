#!/usr/bin/env python3
"""Evaluate pipeline SLAs and persist monitoring outputs."""

from __future__ import annotations

import csv
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import duckdb


ROOT_DIR = Path(__file__).resolve().parents[2]
DUCKDB_PATH = ROOT_DIR / "data" / "processed" / "regional_resilience.duckdb"
REPORTS_DIR = ROOT_DIR / "data" / "reports"
LOG_PATH = REPORTS_DIR / "pipeline_run_log.csv"
MARKDOWN_REPORT_PATH = REPORTS_DIR / "pipeline_sla_report.md"

FRESHNESS_THRESHOLD_DAYS = int(os.getenv("SLA_MAX_PREDICTION_STALENESS_DAYS", "30"))
COMPLETENESS_MIN = float(os.getenv("SLA_MIN_COMPLETENESS_RATE", "0.85"))
ROW_DELTA_MAX_RATIO = float(os.getenv("SLA_MAX_ROWCOUNT_DELTA_RATIO", "0.25"))


@dataclass
class CheckResult:
    check_name: str
    status: str
    observed_value: str
    threshold_value: str
    detail: str


def _safe_exists(con: duckdb.DuckDBPyConnection, schema: str, table: str) -> bool:
    q = """
    select count(*)
    from information_schema.tables
    where table_schema = ? and table_name = ?
    """
    return con.execute(q, [schema, table]).fetchone()[0] == 1


def check_freshness(con: duckdb.DuckDBPyConnection) -> CheckResult:
    if not _safe_exists(con, "analytics_predictions", "pred_capacity_growth_forecast"):
        return CheckResult("data_freshness", "FAIL", "missing", f"<= {FRESHNESS_THRESHOLD_DAYS} days", "Prediction table missing")

    max_ts = con.execute(
        """
        select max(try_cast(generated_at_utc as timestamp))
        from analytics_predictions.pred_capacity_growth_forecast
        """
    ).fetchone()[0]

    if max_ts is None:
        return CheckResult("data_freshness", "FAIL", "null", f"<= {FRESHNESS_THRESHOLD_DAYS} days", "No generated timestamps found")

    now = datetime.now(timezone.utc).replace(tzinfo=None)
    age_days = (now - max_ts).days
    status = "PASS" if age_days <= FRESHNESS_THRESHOLD_DAYS else "FAIL"
    detail = f"Latest forecast generated at {max_ts.isoformat()}"
    return CheckResult("data_freshness", status, str(age_days), f"<= {FRESHNESS_THRESHOLD_DAYS}", detail)


def check_completeness(con: duckdb.DuckDBPyConnection) -> CheckResult:
    if not _safe_exists(con, "analytics_marts", "mart_data_quality_status"):
        return CheckResult("minimum_completeness", "FAIL", "missing", f">= {COMPLETENESS_MIN:.2f}", "Data quality mart missing")

    row = con.execute(
        """
        select capacity_completeness_rate, year
        from analytics_marts.mart_data_quality_status
        order by year desc
        limit 1
        """
    ).fetchone()

    if row is None or row[0] is None:
        return CheckResult("minimum_completeness", "FAIL", "null", f">= {COMPLETENESS_MIN:.2f}", "No completeness rate available")

    rate, year = row
    status = "PASS" if rate >= COMPLETENESS_MIN else "FAIL"
    detail = f"Latest completeness from year {year}"
    return CheckResult("minimum_completeness", status, f"{rate:.4f}", f">= {COMPLETENESS_MIN:.2f}", detail)


def check_failed_refresh_alerts(con: duckdb.DuckDBPyConnection) -> CheckResult:
    required = [
        ("analytics_marts", "mart_resilience_score"),
        ("analytics_marts", "mart_data_quality_status"),
        ("analytics_predictions", "pred_capacity_growth_forecast"),
    ]
    missing = [f"{s}.{t}" for s, t in required if not _safe_exists(con, s, t)]
    status = "PASS" if not missing else "FAIL"
    detail = "All required refresh outputs present" if not missing else f"Missing tables: {', '.join(missing)}"
    return CheckResult("failed_refresh_alerts", status, "0" if not missing else str(len(missing)), "0 missing", detail)


def check_row_count_anomaly(con: duckdb.DuckDBPyConnection) -> CheckResult:
    if not _safe_exists(con, "analytics_facts", "fct_regional_sector_capacity"):
        return CheckResult("row_count_anomaly", "FAIL", "missing", f"<= {ROW_DELTA_MAX_RATIO:.2f}", "Fact table missing")

    rows = con.execute(
        """
        select year, count(*) as row_count
        from analytics_facts.fct_regional_sector_capacity
        group by year
        order by year
        """
    ).fetchall()

    if len(rows) < 2:
        return CheckResult("row_count_anomaly", "PASS", "0.0000", f"<= {ROW_DELTA_MAX_RATIO:.2f}", "Not enough history to evaluate anomaly")

    latest_year, latest_count = rows[-1]
    _, prev_count = rows[-2]
    if prev_count == 0:
        return CheckResult("row_count_anomaly", "FAIL", "inf", f"<= {ROW_DELTA_MAX_RATIO:.2f}", "Previous year row count is zero")

    delta_ratio = abs(latest_count - prev_count) / prev_count
    status = "PASS" if delta_ratio <= ROW_DELTA_MAX_RATIO else "FAIL"
    detail = f"Row count comparison {latest_year} vs previous year"
    return CheckResult("row_count_anomaly", status, f"{delta_ratio:.4f}", f"<= {ROW_DELTA_MAX_RATIO:.2f}", detail)


def persist_monitoring(con: duckdb.DuckDBPyConnection, checks: list[CheckResult], run_status: str) -> None:
    con.execute("create schema if not exists analytics_monitoring")
    con.execute(
        """
        create table if not exists analytics_monitoring.pipeline_sla_checks (
            run_id varchar,
            run_timestamp_utc varchar,
            check_name varchar,
            status varchar,
            observed_value varchar,
            threshold_value varchar,
            detail varchar
        )
        """
    )

    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_ts = datetime.now(timezone.utc).isoformat()

    rows = [
        (run_id, run_ts, c.check_name, c.status, c.observed_value, c.threshold_value, c.detail)
        for c in checks
    ]

    con.executemany(
        """
        insert into analytics_monitoring.pipeline_sla_checks
        (run_id, run_timestamp_utc, check_name, status, observed_value, threshold_value, detail)
        values (?, ?, ?, ?, ?, ?, ?)
        """,
        rows,
    )

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    log_exists = LOG_PATH.exists()
    with LOG_PATH.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "run_timestamp_utc",
                "run_status",
                "checks_passed",
                "checks_failed",
                "freshness_threshold_days",
                "completeness_min",
                "row_delta_max_ratio",
            ],
        )
        if not log_exists:
            writer.writeheader()
        writer.writerow(
            {
                "run_timestamp_utc": run_ts,
                "run_status": run_status,
                "checks_passed": sum(1 for c in checks if c.status == "PASS"),
                "checks_failed": sum(1 for c in checks if c.status == "FAIL"),
                "freshness_threshold_days": FRESHNESS_THRESHOLD_DAYS,
                "completeness_min": COMPLETENESS_MIN,
                "row_delta_max_ratio": ROW_DELTA_MAX_RATIO,
            }
        )

    lines = [
        "# Pipeline SLA Report",
        "",
        f"Generated at (UTC): {run_ts}",
        f"Overall status: {run_status}",
        "",
        "| Check | Status | Observed | Threshold | Detail |",
        "| --- | --- | --- | --- | --- |",
    ]

    for c in checks:
        lines.append(
            f"| {c.check_name} | {c.status} | {c.observed_value} | {c.threshold_value} | {c.detail} |"
        )

    freshness_failed = any(c.check_name == "data_freshness" and c.status == "FAIL" for c in checks)
    completeness_failed = any(c.check_name == "minimum_completeness" and c.status == "FAIL" for c in checks)

    lines.extend([
        "",
        "## Alert Routing Note",
        "",
        "Use this lightweight routing rule to close the loop when SLA fails.",
    ])

    if freshness_failed:
        lines.extend([
            "",
            "- Freshness FAIL -> notify Data Engineer / Maintainer.",
            "- First action: run `python src/forecasting/phase8_capacity_growth_forecast.py` and re-run SLA monitor.",
        ])

    if completeness_failed:
        lines.extend([
            "",
            "- Completeness FAIL -> notify Data Engineer and Analytics Owner.",
            "- First action: run ingestion + dbt run/test, then review `analytics_marts.mart_data_quality_status`.",
        ])

    if not freshness_failed and not completeness_failed:
        lines.extend([
            "",
            "- No freshness/completeness failure in this run. Keep default daily monitoring.",
        ])

    MARKDOWN_REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    con = duckdb.connect(str(DUCKDB_PATH))
    try:
        checks = [
            check_freshness(con),
            check_completeness(con),
            check_failed_refresh_alerts(con),
            check_row_count_anomaly(con),
        ]
        run_status = "PASS" if all(c.status == "PASS" for c in checks) else "FAIL"
        persist_monitoring(con, checks, run_status)
    finally:
        con.close()

    failed = [c for c in checks if c.status == "FAIL"]
    print(f"SLA checks completed. Overall status: {run_status}")
    if failed:
        for c in failed:
            print(f"FAILED: {c.check_name} - {c.detail}")


if __name__ == "__main__":
    main()
