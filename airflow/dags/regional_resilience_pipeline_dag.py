"""Phase 10 Airflow DAG for production-like orchestration."""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

from airflow import DAG
from airflow.operators.bash import BashOperator


PROJECT_ROOT = Path("/workspaces/regional_infrastructure_resilence_auditor")
PYTHON_ANALYTICS = PROJECT_ROOT / ".venv" / "bin" / "python"
DBT_BIN = PROJECT_ROOT / ".venv" / "bin" / "dbt"


default_args = {
    "owner": "regional_resilience_team",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=10),
}

with DAG(
    dag_id="regional_resilience_daily_pipeline",
    default_args=default_args,
    description="Daily orchestration for ingestion, dbt transforms, forecasting, SLA checks, and dashboard signals",
    start_date=datetime(2025, 1, 1),
    schedule="0 6 * * *",
    catchup=False,
    max_active_runs=1,
    tags=["regional", "resilience", "phase10"],
) as dag:
    ingest_raw = BashOperator(
        task_id="ingest_raw_data",
        bash_command=f"cd {PROJECT_ROOT} && {PYTHON_ANALYTICS} src/ingest_raw_duckdb.py",
    )

    dbt_run = BashOperator(
        task_id="dbt_run_models",
        bash_command=(
            f"cd {PROJECT_ROOT}/dbt && "
            f"DBT_PROFILES_DIR={PROJECT_ROOT}/dbt "
            f"DBT_DUCKDB_PATH={PROJECT_ROOT}/data/processed/regional_resilience.duckdb "
            f"{DBT_BIN} run"
        ),
    )

    dbt_test = BashOperator(
        task_id="dbt_test_models",
        bash_command=(
            f"cd {PROJECT_ROOT}/dbt && "
            f"DBT_PROFILES_DIR={PROJECT_ROOT}/dbt "
            f"DBT_DUCKDB_PATH={PROJECT_ROOT}/data/processed/regional_resilience.duckdb "
            f"{DBT_BIN} test"
        ),
    )

    model_refresh = BashOperator(
        task_id="refresh_predictive_models",
        bash_command=f"cd {PROJECT_ROOT} && {PYTHON_ANALYTICS} src/forecasting/phase8_capacity_growth_forecast.py",
    )

    dashboard_refresh_signal = BashOperator(
        task_id="emit_dashboard_refresh_signal",
        bash_command=f"cd {PROJECT_ROOT} && {PYTHON_ANALYTICS} src/monitoring/dashboard_refresh_signal.py",
    )

    sla_checks = BashOperator(
        task_id="pipeline_sla_checks",
        bash_command=f"cd {PROJECT_ROOT} && {PYTHON_ANALYTICS} src/monitoring/pipeline_sla_monitor.py",
    )

    ingest_raw >> dbt_run >> dbt_test >> model_refresh >> dashboard_refresh_signal >> sla_checks
