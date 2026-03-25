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
