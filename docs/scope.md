# Scope Definition

## In Scope
- Childcare facility and approved-place capacity analysis
- Youth welfare service capacity analysis
- Hospital bed capacity and specialty concentration analysis
- Regional comparison by federal state and administrative area
- Historical trend analysis where data supports longitudinal views
- Predictive risk scoring and lightweight forecasting
- Policymaker-focused dashboarding and narrative outputs
- Automated ETL/ELT orchestration and quality monitoring

## Out of Scope
- Individual-level data processing (health, social, or personal)
- Route optimization and accessibility modeling
- Real-time event streaming pipelines
- Complex black-box machine learning
- Causal impact estimation and econometric policy claims
- Policy prescriptions not grounded in project evidence

## Evaluation Scope
The project is evaluated on reproducibility, transparency, data quality, and practical decision-support value:
- Reproducibility of ingestion and transformations
- Clarity and traceability of business rules
- Robustness of KPI outputs across domains and time
- Explainability of predictive risk outputs
- Usefulness for public-sector planning workflows

## Folder Conventions
- `data/raw/`: immutable source CSV files exactly as received
- `data/processed/`: intermediate processed extracts produced by scripts
- `data/reference/`: static mapping and standardization reference tables
- `src/`: Python ingestion, cleaning, and forecasting logic
- `dbt/`: SQL transformations, tests, snapshots, and reusable macros
- `airflow/`: DAG definitions and orchestration assets
- `reports/dashboards/`: dashboard app code and assets (Streamlit/Metabase exports)
- `reports/storytelling/`: narrative summaries and policy-facing writeups
- `docs/`: governance, methodology, KPI definitions, and assumptions
