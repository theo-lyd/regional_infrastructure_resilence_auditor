# Current State, Capabilities, and Gaps

This document is the authoritative "implemented vs not implemented" checkpoint for this repository.

## 1. Current State Snapshot

Implemented and operational:
1. config-driven raw ingestion to DuckDB via source registry
2. layered dbt transformations (staging, intermediate, dimensions, facts, marts)
3. forecasting outputs with interpretable model and fallback mode
4. Streamlit stakeholder dashboard (multi-tab, filtered views)
5. Airflow orchestration and CI checks
6. SLA monitoring and alert routing guidance
7. initial dbt snapshot-based SCD Type 2 for core dimensions
8. domain-level data quality scorecard mart and dashboard visibility
9. docs sync CI guardrail and release governance baseline

Not implemented yet:
1. full ad-hoc query builder in the dashboard UI
2. user-defined metric builder in the dashboard UI
3. end-user what-if simulation form in the dashboard UI

## 2. Dashboard and Modeling UX Boundaries

Current dashboard strengths:
1. interactive year and region filtering
2. sortable table views via Streamlit dataframe interactions
3. metric help text and decision-oriented narrative view

Current UX boundaries:
1. no ad-hoc SQL interface for end-users
2. no drag-and-drop metric authoring
3. no interactive scenario controls for forecasting assumptions

## 3. SCD Capability

What exists now:
1. dbt project is configured with snapshot paths
2. active dbt snapshot models for `dim_region` and `dim_sector`
3. model design uses historical yearly snapshots in source fields

Current SCD Type 2 rollout boundary:
1. Type 2 tracking is currently implemented for selected dimensions only
2. additional dimensions still require snapshot expansion and policy decisions

Clarification on SCD Type 1:
1. SCD Type 1 is not explicitly modeled as a dedicated pattern either.
2. Current tables are rebuilt or replaced by pipeline runs and represent transformed historical records, not a formal Type 1 dimension-management implementation contract.

## 4. Alerting: How It Works

Implemented checks:
1. data freshness
2. minimum completeness
3. completeness regression
4. failed refresh output presence
5. row-count anomaly

Frequency:
1. daily through Airflow DAG schedule
2. on-demand when full launcher mode is used

Trigger conditions:
1. any check in FAIL state creates an incident candidate
2. thresholds are configurable via environment variables

Severity model (lightweight):
1. `failed_refresh_alerts`: critical
2. `data_freshness`: high
3. `minimum_completeness`: high
4. `completeness_regression`: medium
5. `row_count_anomaly`: medium

Dedupe and escalation:
1. notify on new incidents (PASS to FAIL transition)
2. suppress duplicate consecutive failures by default
3. escalate persistent failures every N consecutive runs (default N=2)
4. notify recovery when FAIL returns to PASS

## 5. Data Robustness for Public-Sector Inputs

Already robust:
1. raw-line preservation for auditability
2. source structure profiling (metadata/data/footer counts)
3. encoding integrity checks and mojibake detection
4. normalization macros for missing markers and varied numeric formats
5. quality marts and SLA checks expose completeness and anomalies

Current limitations:
1. onboarding new domains/formats still requires source + staging model extension
2. schema contracts currently enforce column-count ranges, not full semantic typing
3. XLSX support is adapter-level and still depends on upstream sheet quality assumptions

## 6. Handling New and Different Dataset Formats

CSV:
1. supported in current ingestion pattern for configured sources
2. additional CSV datasets require ingestion + dbt source/model extension

XLSX:
1. implemented in ingestion adapter through source registry format setting
2. requires explicit sheet/contract configuration before production use

Messy or poor data:
1. system is resilient to many common missing/format issues during transformation
2. incompatible schema drift still requires explicit engineering updates
3. poor-quality data is surfaced in quality marts and SLA artifacts for governance review

## 7. Final Verdict: UI Expansion Complexity

Ad-hoc query/metric builder complexity: high
1. requires semantic layer governance, guardrails, and performance controls
2. introduces data-trust and metric-definition drift risks
3. requires stronger UX, audit logging, and permission design

End-user what-if form complexity: medium-high
1. needs validated scenario inputs and bounded assumptions
2. requires explainable scenario outputs with uncertainty context
3. needs reproducibility and governance of scenario runs for policy defensibility

## 8. Recommendation Sequence

1. expand SCD snapshots to additional dimensions and publish dimensional SCD policy
2. expand alerting channels (email/Teams/webhook) using the existing severity + dedupe model
3. add controlled what-if form before full ad-hoc query builder
4. add semantic layer contracts before user-authored metrics
