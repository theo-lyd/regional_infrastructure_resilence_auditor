# Dashboard Apps

## Phase 9 Policy Dashboard

Primary app file:
- `reports/dashboards/policy_decision_dashboard.py`

Legacy Phase 8 app:
- `reports/dashboards/executive_overview_app.py`

### Phase 9 View Mapping

1. 9.1 Executive overview
- service maturity by region/year trend
- top underserved regions
- data quality status

2. 9.2 Domain dashboards
- childcare view
- youth welfare view
- hospital capacity view

3. 9.3 Cross-sector resilience
- matrix-style comparison across childcare, youth, and hospital capacities

4. 9.4 Predictive view
- forecasted pressure table
- risk band ranking

5. 9.5 Policy narrative
- interpretation annotations
- attention list for high-risk regions

### Interactivity

The Phase 9 dashboard is interactive (not static-only):
- global `Filter Year` control updates all views to a selected year context
- global `Filter Region` control narrows executive/domain/cross-sector/predictive outputs
- table views support in-UI sorting via Streamlit dataframe behavior
- KPI cards include metric help text; each tab includes a short metric guide caption
- executive tab includes baseline-vs-current comparison cards for maturity and resilience

### Predictive Model Operations

- Users can rerun the predictive model at any time with:
	- `python src/forecasting/phase8_capacity_growth_forecast.py`
- The full launcher also reruns forecasting automatically:
	- `scripts/run_system.sh full`
- Custom prediction scenarios are not yet exposed as dashboard controls.
- Custom predictions today require editing model inputs/assumptions and rerunning the forecast script.

### KPI Summary Views

- `analytics_marts.mart_kpi_summary_executive`
- `analytics_marts.mart_kpi_summary_domain`

### Screenshot Assets

Generated into:
- `reports/storytelling/screenshots/phase9_executive_overview.png`
- `reports/storytelling/screenshots/phase9_underserved_regions.png`
- `reports/storytelling/screenshots/phase9_predictive_risk.png`

Generation script:
- `src/forecasting/generate_phase9_screenshots.py`

### Run

```bash
cd /workspaces/regional_infrastructure_resilence_auditor
source .venv/bin/activate

# build relevant marts
dbt build --project-dir dbt --profiles-dir dbt --select mart_kpi_summary_executive mart_kpi_summary_domain mart_data_quality_status

# run predictive layer (required for predictive dashboard view)
python src/forecasting/phase8_capacity_growth_forecast.py

# launch dashboard
streamlit run reports/dashboards/policy_decision_dashboard.py

# generate screenshot assets
python src/forecasting/generate_phase9_screenshots.py
```

### Notes

- Ensure dbt and predictive outputs are refreshed before stakeholder demonstrations.
- The dashboard reads `DUCKDB_PATH` from `.env` when provided.
