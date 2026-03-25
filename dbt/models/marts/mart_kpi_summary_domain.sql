with base as (
    select *
    from {{ ref('int_regional_sector_metrics') }}
)
select
    year,
    sector_id,
    count(distinct region_code) as covered_regions,
    avg(capacity_value) as avg_capacity_value,
    avg(coverage_ratio) as avg_coverage_ratio,
    avg(utilization_ratio) as avg_utilization_ratio,
    avg(concentration_ratio) as avg_concentration_ratio
from base
group by 1, 2
