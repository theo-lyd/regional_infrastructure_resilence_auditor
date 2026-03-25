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
COMPLETENESS_DROP_MAX = float(os.getenv("SLA_MAX_COMPLETENESS_DROP", "0.05"))
ESCALATION_EVERY_N_FAILS = int(os.getenv("SLA_ESCALATION_EVERY_N_FAILS", "2"))

CHECK_SEVERITY = {
    "data_freshness": "high",
    "minimum_completeness": "high",
    "completeness_regression": "medium",
    "failed_refresh_alerts": "critical",
    "row_count_anomaly": "medium",
}


@dataclass
class CheckResult:
    check_name: str
    status: str
    observed_value: str
    threshold_value: str
    detail: str


@dataclass
class AlertDecision:
    check_name: str
    status: str
    severity: str
    decision: str
    reason: str
    consecutive_failures: int
    is_notification: bool


def severity_for_check(check_name: str) -> str:
    return CHECK_SEVERITY.get(check_name, "medium")


def recent_statuses(con: duckdb.DuckDBPyConnection, check_name: str, limit: int = 8) -> list[str]:
    if not _safe_exists(con, "analytics_monitoring", "pipeline_sla_checks"):
        return []

    rows = con.execute(
        """
        select status
        from analytics_monitoring.pipeline_sla_checks
        where check_name = ?
        order by run_timestamp_utc desc
        limit ?
        """,
        [check_name, limit],
    ).fetchall()
    return [str(r[0]) for r in rows if r and r[0] is not None]


def build_alert_decisions(con: duckdb.DuckDBPyConnection, checks: list[CheckResult]) -> list[AlertDecision]:
    decisions: list[AlertDecision] = []

    for c in checks:
        severity = severity_for_check(c.check_name)
        history = recent_statuses(con, c.check_name)
        last_status = history[0] if history else None

        prev_consecutive_fails = 0
        for s in history:
            if s == "FAIL":
                prev_consecutive_fails += 1
            else:
                break

        if c.status == "FAIL":
            consecutive = prev_consecutive_fails + 1
            if last_status != "FAIL":
                decisions.append(
                    AlertDecision(
                        check_name=c.check_name,
                        status=c.status,
                        severity=severity,
                        decision="notify_new_incident",
                        reason="Status changed PASS->FAIL (or first observed run)",
                        consecutive_failures=consecutive,
                        is_notification=True,
                    )
                )
            elif ESCALATION_EVERY_N_FAILS > 0 and consecutive % ESCALATION_EVERY_N_FAILS == 0:
                decisions.append(
                    AlertDecision(
                        check_name=c.check_name,
                        status=c.status,
                        severity=severity,
                        decision="notify_escalation",
                        reason=f"Persistent failure reached {consecutive} consecutive runs",
                        consecutive_failures=consecutive,
                        is_notification=True,
                    )
                )
            else:
                decisions.append(
                    AlertDecision(
                        check_name=c.check_name,
                        status=c.status,
                        severity=severity,
                        decision="suppress_duplicate",
                        reason="Consecutive duplicate failure suppressed to reduce alert fatigue",
                        consecutive_failures=consecutive,
                        is_notification=False,
                    )
                )
        else:
            if last_status == "FAIL":
                decisions.append(
                    AlertDecision(
                        check_name=c.check_name,
                        status=c.status,
                        severity=severity,
                        decision="notify_recovery",
                        reason="Status changed FAIL->PASS",
                        consecutive_failures=0,
                        is_notification=True,
                    )
                )
            else:
                decisions.append(
                    AlertDecision(
                        check_name=c.check_name,
                        status=c.status,
                        severity=severity,
                        decision="no_alert",
                        reason="Healthy status with no active incident",
                        consecutive_failures=0,
                        is_notification=False,
                    )
                )

    return decisions


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


def check_completeness_regression(con: duckdb.DuckDBPyConnection) -> CheckResult:
    if not _safe_exists(con, "analytics_marts", "mart_data_quality_status"):
        return CheckResult(
            "completeness_regression",
            "FAIL",
            "missing",
            f"drop <= {COMPLETENESS_DROP_MAX:.2f}",
            "Data quality mart missing",
        )

    rows = con.execute(
        """
        select year, capacity_completeness_rate
        from analytics_marts.mart_data_quality_status
        where capacity_completeness_rate is not null
        order by year desc
        limit 2
        """
    ).fetchall()

    if len(rows) < 2:
        return CheckResult(
            "completeness_regression",
            "PASS",
            "0.0000",
            f"drop <= {COMPLETENESS_DROP_MAX:.2f}",
            "Not enough history to evaluate completeness regression",
        )

    latest_year, latest_rate = rows[0]
    prev_year, prev_rate = rows[1]
    drop = max(0.0, float(prev_rate) - float(latest_rate))
    status = "PASS" if drop <= COMPLETENESS_DROP_MAX else "FAIL"
    detail = f"Completeness comparison {prev_year}->{latest_year}"
    return CheckResult(
        "completeness_regression",
        status,
        f"{drop:.4f}",
        f"drop <= {COMPLETENESS_DROP_MAX:.2f}",
        detail,
    )


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


