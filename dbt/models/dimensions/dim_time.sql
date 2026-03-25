with years as (
    select distinct snapshot_year as year from {{ ref('stg_childcare_22541') }}
    union
    select distinct snapshot_year as year from {{ ref('stg_youth_22542') }}
    union
    select distinct snapshot_year as year from {{ ref('stg_hospital_23111') }}
)
select
    year as year_key,
    year,
    cast(strptime(cast(year as varchar) || '-01-01', '%Y-%m-%d') as date) as year_start_date,
    cast(strptime(cast(year as varchar) || '-12-31', '%Y-%m-%d') as date) as year_end_date,
    true as is_snapshot_year
from years
where year is not null
