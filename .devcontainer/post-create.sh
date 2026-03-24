#!/usr/bin/env bash
set -euo pipefail

# Reproducible bootstrap for Codespaces and local dev containers.
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "[Phase 2] Upgrading pip tooling"
python3 -m pip install --upgrade pip setuptools wheel

echo "[Phase 2] Creating project virtual environment (.venv)"
python3 -m venv .venv

echo "[Phase 2] Installing core and developer dependencies"
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo "[Phase 2] Creating isolated Airflow environment (.airflow-venv)"
python3 -m venv .airflow-venv
. .airflow-venv/bin/activate
python -m pip install --upgrade pip
python -m pip install "apache-airflow>=2.10.0,<3.0"

echo "[Phase 2] Creating Airflow project structure"
mkdir -p airflow/dags airflow/logs airflow/plugins

echo "[Phase 2] Persisting Airflow environment variables"
if ! grep -q "AIRFLOW_HOME=.*\/airflow" ~/.bashrc; then
	cat <<'EOF' >> ~/.bashrc

# Airflow project-scoped config
export AIRFLOW_HOME=$(pwd)/airflow
export AIRFLOW__CORE__LOAD_EXAMPLES=False
EOF
fi

echo "[Phase 2] Bootstrap completed"
