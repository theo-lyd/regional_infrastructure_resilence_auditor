# Defense Q&A and Lessons Learned

## Sample Stakeholder Questions

1. Which regions are currently most underserved across all service domains?
Answer approach:
- use `mart_underserved_region_score` latest-year ranking
- cross-check with domain-specific tables to avoid one-domain bias

2. Is the current data quality good enough for policy use?
Answer approach:
- present `mart_data_quality_status` and completeness rate
- show SLA report from `data/reports/pipeline_sla_report.md`

3. Which regions are forecasted to face near-term pressure?
Answer approach:
- show `analytics_predictions.pred_capacity_growth_forecast`
- filter to `risk_band = high_risk`

4. How do we know this is reproducible and auditable?
Answer approach:
- point to dbt tests, CI workflow, Airflow DAG, and phase technical docs
- explain versioned business rules and predictable runbook sequence

5. What should policymakers do first after seeing the dashboard?
Answer approach:
- prioritize highest-risk and highest-underserved overlap regions
- assign domain leads by sector pressure type

6. Do we support ad-hoc query builders or user-authored metrics in the UI today?
Answer approach:
- no, not currently
- explain this as an intentional governance choice to prevent metric drift and uncontrolled query behavior in a public-sector context
- point to roadmap item in `docs/current_state_capabilities_and_gaps.md`

7. Do we support end-user what-if simulation forms today?
Answer approach:
- no, not currently
- explain that forecasting is operationally rerunnable but scenario authoring in UI requires stronger assumption validation and scenario traceability

8. Is SCD Type 2 implemented?
Answer approach:
- yes, for an initial scoped set of dimensions (`dim_region`, `dim_sector`)
- clarify that Type 2 rollout is active but not yet expanded to all candidate dimensions

## Data Lineage Explanation (Plain Language)

1. Source files are ingested unchanged into raw tables.
2. dbt staging and clean models standardize fields and values.
3. Intermediate models align sectors to a common regional-year grain.
4. Facts and marts compute policy-facing KPIs.
5. Forecasting adds near-term risk projection.
6. Dashboard and narrative layer translate metrics into action guidance.

## Lessons Learned

1. Interpretability beats complexity in public-sector stakeholder adoption.
2. Data quality visibility must be a first-class dashboard feature, not an appendix.
3. Separate Airflow and analytics virtual environments reduces operational conflicts.
4. Structured phase documentation dramatically improves defense readiness.
5. Forecasting needs explicit fallback behavior when historical supervision is limited.
6. Governance artifacts (rules, lineage, tests) are as important as model code.
7. Alert fatigue controls (severity plus dedupe/escalation) materially improve operational signal quality.
8. Explicitly documenting what is not yet implemented improves defense credibility.

## Interview Talking Points

1. Explain one technical tradeoff: transparent linear/score forecasting versus black-box models.
2. Explain one governance tradeoff: stricter normalization rules versus retaining source nuance.
3. Explain one operations tradeoff: daily orchestration cadence versus source publication frequency.
4. Demonstrate how SLA failures are detected and surfaced.
