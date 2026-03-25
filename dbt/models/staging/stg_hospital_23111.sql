with src as (
    select *
    from {{ source('raw', 'raw_23111_01_04_4') }}
),
filtered as (
    select
        *,
        trim(col_1) as snapshot_date_raw,
        trim(col_2) as region_code_raw,
        trim(col_3) as region_name_raw
    from src
    where regexp_matches(trim(col_1), '^\d{2}\.\d{2}\.\d{4}$')
      and (trim(col_2) = 'DG' or regexp_matches(trim(col_2), '^[0-9]+$'))
)
select
    *,
    true as is_data_row,
    try_strptime(snapshot_date_raw, '%d.%m.%Y')::date as snapshot_date,
    try_cast(substr(snapshot_date_raw, 7, 4) as integer) as snapshot_year,
    regexp_replace(region_name_raw, '\\s+', ' ') as region_name_clean,
    region_code_raw as region_code_clean,
    {{ region_level_from_code('region_code_raw') }} as region_level,
    snapshot_date_raw || '|' || region_code_raw as region_year_key,
    {{ to_int_or_null('col_4') }} as hospitals_total,
    {{ to_int_or_null('col_5') }} as beds_total_jd,
    {{ to_int_or_null('col_6') }} as beds_augenheilkunde,
    {{ to_int_or_null('col_7') }} as beds_chirurgie,
    {{ to_int_or_null('col_8') }} as beds_frauenheilkunde_geburtshilfe,
    {{ to_int_or_null('col_9') }} as beds_hno,
    {{ to_int_or_null('col_10') }} as beds_haut_geschlechtskrankheiten,
    {{ to_int_or_null('col_11') }} as beds_innere_medizin,
    {{ to_int_or_null('col_12') }} as beds_geriatrie,
    {{ to_int_or_null('col_13') }} as beds_kinderheilkunde,
    {{ to_int_or_null('col_14') }} as beds_neurologie,
    {{ to_int_or_null('col_15') }} as beds_orthopaedie,
    {{ to_int_or_null('col_16') }} as beds_urologie,
    {{ to_int_or_null('col_17') }} as beds_uebrige_fachbereiche,
    {{ to_int_or_null('col_18') }} as beds_kjpp,
    {{ to_int_or_null('col_19') }} as beds_psychiatrie_psychotherapie,
    {{ to_int_or_null('col_20') }} as beds_psychotherapeutische_medizin
from filtered
