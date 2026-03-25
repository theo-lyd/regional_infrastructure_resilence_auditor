# Shell Commands Reference Guide

This guide explains recurring shell commands used to run, validate, and operate this repository.

## 1. Environment Commands

`source .venv/bin/activate`
- Activates the analytics Python environment used for ingestion, dbt, forecasting, and dashboard operations.

`source .airflow-venv/bin/activate`
- Activates the Airflow-specific environment for scheduler/webserver and DAG runtime isolation.

## 2. Ingestion and Raw Validation

`python src/ingest_raw_duckdb.py`
- Loads configured raw CSV sources into DuckDB raw schema, preserving line-level content.

`python src/validate_raw_duckdb.py`
- Validates raw ingestion row counts and encoding integrity, then writes a markdown validation report.

## 3. dbt Transformation and Testing

`dbt run --project-dir dbt --profiles-dir dbt`
- Executes dbt model transformations into staging/intermediate/dimensions/facts/marts schemas.

`dbt test --project-dir dbt --profiles-dir dbt`
- Runs dbt tests for model quality and contract checks.

`dbt build --select models/dimensions models/intermediate models/marts`
- Builds selected model groups and executes associated tests.

`dbt compile --project-dir dbt --profiles-dir dbt`
- Compiles dbt SQL without executing models; useful for quick structural validation.

## 4. Forecasting and Dashboard Signals

`python src/forecasting/phase8_capacity_growth_forecast.py`
- Trains/executes forecasting logic and writes prediction outputs to DuckDB and CSV.

`python src/monitoring/dashboard_refresh_signal.py`
- Emits dashboard refresh metadata artifact indicating latest successful pipeline refresh timing.

## 5. Monitoring and SLA

`python src/monitoring/pipeline_sla_monitor.py`
- Runs SLA checks, persists monitoring records, and generates markdown/CSV reports.

## 6. Dashboard Launch

`streamlit run reports/dashboards/policy_decision_dashboard.py`
- Launches the Streamlit policy dashboard.

`scripts/run_system.sh full`
- Runs end-to-end refresh sequence and launches dashboard.

`scripts/run_system.sh frontend-only`
- Launches dashboard only, using existing prepared outputs.

`AUTO_OPEN_BROWSER=0 scripts/run_system.sh full`
- Runs full mode while disabling automatic browser opening.

## 7. Quality and Syntax Checks

`python -m py_compile <file.py>`
- Performs Python syntax validation for one or more modules.

`ruff check src/`
- Runs lint checks on source files.

## 8. Airflow Operations

`airflow dags list`
- Lists discoverable DAGs in the active Airflow environment.

`airflow dags test regional_resilience_daily_pipeline <date>`
- Executes a DAG test run for a specific execution date without full scheduler orchestration.

## 9. CI-Equivalent Smoke Sequence

1. `python src/ingest_raw_duckdb.py`
2. `dbt compile --project-dir dbt --profiles-dir dbt`
3. `dbt test --project-dir dbt --profiles-dir dbt`
4. `python src/forecasting/phase8_capacity_growth_forecast.py`
5. `python src/monitoring/pipeline_sla_monitor.py`

This sequence approximates major local checks performed before or alongside CI.

## 10. Git vs Shell Docs

- For Git-specific command explanations, use `docs/git_commands_reference.md`.
- This document focuses on shell/runtime commands for system operation.