def persist_monitoring(
    con: duckdb.DuckDBPyConnection,
    checks: list[CheckResult],
    decisions: list[AlertDecision],
    run_status: str,
) -> None:
    con.execute("create schema if not exists analytics_monitoring")
    con.execute(
        """
        create table if not exists analytics_monitoring.pipeline_sla_checks (
            run_id varchar,
            run_timestamp_utc varchar,
            check_name varchar,
            status varchar,
            severity varchar,
            observed_value varchar,
            threshold_value varchar,
            detail varchar
        )
        """
    )

    con.execute("alter table analytics_monitoring.pipeline_sla_checks add column if not exists severity varchar")

    con.execute(
        """
        create table if not exists analytics_monitoring.pipeline_alert_events (
            run_id varchar,
            run_timestamp_utc varchar,
            check_name varchar,
            status varchar,
            severity varchar,
            decision varchar,
            reason varchar,
            consecutive_failures integer,
            is_notification boolean
        )
        """
    )

    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_ts = datetime.now(timezone.utc).isoformat()

    rows = [
        (
            run_id,
            run_ts,
            c.check_name,
            c.status,
            severity_for_check(c.check_name),
            c.observed_value,
            c.threshold_value,
            c.detail,
        )
        for c in checks
    ]

    con.executemany(
        """
        insert into analytics_monitoring.pipeline_sla_checks
        (run_id, run_timestamp_utc, check_name, status, severity, observed_value, threshold_value, detail)
        values (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        rows,
    )

    decision_rows = [
        (
            run_id,
            run_ts,
            d.check_name,
            d.status,
            d.severity,
            d.decision,
            d.reason,
            d.consecutive_failures,
            d.is_notification,
        )
        for d in decisions
    ]
    con.executemany(
        """
        insert into analytics_monitoring.pipeline_alert_events
        (run_id, run_timestamp_utc, check_name, status, severity, decision, reason, consecutive_failures, is_notification)
        values (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        decision_rows,
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
                    "completeness_drop_max",
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
                    "completeness_drop_max": COMPLETENESS_DROP_MAX,
            }
        )

    lines = [
        "# Pipeline SLA Report",
        "",
        f"Generated at (UTC): {run_ts}",
        f"Overall status: {run_status}",
        "",
        "| Check | Status | Severity | Observed | Threshold | Detail |",
        "| --- | --- | --- | --- | --- | --- |",
    ]

    for c in checks:
        lines.append(
            f"| {c.check_name} | {c.status} | {severity_for_check(c.check_name)} | {c.observed_value} | {c.threshold_value} | {c.detail} |"
        )

    lines.extend([
        "",
        "## Alert Decisions (Dedupe and Escalation)",
        "",
        "| Check | Status | Severity | Decision | Consecutive Fails | Notify | Reason |",
        "| --- | --- | --- | --- | ---: | --- | --- |",
    ])
    for d in decisions:
        lines.append(
            f"| {d.check_name} | {d.status} | {d.severity} | {d.decision} | {d.consecutive_failures} | {str(d.is_notification).lower()} | {d.reason} |"
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
            check_completeness_regression(con),
            check_failed_refresh_alerts(con),
            check_row_count_anomaly(con),
        ]
        decisions = build_alert_decisions(con, checks)
        run_status = "PASS" if all(c.status == "PASS" for c in checks) else "FAIL"
        persist_monitoring(con, checks, decisions, run_status)
    finally:
        con.close()

    failed = [c for c in checks if c.status == "FAIL"]
    notify_events = [d for d in decisions if d.is_notification]
    print(f"SLA checks completed. Overall status: {run_status}")
    print(f"Alert notifications emitted: {len(notify_events)}")
    if failed:
        for c in failed:
            print(f"FAILED: {c.check_name} - {c.detail}")


if __name__ == "__main__":
    main()
