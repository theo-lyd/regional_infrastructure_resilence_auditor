# Join Strategy

## Purpose

Define safe and explainable joins across domains to avoid silent duplication or row loss.

## Primary Join Keys

- `region_key`: canonical regional identifier
- `year`: normalized integer year
- `specialty_key`: hospital specialty key where applicable

## Region Code Standardization Rules

Observed source code patterns include:
- `DG` (national aggregate)
- 2-digit codes (state-level)
- 3-digit codes (regional district groupings)
- 5-digit codes (kreis / kreisfreie Stadt)
- occasional 8-digit codes (special historical/administrative cases)

Standardization requirements:
1. trim whitespace around raw codes
2. preserve leading zeros
3. keep `DG` as dedicated national level
4. classify `region_level` by code pattern
5. choose one comparison level per analysis (recommended default: 5-digit kreis level)

## Join Rules

1. Intra-source joins:
- generally unnecessary at raw stage because each source is already one row per `region_code + year`

2. Cross-sector joins (current extracts):
- cannot rely on same-year joins because source years differ (2002 vs 2017 vs 2020)
- only join on `region_key + year` where overlap exists (currently limited)

3. Cross-sector comparison strategy (recommended for current data):
- normalize each source to sector-specific index by region
- compare relative ranking across sectors at common region level
- document that comparisons are cross-snapshot, not same-year causal comparisons

4. Hospital specialty handling:
- keep specialty metrics wide in base fact
- optionally unpivot to `region_key + year + specialty` for specialty analytics

5. Dimension joins:
- use left join from facts to dimensions for enrichment
- enforce referential tests on canonical region keys

## Cardinality Expectations

- `fact_*` to `dim_region`: many-to-one
- `fact_*` to `dim_time`: many-to-one
- hospital specialty fact to specialty dimension: many-to-one

## Safeguards

- uniqueness tests on dimension keys
- duplicate-key checks before joins in intermediate models
- row-count comparisons pre/post join
- null-key monitoring for unmatched records
- explicit filter to remove metadata/footer/date-like note rows before joins
- explicit exclusion or separate treatment of `DG` national aggregate rows

## Common Failure Modes

- region name mismatch due to unstandardized labels
- year type mismatch (string versus integer)
- specialty labels not normalized before join
- false joins driven by footer note rows containing date-like values
- mixing administrative levels (2-digit with 5-digit) in one comparison table
- treating cross-snapshot joins as time-consistent trends
