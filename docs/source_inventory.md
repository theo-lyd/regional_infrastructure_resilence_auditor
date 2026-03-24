# Source Inventory

## Purpose

Track all source inputs, ownership assumptions, ingestion notes, and known limitations.

## Source Table

| Source File | Domain | Expected Grain | Key Fields (Expected) | Notes |
| --- | --- | --- | --- | --- |
| `22541-01-01-4.csv` | Childcare | region-year (plus category if present) | region, year, facility_count, approved_places | Validate locale numeric formatting |
| `22542-01-02-4.csv` | Youth welfare | region-year (plus service type if present) | region, year, youth_places | Confirm label harmonization across years |
| `23111-01-04-4.csv` | Hospital | region-year-specialty (if present) | region, year, specialty, bed_count | Specialty labels may require standardization mapping |

## Ingestion Controls

- preserve originals in `data/raw/` unchanged
- store ingestion logs and parse diagnostics
- capture row counts and schema fingerprint per file version

## Quality Risks to Watch

- mixed encoding and delimiter variants
- inconsistent region labels or abbreviations
- year field as text with trailing characters
- numeric fields with locale separators
