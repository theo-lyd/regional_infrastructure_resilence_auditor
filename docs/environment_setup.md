# Environment Setup Guide (Phase 2)

This guide explains how to reproduce the development environment for the Regional Infrastructure Resilience Auditor.

Audience:
- novice contributors who need clear, step-by-step instructions
- reviewers and public-sector stakeholders who need reproducibility evidence

## Why this matters

For a policy-facing analytics product, reproducibility is a governance requirement, not only a developer convenience.

This setup ensures:
- consistent package versions across contributors
- stable project structure in GitHub Codespaces
- auditable environment assumptions for project defense and handover

## Deliverables created in Phase 2

- `.devcontainer/devcontainer.json`
- `.devcontainer/post-create.sh`
- `requirements.txt`
- `requirements-airflow.txt`
- `requirements-dev.txt`
- `.env.example`

## Prerequisites

- GitHub account with access to this repository
- GitHub Codespaces enabled (recommended)
- or local machine with Python 3.11 and `venv`

## Option A (recommended): GitHub Codespaces

1. Open the repository in GitHub.
2. Click **Code** > **Codespaces** > **Create codespace on master**.
3. Wait for container startup.
4. The post-create script runs automatically:
   - upgrades pip tooling
   - creates `.venv` (dbt/DuckDB/analytics)
   - creates `.airflow_venv` (Airflow only)
   - installs dependencies from dedicated manifests

Validation checks in terminal:

```bash
source .venv/bin/activate
python --version
pip list | grep -E "duckdb|pandas|dbt-duckdb|streamlit"

source .airflow_venv/bin/activate
python --version
pip list | grep -E "apache-airflow"
```

## Option B: local setup

Run from repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt -r requirements-dev.txt

python3 -m venv .airflow_venv
source .airflow_venv/bin/activate
pip install --upgrade pip
pip install -r requirements-airflow.txt

cp .env.example .env
```

## Environment usage convention

- Use `.venv` for ingestion, cleaning, dbt, forecasting, and dashboard development.
- Use `.airflow_venv` only for Airflow scheduler/webserver/DAG tooling.

This separation prevents package conflicts and improves reproducibility.

## Environment variables

1. Copy template:

```bash
cp .env.example .env
```

2. Review key variables:
- `DUCKDB_PATH`: location of analytical DuckDB file
- `DBT_PROFILES_DIR`: dbt profile directory
- `AIRFLOW_HOME`: base Airflow metadata/log path

## Codespaces constraints and practical notes

- Codespaces has finite CPU/RAM and storage; avoid large temporary artifacts in repository root.
- Keep raw source data in `data/raw/` and avoid committing personal/local test dumps.
- Airflow installs are isolated in `.airflow_venv` to avoid dependency drift with analytics tooling.
- Pin dependency ranges in manifests to reduce "works on my machine" issues.

## Industry-standard practices applied

- environment provisioning scripted in version control
- runtime and dev dependencies separated
- airflow dependencies separated from analytics dependencies
- env vars templated with `.env.example`
- deterministic component isolation for orchestrator conflicts
- reproducible onboarding instructions for future contributors

## Public-sector stakeholder defense notes (Berlin presentation)

When defending this phase, emphasize:
- reproducibility: any reviewer can recreate the same toolchain
- auditability: setup assumptions are explicit and documented
- maintainability: environment bootstrap is automated and versioned
- risk control: Airflow is always isolated to protect analytics environment stability
