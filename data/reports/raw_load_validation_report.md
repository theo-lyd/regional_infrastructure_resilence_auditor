# Raw Load Validation Report

Generated at (UTC): 2026-03-25T17:32:43.441252+00:00

## Overall Result

- Status: PASS

## File-Level Checks

| File | Format | Raw Table | Exists | Expected Rows | Loaded Rows | Row Count Match | Mojibake Rows (`�`) | Non-ASCII Source Rows | Non-ASCII Mismatches | Encoding Check |
| --- | --- | --- | --- | ---: | ---: | --- | ---: | ---: | ---: | --- |
| 22541-01-01-4.csv | csv | raw_22541_01_01_4 | True | 560 | 560 | True | 0 | 110 | 0 | True |
| 22542-01-02-4.csv | csv | raw_22542_01_02_4 | True | 580 | 580 | True | 0 | 121 | 0 | True |
| 23111-01-04-4.csv | csv | raw_23111_01_04_4 | True | 598 | 598 | True | 0 | 122 | 0 | True |

## Validation Logic

1. Raw table exists in schema `raw`.
2. Loaded row count equals source line count from CSV file.
3. Encoding corruption check: no replacement-char rows (`�`).
4. Non-ASCII integrity check: source non-ASCII lines match `raw_line` exactly by line number.
5. For XLSX sources, row-count and line-preservation checks are approximated via sheet row extraction.
