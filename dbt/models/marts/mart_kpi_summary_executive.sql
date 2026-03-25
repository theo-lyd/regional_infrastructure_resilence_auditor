with resilience as (
    select
        year,
        avg(resilience_score) as avg_resilience_score,
        avg(service_maturity_index) as avg_service_maturity
    from {{ ref('mart_resilience_score') }}
    group by 1
),
underserved as (
    select
        year,
        avg(underserved_region_score) as avg_underserved_score
    from {{ ref('mart_underserved_region_score') }}
    group by 1
),
coverage as (
    select
        year,
        avg(coverage_gap_index) as avg_coverage_gap
    from {{ ref('mart_coverage_gap_index') }}
    group by 1
),
quality as (
    select
        year,
        data_quality_status,
        capacity_completeness_rate
    from {{ ref('mart_data_quality_status') }}
)
select
    r.year,
    r.avg_resilience_score,
    r.avg_service_maturity,
    u.avg_underserved_score,
    c.avg_coverage_gap,
    q.capacity_completeness_rate,
    q.data_quality_status
from resilience r
left join underserved u on r.year = u.year
left join coverage c on r.year = c.year
left join quality q on r.year = q.year
