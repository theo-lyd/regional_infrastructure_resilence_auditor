# Source Inventory

## Purpose

Document what each raw CSV actually contains before transformation logic begins.

## Inspection Summary (Phase 3 Batch 3.1)

- file format: semicolon-delimited CSV-like extracts
- encoding for all three files: `iso-8859-1`
- umlaut risk: if opened as UTF-8 without conversion, characters appear as `�` (for example `Krankenh�user`, `Pl�tze`)
- all files contain multi-row metadata/header blocks before data rows
- all files contain footer notes and licensing text after data rows
- missing marker in numeric columns: primarily `-`

## Source Table (Observed)

| Source File | Domain | Data Rows (Observed) | Field Count (Data Rows) | Effective Reporting Year(s) | Notes |
| --- | --- | ---: | ---: | --- | --- |
| `22541-01-01-4.csv` | Childcare facilities, places, staff | 538 | 14 | 2002 | Contains one footer line `01.01.2001;` that must be excluded |
| `22542-01-02-4.csv` | Youth welfare facilities/places/staff | 538 | 10 | 2020 | Footer contains standalone note lines `01.01.1979` and `01.01.2011` |
| `23111-01-04-4.csv` | Hospitals and beds by specialty | 538 | 20 | 2017 | Footer contains mixed note row starting `01.01.1979; (ab Berichtsjahr 2011)...` |

## Header and Metadata Structure

### `22541-01-01-4.csv`

- line 1: table id
- lines 2-7: descriptive metadata + hierarchical measure headers + unit row
- line 8 onward: data rows (starting with date pattern `dd.mm.yyyy`)
- trailing section: separator line `__________`, quoted methodological notes, license text, `Stand:` timestamp

### `22542-01-02-4.csv`

- line 1: table id
- lines 2-9: descriptive metadata + hierarchical measure headers + unit row
- line 10 onward: data rows
- trailing section: separator, multi-line quoted notes, license text, `Stand:` timestamp

### `23111-01-04-4.csv`

- line 1: table id
- lines 2-8: descriptive metadata + hierarchical measure headers + unit row
- line 9 onward: data rows
- trailing section: separator, long quoted notes, license text, `Stand:` timestamp

## Ingestion Controls (Mandatory)

1. Read files with explicit encoding `latin-1` / `iso-8859-1`.
2. Parse delimiter as `;`.
3. Keep only rows where first column matches `^\d{2}\.\d{2}\.\d{4}$` and region code is valid (`DG` or digits).
4. Drop footer note rows, separators, license lines, and `Stand:` lines.
5. Normalize `-` to null for numeric measure fields.

## Source Registry and Format Support

1. Source onboarding is now configuration-driven via `data/reference/ingestion_source_registry.json`.
2. Supported source formats in ingestion adapter:
- `csv`
- `xlsx`
3. Schema drift is checked against expected column-count ranges from the registry.
4. Contract failures can stop ingestion when `fail_on_schema_drift=true`.

## Key Risks Identified

1. Character corruption risk if encoding not forced.
2. False year extraction from footer notes (`01.01.1979`, `01.01.2011`, `01.01.2001`).
3. Misaligned schema if metadata rows are treated as data.
4. Cross-sector temporal mismatch: files represent different snapshot years.
