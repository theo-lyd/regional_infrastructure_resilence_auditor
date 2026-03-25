# Data Dictionary (Phase 3 Source-Level)

## Purpose

Define meaningful source columns with business meaning, data type, key role, and cleaning requirements.

## Common Key Columns (All Three Sources)

| Canonical Column | Meaning | Type | Key Status | Cleaning Requirement |
| --- | --- | --- | --- | --- |
| `snapshot_date_raw` | raw date string from col 1 (`dd.mm.yyyy`) | string | component of natural key | parse to date, derive `year` |
| `year` | reporting year from `snapshot_date_raw` | integer | component of natural key | `year = int(substr(snapshot_date_raw, 7, 4))` |
| `region_code_raw` | source territorial code (`DG`, 2-digit, 3-digit, 5-digit, sometimes 8-digit) | string | component of natural key | trim spaces, preserve leading zeros |
| `region_name_raw` | source regional label | string | descriptive | trim left padding, normalize whitespace, keep umlauts |

## `22541-01-01-4.csv` (Childcare)

Data schema after canonical keys (11 measures):

| Canonical Column | Meaning | Type | Key Status | Cleaning Requirement |
| --- | --- | --- | --- | --- |
| `facilities_total` | total childcare facilities | integer | metric | cast numeric, `-` -> null |
| `facilities_kindergarten` | kindergarten facilities | integer | metric | cast numeric, `-` -> null |
| `facilities_hort` | after-school facilities (Horte) | integer | metric | cast numeric, `-` -> null |
| `facilities_krippe` | nursery facilities (Kinderkrippen) | integer | metric | cast numeric, `-` -> null |
| `facilities_other` | other facility types | integer | metric | cast numeric, `-` -> null |
| `places_total` | total approved places | integer | metric | cast numeric, `-` -> null |
| `places_krippe` | places for nursery-age children | integer | metric | cast numeric, `-` -> null |
| `places_kindergarten` | places for kindergarten-age children | integer | metric | cast numeric, `-` -> null |
| `places_hort` | places for after-school care | integer | metric | cast numeric, `-` -> null |
| `staff_total` | total active personnel | integer | metric | cast numeric, `-` -> null |
| `staff_kindergarten` | active personnel in kindergartens | integer | metric | cast numeric, `-` -> null |

## `22542-01-02-4.csv` (Youth Welfare)

Data schema after canonical keys (7 measures):

| Canonical Column | Meaning | Type | Key Status | Cleaning Requirement |
| --- | --- | --- | --- | --- |
| `facilities_total` | total youth welfare facilities | integer | metric | cast numeric, `-` -> null |
| `facilities_hilfen` | facilities for Erziehung / junge Volljaehrige support | integer | metric | cast numeric, `-` -> null |
| `facilities_jugendarbeit` | facilities in youth work | integer | metric | cast numeric, `-` -> null |
| `places_hilfen` | available places for Erziehung / junge Volljaehrige support | integer | metric | cast numeric, `-` -> null |
| `staff_total` | total active personnel | integer | metric | cast numeric, `-` -> null |
| `staff_hilfen` | staff for Erziehung / junge Volljaehrige support | integer | metric | cast numeric, `-` -> null |
| `staff_jugendarbeit` | staff in youth work | integer | metric | cast numeric, `-` -> null |

## `23111-01-04-4.csv` (Hospital Infrastructure)

Data schema after canonical keys (17 measures):

| Canonical Column | Meaning | Type | Key Status | Cleaning Requirement |
| --- | --- | --- | --- | --- |
| `hospitals_total` | number of hospitals | integer | metric | cast numeric, `-` -> null |
| `beds_total_jd` | total beds (annual average) | integer | metric | cast numeric, `-` -> null |
| `beds_augenheilkunde` | beds in ophthalmology | integer | metric | cast numeric, `-` -> null |
| `beds_chirurgie` | beds in surgery (combined) | integer | metric | cast numeric, `-` -> null |
| `beds_frauenheilkunde_geburtshilfe` | beds in gynecology and obstetrics | integer | metric | cast numeric, `-` -> null |
| `beds_hno` | beds in ENT | integer | metric | cast numeric, `-` -> null |
| `beds_haut_geschlechtskrankheiten` | beds in dermatology/venereal disease | integer | metric | cast numeric, `-` -> null |
| `beds_innere_medizin` | beds in internal medicine | integer | metric | cast numeric, `-` -> null |
| `beds_geriatrie` | beds in geriatrics | integer | metric | cast numeric, `-` -> null |
| `beds_kinderheilkunde` | beds in pediatrics | integer | metric | cast numeric, `-` -> null |
| `beds_neurologie` | beds in neurology | integer | metric | cast numeric, `-` -> null |
| `beds_orthopaedie` | beds in orthopedics | integer | metric | cast numeric, `-` -> null |
| `beds_urologie` | beds in urology | integer | metric | cast numeric, `-` -> null |
| `beds_uebrige_fachbereiche` | beds in remaining specialties | integer | metric | cast numeric, `-` -> null |
| `beds_kjpp` | beds in child/adolescent psychiatry/psychotherapy | integer | metric | cast numeric, `-` -> null |
| `beds_psychiatrie_psychotherapie` | beds in psychiatry/psychotherapy | integer | metric | cast numeric, `-` -> null |
| `beds_psychotherapeutische_medizin` | beds in psychotherapeutic medicine | integer | metric | cast numeric, `-` -> null |

