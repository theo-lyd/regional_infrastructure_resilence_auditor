with src as (
    select *
    from {{ ref('stg_clean_childcare_22541') }}
    where region_level = 'kreis'
),
agg as (
    select
        region_code_clean as region_code,
        max(region_name_canonical) as region_name,
        snapshot_year as year,
        sum(case when category_code = 'places_total' then capacity_value else 0 end) as approved_places_total,
        sum(case when category_code = 'facility_count_total' then capacity_value else 0 end) as facility_count_total,
        sum(case when category_code = 'staff_total' then capacity_value else 0 end) as staff_total
    from src
    group by 1, 3
)
select
    *,
    case when facility_count_total > 0 then approved_places_total::double / facility_count_total else null end as places_per_facility
from agg
