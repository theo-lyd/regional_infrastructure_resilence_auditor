with base as (
    select *
    from {{ ref('int_regional_sector_metrics') }}
),
lagged as (
    select
        region_code,
        region_name,
        sector_id,
        year,
        capacity_value,
        coverage_ratio,
        concentration_ratio,
        lag(capacity_value) over (partition by region_code, sector_id order by year) as prev_capacity,
        lag(coverage_ratio) over (partition by region_code, sector_id order by year) as prev_coverage,
        lag(concentration_ratio) over (partition by region_code, sector_id order by year) as prev_concentration
    from base
)
select
    region_code,
    region_name,
    sector_id,
    year,
    capacity_value,
    prev_capacity,
    case
        when prev_capacity is null or prev_capacity = 0 then null
        else (capacity_value - prev_capacity) / prev_capacity
    end as capacity_yoy_growth,
    coverage_ratio,
    prev_coverage,
    case when prev_coverage is null then null else coverage_ratio - prev_coverage end as coverage_yoy_delta,
    concentration_ratio,
    prev_concentration,
    case when prev_concentration is null then null else concentration_ratio - prev_concentration end as concentration_yoy_delta
from lagged
