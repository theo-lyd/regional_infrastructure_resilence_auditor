with yoy as (
    select *
    from {{ ref('int_regional_sector_yoy') }}
)
select
    region_code,
    region_name,
    year,
    avg(capacity_yoy_growth) as avg_capacity_yoy_growth,
    avg(coverage_yoy_delta) as avg_coverage_yoy_delta,
    avg(concentration_yoy_delta) as avg_concentration_yoy_delta,
    count(*) as contributing_sector_count
from yoy
group by 1, 2, 3
