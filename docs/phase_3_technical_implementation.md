# Phase 3 Technical Implementation

## Scope of This Technical Record

This document captures the implementation details for Phase 3 (source audit and data understanding):
- what was implemented
- how it was implemented
- evidence collection commands and outputs used
- files updated

## What Was Implemented

1. Source-level inspection for each CSV:
- column structure and header depth
- encoding validation
- umlaut/character risk identification
- missing marker detection
- metadata/footer row detection

2. Source-grounded documentation updates:
- `docs/source_inventory.md`
- `docs/data_dictionary.md`
- `docs/grain_definition.md`
- `docs/join_strategy.md`

3. Explicit ingestion constraints added:
- `iso-8859-1` encoding requirement
- semicolon delimiter requirement
- row filtering rules for non-data footer/metadata lines
- null normalization (`-` -> null)

## How It Was Implemented

Implementation method:
1. Inspect raw files directly before any transformation code.
2. Validate row patterns using command-line profiling (`awk`, `sed`, `grep`, `file`).
3. Detect and isolate anomalies (date-like footer rows and mixed note lines).
4. Update all four deliverable docs with observed facts, not assumptions.

## Files Created/Updated in Phase 3

Updated deliverables:
1. `docs/source_inventory.md`
2. `docs/data_dictionary.md`
3. `docs/grain_definition.md`
4. `docs/join_strategy.md`

## Commands/Codes and Files Ran

Commands used in the source audit:

```bash
# encoding detection
file -bi data/raw/22541-01-01-4.csv data/raw/22542-01-02-4.csv data/raw/23111-01-04-4.csv

# inspect headers and sample data rows
sed -n '1,25p' data/raw/22541-01-01-4.csv
sed -n '1,25p' data/raw/22542-01-02-4.csv
sed -n '1,25p' data/raw/23111-01-04-4.csv

# profile field counts and schema consistency
awk -F';' 'NR<=20{print NR ":" NF " fields | " $0}' data/raw/22541-01-01-4.csv
awk -F';' 'NR<=20{print NR ":" NF " fields | " $0}' data/raw/22542-01-02-4.csv
awk -F';' 'NR<=20{print NR ":" NF " fields | " $0}' data/raw/23111-01-04-4.csv

# detect missing-value markers and anomalies
grep -nE ';(-|\.|NA|N/A|NULL|x|X|\*|\.{3})($|;)|^(-|\.|NA|N/A|NULL|x|X|\*|\.{3})(;|$)' data/raw/*.csv

# detect malformed data-like rows
awk -F';' 'NR>1 && $1 ~ /^[0-9]{2}\.[0-9]{2}\.[0-9]{4}$/ && NF!=14 {print NR":"NF":"$0}' data/raw/22541-01-01-4.csv
awk -F';' 'NR>1 && $1 ~ /^[0-9]{2}\.[0-9]{2}\.[0-9]{4}$/ && NF!=10 {print NR":"NF":"$0}' data/raw/22542-01-02-4.csv
awk -F';' 'NR>1 && $1 ~ /^[0-9]{2}\.[0-9]{2}\.[0-9]{4}$/ && NF!=20 {print NR":"NF":"$0}' data/raw/23111-01-04-4.csv

# inspect footer sections
sed -n '540,600p' data/raw/22541-01-01-4.csv
sed -n '540,600p' data/raw/22542-01-02-4.csv
sed -n '540,600p' data/raw/23111-01-04-4.csv
```

## Critical Findings Recorded

1. All files are `iso-8859-1` and require explicit decoding.
2. Each file includes multi-line metadata headers and footer notes.
3. Date-like footer note rows can be misclassified as data if filtering is naive.
4. Snapshot-year mismatch across sectors prevents direct same-year cross-sector joins with current extracts.

## Output State After Completion

- Phase 3 documentation now reflects observed source realities and enforceable ingestion logic.
- Next-phase transformation work can proceed with reduced schema and join-risk ambiguity.
