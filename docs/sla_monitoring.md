# SLA Monitoring Guide (Phase 10)

## Purpose

Define measurable service-level checks so the pipeline behaves like a production data product.

## SLA Checks Implemented

The script `src/monitoring/pipeline_sla_monitor.py` executes four checks.

1. Data freshness
- Measure: age of latest `generated_at_utc` in `analytics_predictions.pred_capacity_growth_forecast`
- Threshold: `SLA_MAX_PREDICTION_STALENESS_DAYS` (default `30`)

2. Minimum completeness
- Measure: latest `capacity_completeness_rate` from `analytics_marts.mart_data_quality_status`
- Threshold: `SLA_MIN_COMPLETENESS_RATE` (default `0.85`)

3. Failed refresh alerts
- Measure: presence of required output tables
- Required tables:
  - `analytics_marts.mart_resilience_score`
  - `analytics_marts.mart_data_quality_status`
  - `analytics_predictions.pred_capacity_growth_forecast`

4. Row-count anomalies
- Measure: absolute year-over-year row-count delta ratio for `analytics_facts.fct_regional_sector_capacity`
- Threshold: `SLA_MAX_ROWCOUNT_DELTA_RATIO` (default `0.25`)

## Monitoring Outputs

1. DuckDB monitoring table
- `analytics_monitoring.pipeline_sla_checks`
- Contains run id, check name, status, observed value, threshold, and details

2. Pipeline run log CSV
- `data/reports/pipeline_run_log.csv`
- Contains one row per monitoring run with counts of passed/failed checks

3. Markdown SLA report
- `data/reports/pipeline_sla_report.md`
- Human-readable summary for stakeholder review

## Threshold Configuration

Configure through `.env` values:

```bash
SLA_MAX_PREDICTION_STALENESS_DAYS=30
SLA_MIN_COMPLETENESS_RATE=0.85
SLA_MAX_ROWCOUNT_DELTA_RATIO=0.25
```

## Alert Interpretation

- `PASS`: observed value satisfies threshold.
- `FAIL`: observed value violates threshold or required table is missing.
- Failures are logged to DuckDB and included in CSV/Markdown outputs.

## Severity Model (Lightweight)

- `failed_refresh_alerts`: `critical`
- `data_freshness`: `high`
- `minimum_completeness`: `high`
- `row_count_anomaly`: `medium`

Severity is persisted with each check result and used for triage priority in monitoring outputs.

## Dedupe and Escalation Rules

Implemented anti-fatigue logic:

1. New incident notification:
- Trigger when a check transitions from `PASS` to `FAIL`.

2. Duplicate suppression:
- Consecutive duplicate failures are suppressed by default to reduce noisy repeat alerts.

3. Escalation:
- Persistent failures are escalated every `N` consecutive runs.
- Config: `SLA_ESCALATION_EVERY_N_FAILS` (default `2`).

4. Recovery notification:
- Trigger when a check transitions from `FAIL` to `PASS`.

Persisted artifacts:
- `analytics_monitoring.pipeline_alert_events` (decision and notification tracking)
- markdown report section `Alert Decisions (Dedupe and Escalation)`

## Alert Routing (When Freshness/Completeness Fails)

Keep routing lightweight and deterministic.

1. If `data_freshness` fails:
- notify: Data Engineer / Maintainer (primary)
- first action: run forecast refresh (`python src/forecasting/phase8_capacity_growth_forecast.py`) and re-run SLA monitor

2. If `minimum_completeness` fails:
- notify: Data Engineer and Analytics Owner
- first action: run ingestion + dbt run/test to confirm source/model integrity, then review latest completeness in `analytics_marts.mart_data_quality_status`

3. If either fails repeatedly for 2 runs:
- notify: Stakeholder Liaison / Policy Analyst
- first action: mark dashboard outputs as "review required" until SLA returns PASS

## Operational Usage

Manual run:

```bash
cd /workspaces/regional_infrastructure_resilence_auditor
source .venv/bin/activate
python src/monitoring/pipeline_sla_monitor.py
```

Scheduled run:
- Triggered as final task in Airflow DAG `regional_resilience_daily_pipeline`.
