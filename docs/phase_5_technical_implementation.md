# Phase 5 Technical Implementation

## Scope of This Technical Record

This document captures implementation details for Phase 5 (dbt project initialization):
- what was implemented
- how it was implemented
- commands/scripts/files used
- execution and test outcomes

## What Was Implemented

1. dbt scaffold initialization:
- `dbt/dbt_project.yml`
- `dbt/profiles.yml`
- `dbt/macros/standardization.sql`
- existing folder structure leveraged: `models/`, `snapshots/`, `tests/`, `macros/`

2. Source definitions for raw DuckDB tables:
- `dbt/models/staging/_sources_raw.yml`
- sources mapped to schema `raw`:
  - `raw_22541_01_01_4`
  - `raw_22542_01_02_4`
  - `raw_23111_01_04_4`

3. Staging models (1:1 structured exposure with raw preservation):
- `dbt/models/staging/stg_childcare_22541.sql`
- `dbt/models/staging/stg_youth_22542.sql`
- `dbt/models/staging/stg_hospital_23111.sql`
- `dbt/models/staging/stg_region_codes.sql`

4. First dbt tests:
- YAML tests in `dbt/models/staging/stg_models.yml`
  - `not_null`
  - `unique`
  - `accepted_values`
  - `relationships`
- Singular validity tests:
  - `dbt/tests/test_snapshot_date_validity.sql`
  - `dbt/tests/test_snapshot_year_validity.sql`

## How It Was Implemented

### Project Configuration

1. Configure dbt project metadata and paths in `dbt_project.yml`.
2. Configure DuckDB profile in `profiles.yml` with local database path.
3. Set staging models to materialize as views in schema `analytics_staging`.

### Staging Modeling Strategy

1. Keep raw columns from raw tables (`select *`) to preserve traceability.
2. Add standardized structured fields:
- `snapshot_date_raw`, `snapshot_date`, `snapshot_year`
- `region_code_raw`, `region_name_raw`, `region_code_clean`, `region_name_clean`
- `region_level`, `region_year_key`
3. Expose typed metric columns using macro-based parsing:
- `to_int_or_null()` converts `-` to null and casts numerics safely.
4. Build cross-source region reference model (`stg_region_codes`) for relationship tests.

### Testing Strategy

1. Entity-level checks:
- non-null keys and dates
- uniqueness on `region_year_key`
2. Domain checks:
- accepted values for `region_level`
3. Relational checks:
- each staging model `region_code_clean` must exist in `stg_region_codes`
4. Temporal validity checks:
- valid `dd.mm.yyyy` parsing
- `snapshot_year` equals year extracted from `snapshot_date`

## Commands/Codes and Files Ran

Commands executed during this phase:

```bash
# verify dbt runtime
/workspaces/regional_infrastructure_resilence_auditor/.venv/bin/dbt --version

# validate project syntax
/workspaces/regional_infrastructure_resilence_auditor/.venv/bin/dbt parse --project-dir dbt --profiles-dir dbt

# build staging models and run tests
/workspaces/regional_infrastructure_resilence_auditor/.venv/bin/dbt build --project-dir dbt --profiles-dir dbt --select models/staging+
```

Key outputs from executed commands:
1. `dbt parse`: success, no warnings after syntax adjustments.
2. `dbt build --select models/staging+`: PASS=27, WARN=0, ERROR=0.

## Quality/Compatibility Adjustments Made

1. Updated generic test argument syntax to modern dbt format (`arguments:` block) to remove deprecation warnings.
2. Updated `stg_region_codes` aggregation to guarantee unique `region_code_clean` for relationship and uniqueness tests.
3. Added `.gitignore` rules for local dbt artifacts:
- `dbt/target/`
- `dbt/logs/`
- `dbt/.user.yml`

## Output State After Completion

- dbt project skeleton is operational.
- source definitions are connected to DuckDB raw tables.
- staging layer is materialized and tested.
- baseline data quality and validity checks are active.
