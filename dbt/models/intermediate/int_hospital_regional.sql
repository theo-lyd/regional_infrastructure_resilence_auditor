with src as (
    select *
    from {{ ref('stg_clean_hospital_23111') }}
    where region_level = 'kreis'
),
agg as (
    select
        region_code_clean as region_code,
        max(region_name_canonical) as region_name,
        snapshot_year as year,
        sum(case when category_code = 'beds_total_jd' then capacity_value else 0 end) as beds_total,
        sum(case when category_code = 'hospitals_total' then capacity_value else 0 end) as hospitals_total,
        max(case when category_code like 'beds_%' then specialty_concentration_ratio else null end) as max_specialty_concentration
    from src
    group by 1, 3
)
select
    *,
    case when hospitals_total > 0 then beds_total::double / hospitals_total else null end as beds_per_hospital
from agg
