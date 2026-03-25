# Predictive Modeling Assumptions (Phase 8)

## Prediction Target

Selected target:
- capacity growth forecast

Definition:
- `target_growth_next_year = (capacity_{t+1} - capacity_t) / capacity_t`

## Feature Engineering Assumptions

1. Prior-year growth:
- sourced from `analytics_intermediate.int_regional_sector_yoy.capacity_yoy_growth`
- missing values are imputed as `0.0`

2. Moving averages:
- three-period moving average of `capacity_value`
- computed per `region_code` + `sector_id`

3. Service concentration:
- sourced from `analytics_intermediate.int_regional_sector_metrics.concentration_ratio`
- missing values are imputed as `0.0`

4. Regional deficit trend:
- derived from annual change in `analytics_marts.mart_coverage_gap_index.coverage_gap_index`
- joined at region-year level and applied to all sector rows in that region-year

## Model Choice Assumptions

Model type:
- linear regression (interpretable baseline)

Why this model:
- direct coefficient interpretation for each engineered feature
- low complexity and transparent behavior for policy communication
- stable baseline for future comparison with richer time-series methods

## Evaluation Assumptions

1. Trend fit:
- R-squared and MAE on latest-year holdout when enough history exists

2. Directional accuracy:
- share of records where sign(predicted growth) matches sign(actual growth)

3. Interpretability:
- feature coefficients persisted in `analytics_predictions.pred_capacity_growth_coefficients`

4. Business usefulness:
- risk bands based on predicted growth thresholds:
  - `high_risk`: < -5%
  - `watch`: -5% to < 2%
  - `stable_or_growth`: >= 2%

## Operational Assumptions

- Forecasting operates on annual snapshots.
- Predictions are generated per `region_code` + `sector_id`.
- Output tables are regenerated with `create or replace` semantics for reproducibility.
