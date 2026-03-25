# Business Rules

## Purpose

Define standardization and interpretation rules used to convert raw statistics into reliable analytical fields.

## 1. Missing Value Policy

Values treated as missing:
1. `-`
2. `k. A.` / `k.a.` / `ka`
3. `n/a` / `na`
4. `null`
5. empty string

Rule:
- Missing markers are normalized to `NULL` before numeric conversion.

## 2. Numeric Normalization Policy

Supported input patterns:
1. comma decimals (example: `12,5`)
2. million notation (example: `48 Mio.`)
3. text ranges (example: `10-20`)

Rules:
1. Comma decimals are converted to dot decimal before cast.
2. `Mio.` values are converted to absolute numbers (`48 Mio.` -> `48000000`).
3. Range values are converted to midpoint for standardized numeric use (`10-20` -> `15`).
4. Unparseable values after normalization become `NULL`.

## 3. Region Normalization Policy

Canonical region vocabulary:
1. preserve official region code with leading zeros
2. trim whitespace around codes and names
3. collapse repeated internal whitespace in names
4. keep umlauts and German characters

Region level mapping:
1. `DG` -> `national`
2. 2-digit code -> `state`
3. 3-digit code -> `regierungsbezirk`
4. 5-digit code -> `kreis`
5. 8-digit code -> `special`
6. otherwise -> `unknown`

## 4. Sector and Category Normalization Policy

Sectors:
1. `childcare`
2. `youth_welfare`
3. `hospital`

Category normalization:
1. Childcare metrics are standardized into canonical category codes (for example `facility_count_total`, `approved_places_total`).
2. Youth metrics are standardized into canonical category codes (for example `youth_places_hilfen`, `youth_staff_total`).
3. Hospital metrics are standardized into canonical category codes with English-friendly aliases for reporting fields.

Regional grouping:
- Cross-sector comparisons should default to `kreis` level unless explicitly documented otherwise.

## 5. Time Normalization Policy

Rules:
1. `snapshot_date_raw` must parse with `%d.%m.%Y`.
2. `snapshot_year` is derived from parsed date.
3. `period_type` is standardized as `snapshot` for current source extracts.
4. `period_start_year` and `period_end_year` both equal `snapshot_year` for snapshot data.
5. Date-like footer/metadata rows are excluded before analytical modeling.

## 6. Capacity Definition Policy

`capacity_value` is the normalized numeric value representing the primary measure of service provision for a row's sector/category.

Examples:
1. childcare: approved places / facility count / staff count
2. youth welfare: places and staff categories
3. hospital: bed and hospital counts

`capacity_class` rule:
- default classification is `permanent` for current source fields.
- temporary capacity can only be assigned when explicit temporary indicators exist in source data.

## 7. Unknown and Unparseable Handling

Rules:
1. Unknown textual values are converted to `NULL` and flagged as missing.
2. Records remain in cleaned staging if keys and date are valid; measure-level nulls are preserved.
3. Downstream KPIs must decide whether to exclude or impute null measures; no implicit imputation in staging.

## 8. Specialty Concentration Rule (Hospital)

Definition:
- `specialty_concentration_ratio = specialty_beds / total_beds_for_concentration`

Rules:
1. Computed only for hospital categories beginning with `beds_`.
2. Returns `NULL` when denominator is zero or missing.
3. Used as an input for later concentration and resilience analyses.
