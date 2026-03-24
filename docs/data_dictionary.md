# Data Dictionary (Starter)

## Purpose

Provide shared vocabulary for technical and policy stakeholders.

## Core Fields

| Field | Type | Description | Business Meaning |
| --- | --- | --- | --- |
| `region_key` | string | canonical region identifier | stable key for cross-domain comparison |
| `region_name` | string | standardized region label | human-readable region reference |
| `year` | integer | reporting year | temporal comparison anchor |
| `sector` | string | domain label (`childcare`, `youth_welfare`, `hospital`) | distinguishes service domain |
| `facility_count` | numeric | childcare facility total | proxy for childcare infrastructure footprint |
| `approved_places` | numeric | childcare places approved | childcare capacity indicator |
| `youth_places` | numeric | youth service places | youth welfare capacity indicator |
| `bed_count` | numeric | hospital bed count | health infrastructure capacity indicator |
| `specialty` | string | hospital specialty category | supports specialty resilience analysis |
| `service_maturity_index` | numeric | composite score | overall regional infrastructure maturity |
| `underserved_region_score` | numeric | deficit score across domains | prioritization indicator for intervention |
| `forecasted_pressure_index` | numeric | projected near-term constraint risk | early warning for planning action |

## Data Dictionary Governance

- every new KPI field must include definition, type, and formula owner
- deprecations should be documented with replacement guidance
- dashboard labels must map to dictionary terms
