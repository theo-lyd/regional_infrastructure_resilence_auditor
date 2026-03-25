with base as (
    select *
    from {{ ref('int_regional_sector_metrics') }}
)
select
    region_code || '|' || sector_id || '|' || cast(year as varchar) as fact_row_id,
    region_code,
    sector_id,
    year,
    capacity_value,
    demand_value,
    coverage_ratio,
    utilization_ratio,
    concentration_ratio
from base
