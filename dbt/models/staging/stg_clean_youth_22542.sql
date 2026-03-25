with base as (
    select *
    from {{ ref('stg_youth_22542') }}
),
metrics as (
    select
        line_number,
        source_file,
        snapshot_date_raw,
        snapshot_date,
        snapshot_year,
        region_code_clean,
        {{ canonical_region_name('region_name_clean') }} as region_name_canonical,
        region_level,
        'youth_welfare' as sector,
        {{ period_type_from_date('snapshot_date') }} as period_type,
        snapshot_year as period_start_year,
        snapshot_year as period_end_year,
        'facilities_total' as category_code,
        'youth_facilities_total' as category_name,
        {{ to_int_standardized('facilities_total') }} as capacity_value,
        case when {{ normalize_missing_marker('cast(facilities_total as varchar)') }} is null then true else false end as is_missing,
        'permanent' as capacity_class
    from base

    union all

    select
        line_number,
        source_file,
        snapshot_date_raw,
        snapshot_date,
        snapshot_year,
        region_code_clean,
        {{ canonical_region_name('region_name_clean') }} as region_name_canonical,
        region_level,
        'youth_welfare' as sector,
        {{ period_type_from_date('snapshot_date') }} as period_type,
        snapshot_year as period_start_year,
        snapshot_year as period_end_year,
        'places_hilfen' as category_code,
        'youth_places_hilfen' as category_name,
        {{ to_int_standardized('places_hilfen') }} as capacity_value,
        case when {{ normalize_missing_marker('cast(places_hilfen as varchar)') }} is null then true else false end as is_missing,
        'permanent' as capacity_class
    from base

    union all

    select
        line_number,
        source_file,
        snapshot_date_raw,
        snapshot_date,
        snapshot_year,
        region_code_clean,
        {{ canonical_region_name('region_name_clean') }} as region_name_canonical,
        region_level,
        'youth_welfare' as sector,
        {{ period_type_from_date('snapshot_date') }} as period_type,
        snapshot_year as period_start_year,
        snapshot_year as period_end_year,
        'staff_total' as category_code,
        'youth_staff_total' as category_name,
        {{ to_int_standardized('staff_total') }} as capacity_value,
        case when {{ normalize_missing_marker('cast(staff_total as varchar)') }} is null then true else false end as is_missing,
        'permanent' as capacity_class
    from base
)
select
    *,
    region_code_clean || '|' || cast(snapshot_year as varchar) || '|' || category_code as normalized_key
from metrics
