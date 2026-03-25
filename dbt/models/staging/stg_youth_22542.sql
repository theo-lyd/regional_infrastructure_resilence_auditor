with src as (
    select *
    from {{ source('raw', 'raw_22542_01_02_4') }}
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
    {{ to_int_or_null('col_4') }} as facilities_total,
    {{ to_int_or_null('col_5') }} as facilities_hilfen,
    {{ to_int_or_null('col_6') }} as facilities_jugendarbeit,
    {{ to_int_or_null('col_7') }} as places_hilfen,
    {{ to_int_or_null('col_8') }} as staff_total,
    {{ to_int_or_null('col_9') }} as staff_hilfen,
    {{ to_int_or_null('col_10') }} as staff_jugendarbeit
from filtered
