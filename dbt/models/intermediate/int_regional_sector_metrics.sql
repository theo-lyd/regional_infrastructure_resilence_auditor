with childcare as (
    select
        region_code,
        region_name,
        year,
        'childcare' as sector_id,
        approved_places_total as capacity_value,
        facility_count_total as demand_value,
        places_per_facility as coverage_ratio,
        case when approved_places_total > 0 then staff_total::double / approved_places_total else null end as utilization_ratio,
        null::double as concentration_ratio
    from {{ ref('int_childcare_regional') }}
),
youth as (
    select
        region_code,
        region_name,
        year,
        'youth' as sector_id,
        youth_places_total as capacity_value,
        youth_facilities_total as demand_value,
        places_per_facility as coverage_ratio,
        null::double as utilization_ratio,
        case when youth_places_total > 0 then youth_staff_total::double / youth_places_total else null end as concentration_ratio
    from {{ ref('int_youth_regional') }}
),
hospital as (
    select
        region_code,
        region_name,
        year,
        'hospital' as sector_id,
        beds_total as capacity_value,
        null::double as demand_value,
        null::double as coverage_ratio,
        null::double as utilization_ratio,
        max_specialty_concentration as concentration_ratio
    from {{ ref('int_hospital_regional') }}
)
select * from childcare
union all
select * from youth
union all
select * from hospital
