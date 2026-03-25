with fact as (
    select *
    from {{ ref('fct_regional_sector_capacity') }}
),
profiled as (
    select
        year,
        count(*) as total_rows,
        sum(case when capacity_value is not null then 1 else 0 end) as capacity_non_null_rows,
        sum(case when coverage_ratio is not null then 1 else 0 end) as coverage_non_null_rows,
        sum(case when utilization_ratio is not null then 1 else 0 end) as utilization_non_null_rows,
        sum(case when concentration_ratio is not null then 1 else 0 end) as concentration_non_null_rows
    from fact
    group by 1
)
select
    year,
    total_rows,
    case when total_rows > 0 then capacity_non_null_rows::double / total_rows else null end as capacity_completeness_rate,
    case when total_rows > 0 then coverage_non_null_rows::double / total_rows else null end as coverage_completeness_rate,
    case when total_rows > 0 then utilization_non_null_rows::double / total_rows else null end as utilization_completeness_rate,
    case when total_rows > 0 then concentration_non_null_rows::double / total_rows else null end as concentration_completeness_rate,
    case
        when total_rows = 0 then 'insufficient'
        when capacity_non_null_rows::double / total_rows >= 0.95 then 'good'
        when capacity_non_null_rows::double / total_rows >= 0.85 then 'watch'
        else 'critical'
    end as data_quality_status
from profiled
