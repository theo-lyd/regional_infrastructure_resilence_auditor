# Thesis Methodology Chapter

## 1. Methodological Aim

This chapter documents how the Regional Infrastructure Resilience Auditor transforms heterogeneous public-sector infrastructure data into a reproducible decision-support product.

The methodological priority is policy interpretability under engineering reproducibility constraints.

## 2. Data and Scope

The analysis uses three administrative source domains:

1. childcare infrastructure
2. youth welfare capacity
3. hospital capacity

Scope focuses on regional-year comparability and operationally actionable KPI outputs rather than causal attribution.

## 3. Pipeline Design

### 3.1 Raw Integrity

Raw files are ingested line-preserving into DuckDB raw schema tables. This preserves auditability and allows exact trace-back from derived metric to source line context.

### 3.2 Standardization and Cleaning

dbt staging models standardize schema and value formats across domains. Cleaning macros implement explicit missing-value handling, numeric normalization, and canonical region mapping.

### 3.3 Analytical Harmonization

Intermediate models aggregate each domain to common regional-year grain, enabling cross-sector comparisons without ad-hoc manual alignment.

### 3.4 Dimensional and Mart Modeling

Conformed dimensions and facts provide stable analytical keys. Marts publish decision-ready KPI views used by dashboards, storytelling, and policy briefings.

## 4. KPI Method

Domain and cross-sector KPIs are computed from governed mart models:

1. service maturity
2. underserved scoring
3. coverage gap
4. growth and concentration
5. resilience composite
6. data quality status

Each KPI has documented logic and testable model lineage.

## 5. Predictive Method

### 5.1 Target

Capacity growth forecast is defined as next-year proportional change in capacity.

### 5.2 Features

Feature engineering includes:

1. prior-year growth
2. moving average trend
3. service concentration
4. regional deficit trend

### 5.3 Model Strategy

Primary mode uses interpretable linear regression when supervised labels are available. Fallback mode uses explicit score-based extrapolation when supervised training is not reliable.

### 5.4 Evaluation

Evaluation emphasizes trend fit, directional accuracy, interpretability, and policy usefulness, with clear communication when fallback mode is active.

## 6. Reliability, CI/CD, and Monitoring

Reliability controls include:

1. dbt tests for schema and metric contracts
2. GitHub Actions CI for linting and compile/test validation
3. Airflow DAG for scheduled ingestion-transform-forecast-monitor flow
4. SLA checks for freshness, completeness, failed refresh, and row-count anomaly

## 7. Dashboard and Decision Translation

Dashboard views are organized around stakeholder decision questions:

1. executive overview
2. domain deep-dives
3. cross-sector comparison
4. predictive risk ranking
5. policy narrative annotations

This structure ensures analytical outputs are interpretable by both technical and non-technical audiences.

## 8. Limitations

1. Limited historical depth constrains supervised forecasting.
2. Cross-domain comparability depends on source quality and publication practices.
3. Composite indices simplify reality and should not replace domain expertise.
4. Forecast outputs support prioritization, not deterministic planning.

## 9. Methodological Contribution

The project demonstrates a practical blueprint for public-sector analytics products that are:

1. reproducible end-to-end
2. testable and monitorable
3. governance-documented
4. defense-ready for stakeholder and interview contexts
