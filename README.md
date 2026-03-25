# Regional Infrastructure Resilience Auditor

## Problem

Regional planning teams need a single, trusted decision-support layer to identify underserved areas across childcare, youth welfare, and hospital capacity. In practice, source data is fragmented, mixed-format, and hard to compare across domains and time.

This project turns those fragmented administrative data sources into a reproducible analytics product with traceable KPIs, forecasting outputs, and stakeholder-facing dashboards.

## Data Sources

Current source files (immutable raw inputs) are maintained in `data/raw/`:

- `22541-01-01-4.csv` (childcare)
- `22542-01-02-4.csv` (youth welfare)
- `23111-01-04-4.csv` (hospital capacity)

Detailed inventory and caveats are documented in `docs/source_inventory.md`.

## Stack

- Storage and query engine: DuckDB
- Transformation and data contracts: dbt + dbt tests
- Processing scripts: Python + SQL
- Forecasting: interpretable regression/score-based logic
- Orchestration: Airflow (dedicated `.airflow-venv`)
- CI/CD: GitHub Actions
- Decision layer: Streamlit dashboards (Metabase-compatible data layer)
- Reproducible dev environment: GitHub Codespaces + devcontainer

## Architecture

Layered architecture:

1. Raw ingestion (`src/ingest_raw_duckdb.py`) into `raw.*`
2. Staging normalization (`dbt/models/staging/`)
3. Intermediate harmonization (`dbt/models/intermediate/`)
4. Dimensional and fact modeling (`dbt/models/dimensions/`, `dbt/models/facts/`)
5. Decision marts (`dbt/models/marts/`)
6. Forecasting outputs (`analytics_predictions.*`)
7. Dashboard and narrative delivery (`reports/dashboards/`)
8. Monitoring and SLA checks (`src/monitoring/`, `analytics_monitoring.*`)

See complete diagrams and lineage in `docs/architecture_diagrams.md`.

## How To Run

### 1. Environment setup

```bash
cp .env.example .env
source .venv/bin/activate
```

For full setup details (including Airflow environment separation), see `docs/environment_setup.md`.

### 2. Pipeline run (manual sequence)

```bash
python src/ingest_raw_duckdb.py
dbt run --project-dir dbt --profiles-dir dbt
dbt test --project-dir dbt --profiles-dir dbt
python src/forecasting/phase8_capacity_growth_forecast.py
python src/monitoring/dashboard_refresh_signal.py
python src/monitoring/pipeline_sla_monitor.py
```

### 3. Dashboard run

```bash
streamlit run reports/dashboards/policy_decision_dashboard.py
```

### 4. Airflow orchestration

```bash
source .airflow-venv/bin/activate
AIRFLOW_HOME=/workspaces/regional_infrastructure_resilence_auditor/airflow airflow db init
AIRFLOW_HOME=/workspaces/regional_infrastructure_resilence_auditor/airflow AIRFLOW__CORE__DAGS_FOLDER=/workspaces/regional_infrastructure_resilence_auditor/airflow/dags airflow dags list
```

## Key Findings Snapshot (Latest Run)

From latest generated outputs:

- Latest KPI year: `2020`
- Average service maturity: `0.1439`
- Average resilience score: `0.0935`
- Data quality status: `good`
- Capacity completeness: `100%`
- Forecast high-risk region-sector rows: `471`

Example top underserved regions (latest year):

- Landkreis Ludwigslust
- Kelheim, Landkreis
- Ostvorpommern, Landkreis
- Stralsund, Hansestadt, kreisfreie Stadt
- Zwickau, kreisfreie Stadt

## Dashboard Assets

Phase 9 screenshot assets:

- `reports/storytelling/screenshots/phase9_executive_overview.png`
- `reports/storytelling/screenshots/phase9_underserved_regions.png`
- `reports/storytelling/screenshots/phase9_predictive_risk.png`

## Documentation For Defense and Interview

Primary navigation: `docs/docs_index.md`

Phase 11 defense package:

- methodology chapter: `docs/thesis_methodology_chapter.md`
- final presentation deck (markdown): `docs/final_presentation_deck.md`
- architecture and KPI diagrams: `docs/architecture_diagrams.md`
- defense Q&A and lessons learned: `docs/defense_qa_and_lessons.md`

## Phase Status

- Phase 0 to Phase 10 completed.
- Phase 11 completed: documentation, defense, and portfolio packaging.

## License

See `LICENSE`.
