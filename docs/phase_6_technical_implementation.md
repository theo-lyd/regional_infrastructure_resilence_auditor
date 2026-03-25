# Phase 6 Technical Implementation

## Scope of This Technical Record

This document captures implementation details for Phase 6 (data standardization and business rules):
- what was implemented
- how it was implemented
- commands/scripts/files used
- validation outcomes

## What Was Implemented

1. Standardization macro expansion:
- `dbt/macros/standardization.sql`
- added robust helpers for missing values, numeric parsing, region canonicalization, and period typing

2. Cleaned staging models:
- `dbt/models/staging/stg_clean_childcare_22541.sql`
- `dbt/models/staging/stg_clean_youth_22542.sql`
- `dbt/models/staging/stg_clean_hospital_23111.sql`

3. Cleaned staging tests:
- `dbt/models/staging/stg_clean_models.yml`

4. Business rules documentation:
- `docs/business_rules.md`

## How It Was Implemented

### Numeric Normalization

Implemented macros to standardize:
1. missing markers (`-`, `k. A.`, `n/a`, etc.) -> `NULL`
2. comma decimals (`12,5`) -> `12.5`
3. million notation (`48 Mio.`) -> absolute values
4. text ranges (`10-20`) -> midpoint (`15`)

### Region Normalization

Implemented canonicalization rules:
1. trim and whitespace-collapse region names
2. preserve leading zeros in region codes
3. region-level classification from code format

### Sector and Category Normalization

Implemented long-format cleaned staging outputs:
1. one standardized `sector` value per model
2. canonical `category_code` and `category_name` values
3. normalized `capacity_value` for KPI-ready analytics

### Time Normalization

Added standardized time fields:
1. `period_type` = `snapshot`
2. `period_start_year` / `period_end_year`
3. normalized keying with year-level identifiers

### Business Rules

Documented in `docs/business_rules.md`:
1. missing value handling policy
2. unknown treatment policy
3. capacity definition
4. specialty concentration metric definition
5. temporary vs permanent capacity classification

## Commands/Codes and Files Ran

Commands executed in this phase:

```bash
# dbt syntax validation
/workspaces/regional_infrastructure_resilence_auditor/.venv/bin/dbt parse --project-dir dbt --profiles-dir dbt

# build cleaned staging models + tests
/workspaces/regional_infrastructure_resilence_auditor/.venv/bin/dbt build --project-dir dbt --profiles-dir dbt --select stg_clean_childcare_22541 stg_clean_youth_22542 stg_clean_hospital_23111

# inspect changed files
git status --short
```

## Validation Outcomes

Result from executed dbt build:
1. PASS=18
2. WARN=0
3. ERROR=0

This confirms cleaned staging models and normalization tests are operational.

## Output State After Completion

- Standardization logic is centralized in reusable dbt macros.
- Cleaned staging layer is available for downstream marts and KPI modeling.
- Business rules are explicitly documented for audit and stakeholder defense.
