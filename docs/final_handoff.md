# Final Handoff Checklist

## Purpose

Ensure another analyst or team can operate and defend the project without implicit knowledge.

## Handoff Artifacts

- governance docs complete and current
- environment setup validated in fresh Codespace
- dbt and pipeline run instructions documented
- dashboard question bank aligned with stakeholder priorities
- data dictionary and formula mapping up to date

## Operational Checklist

1. Confirm repository builds in a fresh environment.
2. Confirm all required environment variables are documented.
3. Confirm key models/tests run successfully.
4. Confirm dashboard reads from governed marts only.
5. Confirm SLA checks and alert expectations are defined.

## Knowledge Transfer Checklist

1. Explain project objective and policy use-case in plain language.
2. Explain data limitations and interpretation boundaries.
3. Explain KPI definitions and scoring logic.
4. Explain how to trace a dashboard metric back to its model.
5. Explain how to triage a failed pipeline run.

## Support Model

- owner: project maintainer
- escalation path: issue -> diagnosis -> fix PR -> CI validation -> release note
- update cadence: monthly quality review and quarterly KPI logic review

## One-Page Operator Runbook

### Startup Checks (Before Daily Use)

1. Confirm repository is synced and clean (`git status -sb`).
2. Confirm analytics environment is available (`source .venv/bin/activate`).
3. Confirm Airflow environment is available (`source .airflow-venv/bin/activate`) when scheduler operations are needed.
4. Confirm DuckDB file exists at `data/processed/regional_resilience.duckdb`.
5. Confirm latest raw files are present in `data/raw/`.

### Daily Run Steps (Manual Sequence)

1. Run raw ingestion:
	- `python src/ingest_raw_duckdb.py`
2. Run dbt transformations:
	- `dbt run --project-dir dbt --profiles-dir dbt`
3. Run dbt tests:
	- `dbt test --project-dir dbt --profiles-dir dbt`
4. Refresh predictive outputs:
	- `python src/forecasting/phase8_capacity_growth_forecast.py`
5. Emit dashboard refresh signal:
	- `python src/monitoring/dashboard_refresh_signal.py`
6. Run SLA checks:
	- `python src/monitoring/pipeline_sla_monitor.py`
7. (Optional) Refresh screenshots for stakeholder packs:
	- `python src/forecasting/generate_phase9_screenshots.py`

### Failure Checklist (Fast Triage)

1. If ingestion fails:
	- verify raw file names and encoding assumptions
	- inspect `data/reports/raw_ingestion_log.csv`
2. If dbt run/test fails:
	- run failing model/test selector locally
	- inspect `dbt/target/` compiled SQL for root cause
3. If forecast step fails:
	- verify required input tables exist in `analytics_intermediate` and `analytics_marts`
4. If dashboard appears stale:
	- check `data/reports/dashboard_refresh_signal.json` timestamp
5. If SLA fails:
	- inspect `data/reports/pipeline_sla_report.md`
	- inspect `data/reports/pipeline_run_log.csv`
	- query `analytics_monitoring.pipeline_sla_checks` for check-level details

### Who-Does-What (Lean Responsibility Map)

1. Data Engineer / Maintainer:
	- ingestion, dbt modeling/tests, CI upkeep, Airflow DAG health
2. Analytics Owner:
	- KPI logic review, dictionary updates, forecasting assumptions review
3. Stakeholder Liaison / Policy Analyst:
	- dashboard narrative quality, decision-note updates, interpretation guardrails
4. Escalation owner:
	- project maintainer coordinates incident triage and release communication