## Explicit Non-Data Rows to Exclude

- metadata header rows at top of each file
- separator row `__________`
- quoted notes and licensing paragraphs
- `Stand:` timestamp rows
- malformed date-like note rows (`01.01.2001;`, `01.01.1979`, `01.01.2011`, and mixed note variants)

## Data Dictionary Governance

1. Every new transformed field must reference one source column or documented derivation.
2. Any renamed field must keep a mapping table in transformation docs.
3. Dashboard labels must map 1:1 to canonical model fields.

## Dashboard KPI Dictionary (Phase 11 Completion)

The following entries provide one-line, reviewer-friendly KPI definitions used in dashboard views.

| KPI | Definition | Formula | Source Model | Interpretation |
| --- | --- | --- | --- | --- |
| service_maturity_index | Average sector maturity component by region-year. | `avg(sector_maturity_component)` | `analytics_marts.mart_service_maturity_index` | Higher values indicate relatively stronger multi-sector service maturity. |
| underserved_region_score | Average sector penalty for underservice by region-year. | `avg(underserved_penalty)` | `analytics_marts.mart_underserved_region_score` | Higher values indicate greater potential underservice risk. |
| coverage_gap_index | Average shortfall from benchmark coverage by region-year. | `avg(max(raw_gap, 0))` | `analytics_marts.mart_coverage_gap_index` | Higher values indicate larger benchmark gaps requiring attention. |
| resilience_score | Composite resilience metric combining maturity, underserved, gap, and growth signals. | `0.40*maturity + 0.20*(1-underserved) + 0.20*(1-min(gap,1)) + 0.20*bounded_growth` | `analytics_marts.mart_resilience_score` | Higher values indicate more resilient regional service conditions. |
| avg_capacity_yoy_growth | Mean year-over-year growth in capacity across sector rows by region-year. | `avg(capacity_yoy_growth)` | `analytics_marts.mart_growth_and_concentration` | Positive values indicate average capacity expansion; negative implies contraction. |
| avg_coverage_yoy_delta | Mean year-over-year change in coverage indicator by region-year. | `avg(coverage_yoy_delta)` | `analytics_marts.mart_growth_and_concentration` | Positive values indicate improving coverage trajectory. |
| avg_concentration_yoy_delta | Mean year-over-year change in concentration indicator by region-year. | `avg(concentration_yoy_delta)` | `analytics_marts.mart_growth_and_concentration` | Positive values suggest concentration is increasing and should be context-reviewed. |
| capacity_benchmark_ratio | Average benchmark-relative capacity ratio by region-year. | `avg(benchmark_ratio)` | `analytics_marts.mart_capacity_benchmark` | Values above 1 suggest benchmark-relative strength; below 1 suggest potential under-capacity. |
| capacity_completeness_rate | Share of fact rows with non-null capacity values per year. | `capacity_non_null_rows / total_rows` | `analytics_marts.mart_data_quality_status` | Higher values indicate stronger completeness and better decision confidence. |
| data_quality_status | Categorical quality status based on completeness thresholds. | `good if >=0.95; watch if >=0.85; critical otherwise; insufficient if no rows` | `analytics_marts.mart_data_quality_status` | Fast non-technical signal for whether outputs are policy-ready. |
| avg_service_maturity | Annual global average of service maturity across all regions. | `avg(service_maturity_index)` | `analytics_marts.mart_kpi_summary_executive` | Portfolio-level maturity trend indicator for executive reporting. |
| avg_resilience_score | Annual global average of resilience score across all regions. | `avg(resilience_score)` | `analytics_marts.mart_kpi_summary_executive` | Portfolio-level resilience trend indicator for strategic oversight. |
| avg_underserved_score | Annual global average underserved score across all regions. | `avg(underserved_region_score)` | `analytics_marts.mart_kpi_summary_executive` | Higher values indicate systemic underservice pressure. |
| avg_coverage_gap | Annual global average coverage gap across all regions. | `avg(coverage_gap_index)` | `analytics_marts.mart_kpi_summary_executive` | Higher values indicate systemic benchmark shortfall. |
| predicted_capacity_growth | Forecasted proportional growth of next-year capacity for region-sector. | `model_output_growth` | `analytics_predictions.pred_capacity_growth_forecast` | Lower values indicate potential near-term pressure. |
| predicted_capacity | Forecasted next-year capacity level for region-sector. | `source_capacity * (1 + predicted_capacity_growth)` | `analytics_predictions.pred_capacity_growth_forecast` | Used for scenario-oriented planning conversations, not deterministic targets. |
| risk_band | Categorical pressure class from predicted growth. | `high_risk:<-0.05; watch:-0.05 to <0.02; stable_or_growth:>=0.02` | `analytics_predictions.pred_capacity_growth_forecast` | Highlights where proactive policy review should start. |
