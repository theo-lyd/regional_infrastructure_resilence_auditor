# Standardization and Business Rules

## Purpose

Define consistent transformation rules so KPI outputs are defensible and reproducible.

## Standardization Rules

1. Column names:
- normalize to snake_case
- remove special characters and repeated spaces

2. Region names:
- trim whitespace
- standardize known abbreviations using mapping tables in `data/reference/`
- assign canonical region key for joins

3. Time fields:
- parse year as integer
- reject non-parseable year values with logged exceptions

4. Numeric parsing:
- convert locale-formatted numeric strings safely
- strip unit labels before cast where needed
- preserve nulls for non-parseable values and log count

5. Missing values:
- never impute by default in foundational fact tables
- document any imputation in dedicated model logic and methodology notes

## Business Rules

1. Coverage index:
- normalized metric comparing regional provision to benchmark distribution

2. Underserved region score:
- weighted deficit across childcare, youth welfare, and hospital domains
- weights are explicit and version-controlled

3. Service maturity index:
- composite score combining standardized domain capacity indicators
- avoid hidden weighting or undocumented post-processing

4. Forecast risk bands:
- use transparent thresholds (low, medium, high)
- thresholds must be documented in methodology and dashboards

## Validation Rules

- uniqueness tests on dimension keys
- not-null tests on required surrogate/business keys
- accepted values tests for sectors/specialties
- row count and freshness checks as SLA indicators
