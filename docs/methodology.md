# Methodology

## Objective and Methodological Position

The methodology is designed for public-sector decision support where interpretability, reproducibility, and governance are prioritized over model complexity.

The project follows a layered analytics engineering approach:

1. preserve raw source integrity
2. normalize and standardize reproducibly
3. construct conformed analytical entities (dimensions/facts/marts)
4. publish policy-oriented KPIs and forecasting outputs
5. enforce quality through tests, CI, and SLA monitoring

## Data Model

### Layered Model

1. Raw layer (`raw.*` in DuckDB)
- immutable ingestion of source rows and lines

2. Staging layer (`analytics_staging.*`)
- schema harmonization, type coercion, value cleaning
- sector-specific cleaned long-format outputs (`stg_clean_*`)

3. Intermediate layer (`analytics_intermediate.*`)
- regional/year aggregations by sector
- cross-sector aligned metric table
- year-over-year trend features

4. Dimensions (`analytics_dimensions.*`)
- `dim_region`
- `dim_time`
- `dim_sector`

5. Facts (`analytics_facts.*`)
- `fct_regional_sector_capacity`

6. Marts (`analytics_marts.*`)
- resilience, underserved, coverage gap, growth/concentration, benchmark, quality, and KPI summaries

7. Predictions (`analytics_predictions.*`)
- capacity growth forecast outputs, evaluation summary, and model coefficients/weights

### Grain and Join Strategy

Primary analytical grain is `region_code x sector_id x year` for cross-sector comparability. Dimension joins use canonical region codes and normalized sector keys.

## Normalization Rules

Normalization is centralized in dbt macros and documented governance rules.

### Key Rule Categories

1. Missing values
- known sentinels (such as `-`, `k. A.`, `n/a`) are normalized to `NULL`

2. Numeric parsing
- locale-safe conversion for comma decimals
- support for million notation and range midpoint treatment where appropriate

3. Region canonicalization
- preserve leading zeros in region codes
- canonical name mapping and region-level classification
- umlaut-preserving canonical policy

4. Temporal normalization
- normalized snapshot year fields and period descriptors

5. Category standardization
- controlled category codes and sector labels to guarantee metric compatibility

## KPI Framework

### Domain KPIs

Childcare:
- facility count
- approved places
- places per facility
- growth rate

Youth welfare:
- places total
- facilities total
- places per facility
- trend metrics

Hospital capacity:
- beds total
- hospitals total
- beds per hospital
- specialty concentration proxy

### Cross-Sector KPIs

- Service Maturity Index
- Underserved Region Score
- Coverage Gap Index
- Growth and Concentration Trend
- Capacity Benchmark Ratio
- Composite Resilience Score

### Data Quality KPIs

- completeness rate
- data quality status class
- freshness and SLA compliance indicators

## Predictive Logic

### Prediction Target

Selected target: capacity growth forecast.

Formally:

`target_growth_next_year = (capacity_{t+1} - capacity_t) / capacity_t`

### Feature Engineering

1. prior-year growth
2. moving average (3-year) capacity
3. service concentration
4. regional deficit trend

### Model Choice and Fallback

Primary mode:
- interpretable linear regression when supervised next-year labels are available

Fallback mode:
- score-based extrapolation with explicit weights when historical labels are insufficient

### Evaluation

When supervised holdout is possible:
- trend fit (`R^2`, MAE)
- directional accuracy

When fallback mode is used:
- transparent coefficients/weights and rule-based risk bands are still produced

### Risk Banding

- high risk: predicted growth < -5%
- watch: -5% to < 2%
- stable or growth: >= 2%

## Quality and Reproducibility Controls

1. dbt tests for uniqueness, not-null, accepted values, and relationships
2. GitHub Actions for lint, compile, and test checks
3. Airflow DAG orchestration for repeatable scheduled runs
4. SLA monitoring for freshness, completeness, refresh integrity, and row-count anomaly detection

## Limitations

1. Source granularity and historical depth can limit supervised predictive performance.
2. Cross-domain comparability is partly constrained by heterogeneous source definitions.
3. Fallback score-based forecasting is intentionally conservative and should be interpreted as early warning, not causal inference.
4. Regional rankings can be sensitive to changes in source publication practices.
5. Current monitoring is threshold-based; advanced anomaly detection is a future enhancement.

## Methodological Rationale

This methodology intentionally balances technical rigor with interpretability for policy workflows:

- reproducible pipelines over opaque manual handling
- explainable indicators over black-box optimization
- governance-first documentation for audit, defense, and handoff
