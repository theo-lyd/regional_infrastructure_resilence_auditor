# Grain Definition

## Purpose

Prevent metric distortion by making table grain explicit before joins and aggregations.

## Core Grain Definitions

1. `fact_childcare_capacity`
- grain: one row per region-year (and category if category-level source data exists)

2. `fact_youth_service_capacity`
- grain: one row per region-year (and service type if provided)

3. `fact_hospital_beds`
- grain: one row per region-year-specialty (if specialty is available)

4. `fact_cross_sector_resilience`
- grain: one row per region-year
- built after harmonizing sector-level facts to comparable granularity

5. `dim_region`
- grain: one row per canonical region

6. `dim_time`
- grain: one row per year

7. `dim_sector`
- grain: one row per sector (childcare, youth_welfare, hospital)

## Anti-Patterns to Avoid

- joining a region-year table directly to region-year-specialty table without aggregation
- computing cross-sector averages across inconsistent grains
- mixing raw and standardized region keys in joins

## Quality Check

Before each mart build, verify:
- source grain
- target grain
- aggregation path
- no duplicate keys at target grain
