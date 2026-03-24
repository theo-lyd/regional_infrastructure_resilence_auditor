# Join Strategy

## Purpose

Define safe and explainable joins across domains to avoid silent duplication or row loss.

## Primary Join Keys

- `region_key`: canonical regional identifier
- `year`: normalized integer year
- `specialty_key`: hospital specialty key where applicable

## Join Rules

1. Cross-sector joins:
- use `region_key + year` only after each source is aggregated to region-year

2. Hospital specialty joins:
- keep specialty-level joins separate until specialty analysis is complete
- aggregate to region-year before merging into cross-sector marts

3. Dimension joins:
- use left join from facts to dimensions for descriptive enrichment
- enforce referential tests where practical

## Cardinality Expectations

- `fact_*` to `dim_region`: many-to-one
- `fact_*` to `dim_time`: many-to-one
- hospital specialty fact to specialty dimension: many-to-one

## Safeguards

- uniqueness tests on dimension keys
- duplicate-key checks before joins in intermediate models
- row-count comparisons pre/post join
- null-key monitoring for unmatched records

## Common Failure Modes

- region name mismatch due to unstandardized labels
- year type mismatch (string versus integer)
- specialty labels not normalized before join
