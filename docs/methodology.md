# Methodology

## KPI Framework

### Childcare Capacity KPIs
- Facility count: number of childcare facilities by region and year
- Approved places: total approved childcare places by region and year
- Places per facility: approved places divided by facility count
- Growth rate: year-over-year change in approved places
- Coverage index: normalized childcare availability versus benchmark

### Youth Welfare KPIs
- Youth service places: total youth welfare places by region and year
- Places per region: normalized service capacity at regional level
- Regional coverage ratio: regional capacity relative to benchmark
- Trend slope: direction and magnitude of capacity change over time

### Hospital Infrastructure KPIs
- Hospital bed count: total beds by region, year, and specialty
- Beds per hospital: average bed capacity per hospital (where hospital count exists)
- Specialty concentration: concentration metric of specialty beds in a region
- Bed growth rate: year-over-year change in bed capacity
- Specialty resilience score: robustness of specialty coverage across regions

### Cross-Sector KPIs
- Service Maturity Index: composite indicator across childcare, youth welfare, and hospital capacity
- Underserved Region Score: weighted multi-domain deficit score
- Coverage Gap Index: benchmark minus observed provision
- Infrastructure Resilience Score: combined stability and growth score
- Forecasted Pressure Index: predicted near-term under-provision risk

### Data Quality KPIs
- Completeness rate
- Null rate
- Standardization success rate
- Freshness compliance
- SLA breach count

## Technical Principles
1. Raw data stays raw: source files are stored unchanged in `data/raw/`.
2. All cleaning is reproducible: no manual spreadsheet edits or opaque one-off fixes.
3. All business rules are documented: normalization and scoring logic lives in versioned docs and code.
4. All transformations are version-controlled: SQL and Python pipelines are tracked in Git.
5. Dashboards must trace back to model outputs: every chart must map to defined marts/KPIs.

## Business Rule Baseline
- Missing values: standardized sentinel handling with explicit null policy by metric type.
- Abbreviations: normalized through controlled mapping tables in `data/reference/`.
- Numeric parsing: locale-safe conversion for decimal and thousand separators.
- Region standardization: canonical region keys and labels across all source domains.
- Service maturity computation: weighted, documented composite of standardized capacity indicators.
- Underserved identification: threshold and ranking approach based on normalized deficits.
- Predictive thresholds: transparent cutoffs for warning and risk bands.

## Layered Data Model
- Raw layer: immutable ingestion artifacts.
- Staging layer: standardized headers, encoding, values, and labels.
- Intermediate layer: reusable aggregates and normalized analytical structures.
- Mart layer: decision-ready outputs (`mart_service_maturity`, `mart_underserved_regions`, `mart_capacity_trends`, `mart_predictive_risk`, `mart_data_quality`).
- Dimensions: `dim_region`, `dim_time`, `dim_sector`, `dim_specialty`.
- Facts: `fact_childcare_capacity`, `fact_youth_service_capacity`, `fact_hospital_beds`, `fact_cross_sector_resilience`.

## Predictive Approach
- Methods: trend extrapolation, moving averages, linear regression, and composite risk scoring.
- Priorities: interpretability, low operational complexity, policy relevance.
- Outputs: forecasted capacity, uncertainty indicator, regional risk ranking, warning thresholds.
