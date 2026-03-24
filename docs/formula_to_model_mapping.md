# Formula to Model Mapping

## Purpose

Map each KPI formula to the model layer where it is computed for full traceability.

## Mapping Table

| KPI | Formula (Conceptual) | Computation Layer | Expected Model |
| --- | --- | --- | --- |
| Places per facility | approved_places / facility_count | intermediate | `int_childcare_metrics` |
| Childcare growth rate | (current - prior) / prior | mart | `mart_capacity_trends` |
| Regional coverage ratio | regional_capacity / benchmark_capacity | mart | `mart_service_maturity` |
| Bed growth rate | (beds_t - beds_t-1) / beds_t-1 | mart | `mart_capacity_trends` |
| Service maturity index | weighted normalized sector scores | mart | `mart_service_maturity` |
| Underserved region score | weighted deficit sum across sectors | mart | `mart_underserved_regions` |
| Forecasted pressure index | trend forecast + deficit weighting | mart/predictive output | `mart_predictive_risk` |
| Completeness rate | non_null_fields / required_fields | mart | `mart_data_quality` |

## Modeling Notes

- staging models should not contain business scoring formulas
- marts should reference intermediate models, not raw sources
- formula versions must be controlled in Git and explained in docs

## Review Checklist

- each dashboard metric maps to one documented formula
- each formula maps to one model output
- each model output has declared grain and owner
