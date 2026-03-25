# System Launch Modes

This guide defines how to launch the system for technical and non-technical users.

## Quick Options

1. Full refresh plus UI:
- `scripts/run_system.sh full`

2. Frontend-only UI:
- `scripts/run_system.sh frontend-only`

3. Clickable launchers (Linux desktop environments):
- `scripts/launch_full_system.desktop`
- `scripts/launch_frontend.desktop`

## What Each Mode Does

### Full mode

Runs, in order:
1. ingestion
2. dbt run
3. dbt test
4. predictive refresh
5. dashboard refresh signal
6. SLA checks
7. dashboard launch

This is best for technical demonstrations and latest-output assurance.

### Frontend-only mode

Runs only:
1. dashboard launch

This is best for non-technical stakeholder demos where backend details are not needed.

## Airflow, SLA, and Alerts Behavior

- This launcher executes the pipeline directly (manual orchestration path), then launches Streamlit.
- It does not start Airflow scheduler/webserver automatically.
- SLA checks are executed in full mode via `src/monitoring/pipeline_sla_monitor.py`.
- Alert-routing guidance is captured in `docs/sla_monitoring.md` and reflected in `data/reports/pipeline_sla_report.md`.

## Recommended Usage By Persona

1. Technical user:
- use full mode to guarantee fresh data and tested outputs before UI interaction.

2. Non-technical/public-sector user:
- use frontend-only launcher for immediate dashboard interaction with prepared outputs.
