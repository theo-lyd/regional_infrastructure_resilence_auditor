# Grain Definition

## Purpose

Prevent metric distortion by making table grain explicit before joins and aggregations.

## Source Grains (Observed)

### `22541-01-01-4.csv` (Childcare)

- raw data grain: one row per `snapshot_date + region_code`
- measure grain: region-level totals (not facility-level records)
- effective period: snapshot year 2002 (plus one footer note row to exclude)

### `22542-01-02-4.csv` (Youth Welfare)

- raw data grain: one row per `snapshot_date + region_code`
- measure grain: region-level totals by youth-service categories embedded as columns
- effective period: snapshot year 2020 (plus footer note rows with date-like values)

### `23111-01-04-4.csv` (Hospital)

- raw data grain: one row per `snapshot_date + region_code`
- measure grain: region-level totals with specialty bed counts as separate columns
- effective period: snapshot year 2017 (plus one mixed note row to exclude)

## Canonical Modeling Grain Decisions

1. `stg_*` models:
- grain: one row per valid data row (`region_code + year`)

2. `fact_childcare_capacity`:
- grain: one row per `region_code + year` (childcare measures as columns)

3. `fact_youth_service_capacity`:
- grain: one row per `region_code + year` (youth measures as columns)

4. `fact_hospital_beds`:
- grain: one row per `region_code + year` (specialty beds remain wide initially)

5. optional long-format specialty model (recommended):
- grain: one row per `region_code + year + specialty`
- built via unpivot from hospital wide columns

6. `fact_cross_sector_resilience`:
- grain target: one row per `region_code + comparable_year`
- current limitation: no same-year overlap across all three sources, so this fact needs explicit temporal alignment policy

## Temporal Reality Check

- childcare source snapshot: 2002
- youth welfare source snapshot: 2020
- hospital source snapshot: 2017

This means direct same-year cross-sector joins are not currently possible without additional historical extracts or a documented alignment strategy.

## Anti-Patterns to Avoid

- joining footer-note rows as if they were valid data rows
- assuming each source is full time series (these extracts are effectively snapshot files)
- joining region-year tables across sectors without checking year overlap
- mixing raw and standardized region codes (whitespace, code-length differences)

## Quality Check

Before each mart build, verify:
- source grain
- target grain
- aggregation path
- no duplicate keys at target grain
- no metadata/footer rows leak into fact models
