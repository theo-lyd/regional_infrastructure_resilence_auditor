with base as (
    select *
    from {{ ref('stg_hospital_23111') }}
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
        'hospital' as sector,
        {{ period_type_from_date('snapshot_date') }} as period_type,
        snapshot_year as period_start_year,
        snapshot_year as period_end_year,
        'hospitals_total' as category_code,
        'hospitals_total' as category_name,
        {{ to_int_standardized('hospitals_total') }} as capacity_value,
        case when {{ normalize_missing_marker('cast(hospitals_total as varchar)') }} is null then true else false end as is_missing,
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
        'hospital' as sector,
        {{ period_type_from_date('snapshot_date') }} as period_type,
        snapshot_year as period_start_year,
        snapshot_year as period_end_year,
        'beds_total_jd' as category_code,
        'beds_total_jd' as category_name,
        {{ to_int_standardized('beds_total_jd') }} as capacity_value,
        case when {{ normalize_missing_marker('cast(beds_total_jd as varchar)') }} is null then true else false end as is_missing,
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
        'hospital' as sector,
        {{ period_type_from_date('snapshot_date') }} as period_type,
        snapshot_year as period_start_year,
        snapshot_year as period_end_year,
        'beds_psychiatrie_psychotherapie' as category_code,
        'beds_psychiatry_psychotherapy' as category_name,
        {{ to_int_standardized('beds_psychiatrie_psychotherapie') }} as capacity_value,
        case when {{ normalize_missing_marker('cast(beds_psychiatrie_psychotherapie as varchar)') }} is null then true else false end as is_missing,
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
        'hospital' as sector,
        {{ period_type_from_date('snapshot_date') }} as period_type,
        snapshot_year as period_start_year,
        snapshot_year as period_end_year,
        'beds_innere_medizin' as category_code,
        'beds_internal_medicine' as category_name,
        {{ to_int_standardized('beds_innere_medizin') }} as capacity_value,
        case when {{ normalize_missing_marker('cast(beds_innere_medizin as varchar)') }} is null then true else false end as is_missing,
        'permanent' as capacity_class
    from base
),
enriched as (
    select
        *,
        sum(case when category_code like 'beds_%' then coalesce(capacity_value, 0) else 0 end)
            over (partition by region_code_clean, snapshot_year) as total_beds_for_concentration
    from metrics
)
select
    *,
    case
        when category_code like 'beds_%' and total_beds_for_concentration > 0 then capacity_value::double / total_beds_for_concentration
        else null
    end as specialty_concentration_ratio,
    region_code_clean || '|' || cast(snapshot_year as varchar) || '|' || category_code as normalized_key
from enriched
