# Dashboard Apps

## Executive Overview (Phase 8 / Batch D1)

App file:
- `reports/dashboards/executive_overview_app.py`

### What it shows

- latest regional average resilience score
- latest regional average service maturity
- top 10 underserved regions
- data quality status based on fact completeness

### Data sources

- `analytics_marts.mart_resilience_score`
- `analytics_marts.mart_underserved_region_score`
- `analytics_marts.mart_data_quality_status`

### Run

```bash
cd /workspaces/regional_infrastructure_resilence_auditor
source .venv/bin/activate
streamlit run reports/dashboards/executive_overview_app.py
```

### Notes

- Ensure dbt marts are built before running the app.
- The app reads `DUCKDB_PATH` from `.env` if present.
