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
python -m pip install -r requirements.txt -r requirements-dev.txt

if [[ "${AIRFLOW_ISOLATED:-0}" == "1" ]]; then
  echo "[Phase 2] Creating isolated Airflow environment (.venv-airflow)"
  python3 -m venv .venv-airflow
  . .venv-airflow/bin/activate
  python -m pip install --upgrade pip
  python -m pip install "apache-airflow>=2.10.0,<3.0"
fi

echo "[Phase 2] Bootstrap completed"
