with base as (
    select *
    from {{ ref('int_regional_sector_metrics') }}
),
sector_scores as (
    select
        region_code,
        region_name,
        year,
        sector_id,
        case
            when sector_id = 'childcare' then coalesce(coverage_ratio, 0)
            when sector_id = 'youth' then least(coalesce(coverage_ratio, 0) / 25.0, 2.0)
            when sector_id = 'hospital' then least(coalesce(capacity_value, 0) / 10000.0, 2.0)
            else null
        end as sector_maturity_component
    from base
)
select
    region_code,
    region_name,
    year,
    avg(sector_maturity_component) as service_maturity_index,
    count(*) as contributing_sector_count
from sector_scores
where sector_maturity_component is not null
group by 1, 2, 3
