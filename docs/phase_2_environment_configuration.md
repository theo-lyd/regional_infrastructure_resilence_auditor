# Phase 2: Environment Configuration

## Purpose

Phase 2 ensures that any contributor can reproduce the same runtime setup with minimal friction.
For public-sector analytics, reproducibility is mandatory for trust and audit.

## What Was Implemented

- `.devcontainer/devcontainer.json` for Codespaces/devcontainer standardization
- `.devcontainer/post-create.sh` bootstrap script
- `requirements.txt` runtime dependency manifest
- `requirements-dev.txt` development dependency manifest
- `.env.example` environment variable template
- `environment_setup.md` operational setup instructions

## How It Was Implemented

1. Configure devcontainer to run a script-based bootstrap.
2. Bootstrap script creates `.venv`, upgrades pip tooling, installs dependencies.
3. Add optional Airflow isolation (`.venv-airflow`) using `AIRFLOW_ISOLATED=1`.
4. Separate runtime and developer-only dependencies.
5. Provide novice-friendly setup and validation commands.

## Why It Matters

- eliminates environment drift between local and Codespaces setups
- improves onboarding reliability for new team members
- reduces hidden dependency failures in CI/CD
- gives stakeholders confidence that outputs can be reproduced

## Often-Overlooked Details

- Airflow dependency trees may conflict with analytics libraries.
- Scripts must be executable (`chmod +x`) in repository context.
- `.env.example` should never contain real secrets.
- dependency ranges should be pinned tightly enough for stability but flexible enough for security patch updates.

## Codespaces Constraints and Mitigations

- limited CPU/RAM: avoid unnecessary heavyweight startup tasks
- limited storage: keep raw extracts curated and avoid giant temporary files
- startup latency: move expensive optional setup behind toggles
- ephemeral environments: keep setup scripted and idempotent

## Evidence Checklist (Defense Ready)

- Can a fresh Codespace install all dependencies automatically?
- Can a local user reproduce setup using documented commands?
- Are environment assumptions explicit in version control?
- Is optional Airflow isolation documented for conflict handling?

## Exit Criteria for Phase Completion

- all Phase 2 deliverables committed
- bootstrap script syntactically valid
- setup guide available in docs
- dependency manifests separated by purpose
