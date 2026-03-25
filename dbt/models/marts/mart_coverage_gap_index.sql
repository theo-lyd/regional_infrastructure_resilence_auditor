with base as (
    select *
    from {{ ref('int_regional_sector_metrics') }}
),
gaps as (
    select
        region_code,
        region_name,
        year,
        sector_id,
        case
            when sector_id = 'childcare' then 1.0 - coalesce(coverage_ratio, 0)
            when sector_id = 'youth' then 20.0 - coalesce(coverage_ratio, 0)
            when sector_id = 'hospital' then 0.0
            else null
        end as raw_gap
    from base
)
select
    region_code,
    region_name,
    year,
    avg(case when raw_gap < 0 then 0 else raw_gap end) as coverage_gap_index,
    count(*) as contributing_sector_count
from gaps
where raw_gap is not null
group by 1, 2, 3
