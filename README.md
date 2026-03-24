# Regional Infrastructure Resilience Auditor

The Regional Infrastructure Resilience Auditor is a public-sector analytics engineering project that standardizes childcare, youth welfare, and hospital infrastructure data into a unified regional resilience intelligence layer for policy planning.

## Executive Objective

Build a reproducible analytics product that helps policymakers answer:
- Which regions are underserved across childcare, youth services, and hospital capacity?
- Where is capacity growth lagging over time?
- Which regions face increasing near-term service pressure?

## Target Users

- Public-sector analysts
- Regional planning teams
- Non-technical decision-makers using dashboards

## Core Stack

- DuckDB for analytical storage
- dbt for transformations, tests, and snapshots
- Python and SQL for ingestion, normalization, and forecasting
- Airflow for orchestration
- Streamlit/Metabase for dashboarding
- GitHub Actions for CI validation
- GitHub Codespaces for reproducible development

## Repository Structure

```text
.
├── .devcontainer/               # Codespaces/dev container setup
├── .github/workflows/           # CI/CD workflows
├── airflow/                     # Orchestration assets (DAGs, plugins)
├── data/
│   ├── raw/                     # Immutable source CSVs
│   ├── processed/               # Processed/intermediate extracts
│   └── reference/               # Mapping tables and standards
├── dbt/
│   ├── macros/
│   ├── models/
│   │   ├── staging/
│   │   ├── intermediate/
│   │   ├── dimensions/
│   │   ├── facts/
│   │   └── marts/
│   ├── seeds/
│   ├── snapshots/
│   └── tests/
├── docs/                        # Governance, scope, methodology
├── reports/
│   ├── dashboards/              # Dashboard app code/assets
│   └── storytelling/            # Policy-facing narratives
├── src/
│   ├── ingestion/
│   ├── cleaning/
│   ├── forecasting/
│   └── utils/
├── .env.example                 # Environment variable template
└── requirements.txt             # Single dependency manifest
```

## Governance Documents

- `docs/project_brief.md`
- `docs/scope.md`
- `docs/methodology.md`
- `docs/environment_setup.md`
- `docs/metabase_setup.md`

## Documentation Hub (Defense and Watchalong)

Use `docs/docs_index.md` as the primary navigation file.

Key companion docs include:
- phase deep-dives (`docs/phase_0_governance.md`, `docs/phase_1_repository_setup.md`, `docs/phase_2_environment_configuration.md`)
- modeling governance (`docs/grain_definition.md`, `docs/join_strategy.md`, `docs/formula_to_model_mapping.md`)
- source and rules (`docs/source_inventory.md`, `docs/standardization_business_rules.md`)
- stakeholder delivery (`docs/dashboard_question_bank.md`, `docs/thesis_report_outline.md`, `docs/final_handoff.md`)

## Technical Principles

1. Raw data stays raw.
2. Cleaning and normalization are fully reproducible.
3. Business rules are explicitly documented.
4. Transformations are version-controlled.
5. Dashboards must trace back to governed model outputs.

## Quick Start (Codespaces or Local)

1. Open this repository in GitHub Codespaces.
2. Let post-create setup run from `.devcontainer/post-create.sh`.
3. Copy environment template: `cp .env.example .env`.
4. Place source CSV files in `data/raw/`.
5. Build ingestion and transformation layers in `src/` and `dbt/`.
6. Serve dashboard prototypes from `reports/dashboards/`.

For detailed setup and troubleshooting, see `docs/environment_setup.md`.

## Current Implementation Status

- Phase 0 complete: project framing, KPI framework, methodology baseline.
- Phase 1 complete: repository scaffold, folder conventions, Codespaces setup.
- Phase 2 complete: reproducible environment provisioning and dependency manifests.

## Public-Sector Presentation Note

This project is intentionally documented for non-technical and technical audiences, including stakeholder review and defense use cases in Berlin.

## License

See `LICENSE`.
