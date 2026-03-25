with base as (
    select *
    from {{ ref('int_regional_sector_metrics') }}
),
sector_penalties as (
    select
        region_code,
        region_name,
        year,
        sector_id,
        case
            when sector_id = 'childcare' then greatest(0.0, 1.0 - coalesce(coverage_ratio, 0))
            when sector_id = 'youth' then greatest(0.0, 1.0 - least(coalesce(coverage_ratio, 0) / 20.0, 1.0))
            when sector_id = 'hospital' then greatest(0.0, coalesce(concentration_ratio, 0))
            else null
        end as underserved_penalty
    from base
)
select
    region_code,
    region_name,
    year,
    avg(underserved_penalty) as underserved_region_score,
    count(*) as contributing_sector_count
from sector_penalties
where underserved_penalty is not null
group by 1, 2, 3
