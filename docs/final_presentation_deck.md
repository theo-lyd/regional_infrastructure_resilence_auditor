# Final Presentation Deck (Phase 11)

## Slide 1 — Title
- Regional Infrastructure Resilience Auditor
- Public-sector analytics engineering portfolio project

## Slide 2 — Problem
- Fragmented childcare, youth welfare, and hospital datasets
- No unified regional decision-support view
- Need proactive rather than reactive planning

## Slide 3 — Objectives
- Build reproducible data product
- Standardize heterogeneous inputs
- Deliver KPI and risk insights for policymakers

## Slide 4 — Data Sources
- 3 administrative CSV domains
- Regional and temporal heterogeneity
- Encoding and formatting inconsistency challenges

## Slide 5 — Architecture Overview
- Ingestion -> dbt layers -> marts -> forecasting -> dashboard -> SLA monitoring
- Diagram reference: `docs/architecture_diagrams.md`

## Slide 6 — Data Model
- Raw, staging, intermediate, dimensions, facts, marts
- Conformed grain: region x sector x year

## Slide 7 — KPI Framework
- Domain KPIs (childcare, youth, hospital)
- Cross-sector KPIs (maturity, underserved, resilience)
- Data-quality KPIs

## Slide 8 — Predictive Logic
- Target: capacity growth forecast
- Interpretable model with fallback strategy
- Risk band outputs for prioritization

## Slide 9 — Dashboard Views
- Executive overview
- Domain dashboards
- Cross-sector matrix
- Predictive risk ranking
- Policy narrative panel

## Slide 10 — Automation and Reliability
- Airflow daily DAG
- GitHub Actions CI
- SLA monitoring checks and pipeline logs

## Slide 11 — Key Findings (Latest)
- latest KPI year: 2020
- service maturity: 0.1439
- resilience: 0.0935
- data quality status: good, completeness 100%
- high-risk forecast rows: 471

## Slide 12 — Stakeholder Impact
- Faster prioritization of underserved areas
- Transparent evidence chain from source to dashboard
- Better confidence for cross-sector planning discussions

## Slide 13 — Limitations
- historical depth limitations
- source heterogeneity and publication variability
- forecasts are directional, not deterministic
- no end-user ad-hoc query/metric builder in current UI
- no end-user what-if scenario form in current UI
- dbt snapshot-based SCD Type 2 active for selected dimensions, with broader rollout pending

## Slide 14 — Lessons Learned
- interpretability drives adoption
- governance documentation is a product feature
- monitoring and SLA checks are essential for trust
- severity + dedupe/escalation alert rules reduce alert fatigue and improve triage focus

## Slide 15 — Next Steps
- richer predictive model comparison
- policy scenario simulation
- deeper benchmarking and external enrichment

## Appendix — Demo Checklist
- run pipeline
- verify tests and SLA status
- launch dashboard
- walk through executive to predictive tabs
