#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MODE="${1:-full}"
AUTO_OPEN_BROWSER="${AUTO_OPEN_BROWSER:-1}"
APP_URL="http://localhost:8501"

PYTHON_BIN="${ROOT_DIR}/.venv/bin/python"
DBT_BIN="${ROOT_DIR}/.venv/bin/dbt"
STREAMLIT_BIN="${ROOT_DIR}/.venv/bin/streamlit"

if [[ ! -x "${PYTHON_BIN}" || ! -x "${DBT_BIN}" || ! -x "${STREAMLIT_BIN}" ]]; then
  echo "Missing analytics environment binaries."
  echo "Expected: ${PYTHON_BIN}, ${DBT_BIN}, ${STREAMLIT_BIN}"
  echo "Run environment setup first (see docs/environment_setup.md)."
  exit 1
fi

cd "${ROOT_DIR}"

run_full_refresh() {
  echo "[1/6] Ingesting raw data"
  "${PYTHON_BIN}" src/ingest_raw_duckdb.py

  echo "[2/6] Running dbt transformations"
  "${DBT_BIN}" run --project-dir dbt --profiles-dir dbt

  echo "[3/6] Running dbt tests"
  "${DBT_BIN}" test --project-dir dbt --profiles-dir dbt

  echo "[4/6] Refreshing predictive outputs"
  "${PYTHON_BIN}" src/forecasting/phase8_capacity_growth_forecast.py

  echo "[5/6] Emitting dashboard refresh signal"
  "${PYTHON_BIN}" src/monitoring/dashboard_refresh_signal.py

  echo "[6/6] Running SLA checks"
  "${PYTHON_BIN}" src/monitoring/pipeline_sla_monitor.py
}

launch_dashboard() {
  echo "Launching policy dashboard at ${APP_URL}"

  if [[ "${AUTO_OPEN_BROWSER}" == "1" ]]; then
    (
      sleep 2
      if [[ -n "${BROWSER:-}" ]]; then
        "${BROWSER}" "${APP_URL}" >/dev/null 2>&1 || true
      elif command -v xdg-open >/dev/null 2>&1; then
        xdg-open "${APP_URL}" >/dev/null 2>&1 || true
      elif command -v open >/dev/null 2>&1; then
        open "${APP_URL}" >/dev/null 2>&1 || true
      fi
    ) &
  fi

  exec "${STREAMLIT_BIN}" run reports/dashboards/policy_decision_dashboard.py
}

case "${MODE}" in
  full)
    echo "Mode: full (refresh pipeline + launch dashboard)"
    run_full_refresh
    launch_dashboard
    ;;
  frontend-only)
    echo "Mode: frontend-only (launch dashboard with existing data)"
    launch_dashboard
    ;;
  *)
    echo "Unknown mode: ${MODE}"
    echo "Usage: scripts/run_system.sh [full|frontend-only]"
    exit 1
    ;;
esac
