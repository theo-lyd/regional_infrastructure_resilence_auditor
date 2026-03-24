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
   - creates `.venv`
   - installs `requirements.txt` and `requirements-dev.txt`

Validation checks in terminal:

```bash
source .venv/bin/activate
python --version
pip list | grep -E "duckdb|pandas|dbt-duckdb|airflow|streamlit"
```

## Option B: local setup

Run from repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt -r requirements-dev.txt
cp .env.example .env
```

## Optional: isolate Airflow (recommended if package conflicts appear)

Airflow can have stricter dependency constraints than analytics libraries.
If you encounter dependency clashes, isolate Airflow into `.venv-airflow`.

### In Codespaces

Set in `.env`:

```bash
AIRFLOW_ISOLATED=1
```

Re-run bootstrap:

```bash
bash .devcontainer/post-create.sh
```

### Manual local isolation

```bash
python3 -m venv .venv-airflow
source .venv-airflow/bin/activate
pip install --upgrade pip
pip install "apache-airflow>=2.10.0,<3.0"
```

## Environment variables

1. Copy template:

```bash
cp .env.example .env
```

2. Review key variables:
- `DUCKDB_PATH`: location of analytical DuckDB file
- `DBT_PROFILES_DIR`: dbt profile directory
- `AIRFLOW_HOME`: base Airflow metadata/log path
- `AIRFLOW_ISOLATED`: toggle for separate Airflow venv during bootstrap

## Codespaces constraints and practical notes

- Codespaces has finite CPU/RAM and storage; avoid large temporary artifacts in repository root.
- Keep raw source data in `data/raw/` and avoid committing personal/local test dumps.
- Heavy Airflow installs can slow first boot; use isolated mode only when needed.
- Pin dependency ranges in manifests to reduce "works on my machine" issues.

## Industry-standard practices applied

- environment provisioning scripted in version control
- runtime and dev dependencies separated
- env vars templated with `.env.example`
- optional component isolation for orchestrator conflicts
- reproducible onboarding instructions for future contributors

## Public-sector stakeholder defense notes (Berlin presentation)

When defending this phase, emphasize:
- reproducibility: any reviewer can recreate the same toolchain
- auditability: setup assumptions are explicit and documented
- maintainability: environment bootstrap is automated and versioned
- risk control: Airflow can be isolated without blocking analytics development
