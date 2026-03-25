# Interview Question Bank With Suggested Answers

This guide provides business, theoretical, and technical/implementation interview questions and concise answer patterns tailored to this project.

## A. Business and Public-Sector Questions

### 1. What business problem does this project solve?
Suggested answer:
- It consolidates fragmented childcare, youth welfare, and hospital infrastructure data into one comparable regional decision-support layer. The product helps policymakers prioritize underserved areas, detect pressure trends, and act earlier.

### 2. Why is this valuable for public-sector stakeholders?
Suggested answer:
- Public agencies often operate in data silos. This project creates shared indicators and traceable evidence from source to dashboard, improving coordination, transparency, and defensibility in planning decisions.

### 3. How do you prevent misleading policy conclusions?
Suggested answer:
- By documenting assumptions and limits explicitly, exposing data quality status directly in dashboards, and using interpretable KPIs/forecasting rather than opaque black-box models.

### 4. What are key findings from your latest run?
Suggested answer:
- Latest KPI year is 2020, average service maturity is about 0.1439, resilience about 0.0935, data quality status is good with 100% capacity completeness, and forecast output flags 471 high-risk region-sector rows for attention.

### 5. What policy action can this enable immediately?
Suggested answer:
- Rapid triage: identify overlap between high underserved score and high forecast risk, then prioritize those regions for capacity planning review by sector leads.

## B. Theoretical and Methodology Questions

### 6. Why did you choose a layered data model?
Suggested answer:
- It separates concerns: raw integrity, standardized staging, reusable intermediate logic, conformed analytical entities, and decision marts. This increases maintainability, testability, and explainability.

### 7. How do you define and preserve data lineage?
Suggested answer:
- Every dashboard metric maps to a dbt model and upstream dependencies. We maintain documented lineage and deterministic transformations so each value can be traced back to source artifacts.

### 8. Why prioritize interpretability in prediction?
Suggested answer:
- In public-sector settings, trust and explainability matter more than marginal accuracy gains. Interpretable models support stakeholder buy-in, governance review, and practical deployment.

### 9. How do you evaluate model usefulness beyond fit statistics?
Suggested answer:
- We combine trend fit/directional checks with business usefulness criteria: can the output rank risk and trigger actionable follow-up with clear threshold logic?

### 10. What are the main methodological limitations?
Suggested answer:
- Limited historical depth for supervised forecasting, source heterogeneity across sectors, and composite KPI simplification. Forecast outputs are directional support, not deterministic truth.

## C. Technical and Implementation Questions

### 11. Why DuckDB + dbt for this project?
Suggested answer:
- DuckDB enables fast local analytics and reproducibility in Codespaces. dbt provides transformation modularity, tests, and contract-like model governance suitable for a production-style workflow.

### 12. How do you ensure reproducibility?
Suggested answer:
- Versioned code/config/docs, deterministic scripts, explicit environment setup, dbt tests, CI checks, and phase-by-phase technical implementation records.

### 13. How is orchestration handled?
Suggested answer:
- Airflow DAG schedules ingestion, dbt run, dbt test, predictive refresh, dashboard refresh signal, and SLA checks in a controlled sequence.

### 14. Why split `.venv` and `.airflow-venv`?
Suggested answer:
- It prevents dependency conflicts and keeps orchestration runtime isolated, while analytics/dbt scripts stay stable in the analytics environment.

### 15. What does CI/CD validate?
Suggested answer:
- Linting, Python syntax checks, dbt compile, and dbt tests. This catches structural regressions before merge/deploy.

### 16. What SLA checks are implemented?
Suggested answer:
- Data freshness, minimum completeness, failed refresh output presence, and row-count anomaly thresholds. Outputs are persisted in monitoring table/log/report artifacts.

### 17. How do dashboards stay synchronized with pipeline runs?
Suggested answer:
- Pipeline emits a dashboard refresh signal artifact after model refresh and then executes SLA checks; dashboard consumes updated governed marts/prediction tables.

### 18. How would you scale this to more domains?
Suggested answer:
- Extend source inventory and normalization mappings, add sector-specific cleaned staging and intermediate models, enforce tests/lineage contracts, and fold into conformed marts and dashboard tabs.

## D. Senior Professional Challenge Questions

### 19. What tradeoff did you make that you would revisit with more time?
Suggested answer:
- We prioritized interpretability and operational readiness over sophisticated forecasting; with more history and resources I would benchmark additional models while preserving explainability.

### 20. How would you harden this for production beyond current state?
Suggested answer:
- Add secrets management, environment-specific deployment config, alert routing (email/Teams), richer anomaly detection, and scheduled dashboard export/reporting workflows.

### 21. How do you handle schema drift in source files?
Suggested answer:
- Add source structure checks and contract tests in ingestion/staging, fail pipeline on incompatible drift, and route alert with explicit drift report.

### 22. How would you quantify policy impact?
Suggested answer:
- Define baseline intervention latency and targeting precision before deployment, then compare post-deployment improvements in prioritization speed and allocation quality.

### 23. Do we already support end-user ad-hoc query and custom metric builders?
Suggested answer:
- Not yet. The dashboard currently supports guided filtering/sorting and governed KPI views. Full ad-hoc querying and user-defined metric authoring are intentionally deferred because they require semantic governance, security guardrails, and stronger performance controls.

### 24. Do we already support end-user what-if simulation forms?
Suggested answer:
- Not yet in the dashboard UI. Forecasting can be rerun operationally, but interactive scenario editing is deferred until assumption validation, explainability controls, and scenario audit logging are implemented.

### 25. Is SCD Type 2 active in this project today?
Suggested answer:
- Yes, in an initial scoped rollout. dbt snapshot models are active for selected dimensions (`dim_region`, `dim_sector`). Additional dimensions remain roadmap candidates for broader Type 2 coverage.

### 26. How do we control alert fatigue?
Suggested answer:
- SLA monitoring now classifies check severity (critical/high/medium), suppresses duplicate consecutive failures, escalates persistent incidents at configurable intervals, and sends recovery notifications when checks return to PASS.

## E. Presentation Strategy Tips

1. Open with problem and public value, not tools.
2. Show one end-to-end lineage example from source row to dashboard insight.
3. Explain one KPI and one forecast output in plain language.
4. Surface limitations proactively.
5. Close with operations confidence: tests, CI, orchestration, SLA monitoring.
