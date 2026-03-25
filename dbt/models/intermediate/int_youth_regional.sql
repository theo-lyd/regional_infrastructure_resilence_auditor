with src as (
    select *
    from {{ ref('stg_clean_youth_22542') }}
    where region_level = 'kreis'
),
agg as (
    select
        region_code_clean as region_code,
        max(region_name_canonical) as region_name,
        snapshot_year as year,
        sum(case when category_code = 'places_hilfen' then capacity_value else 0 end) as youth_places_total,
        sum(case when category_code = 'facilities_total' then capacity_value else 0 end) as youth_facilities_total,
        sum(case when category_code = 'staff_total' then capacity_value else 0 end) as youth_staff_total
    from src
    group by 1, 3
)
select
    *,
    case when youth_facilities_total > 0 then youth_places_total::double / youth_facilities_total else null end as places_per_facility
from agg
