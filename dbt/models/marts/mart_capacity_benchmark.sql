with base as (
    select *
    from {{ ref('int_regional_sector_metrics') }}
),
benchmarked as (
    select
        region_code,
        region_name,
        year,
        sector_id,
        case
            when sector_id = 'childcare' then coalesce(capacity_value, 0) / nullif(coalesce(demand_value, 0), 0)
            when sector_id = 'youth' then coalesce(coverage_ratio, 0) / 20.0
            when sector_id = 'hospital' then coalesce(capacity_value, 0) / 10000.0
            else null
        end as benchmark_ratio
    from base
)
select
    region_code,
    region_name,
    year,
    avg(benchmark_ratio) as capacity_benchmark_ratio,
    count(*) as contributing_sector_count
from benchmarked
where benchmark_ratio is not null
group by 1, 2, 3
