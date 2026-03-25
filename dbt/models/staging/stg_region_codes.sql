with unioned as (
    select region_code_clean, region_name_clean, region_level from {{ ref('stg_childcare_22541') }}
    union all
    select region_code_clean, region_name_clean, region_level from {{ ref('stg_youth_22542') }}
    union all
    select region_code_clean, region_name_clean, region_level from {{ ref('stg_hospital_23111') }}
)
select
    region_code_clean,
    any_value(region_name_clean) as region_name_clean,
    any_value(region_level) as region_level
from unioned
group by 1
