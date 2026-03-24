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

echo "[Phase 2] Creating isolated Airflow environment (.airflow_venv)"
python3 -m venv .airflow_venv
. .airflow_venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-airflow.txt

echo "[Phase 2] Bootstrap completed"
