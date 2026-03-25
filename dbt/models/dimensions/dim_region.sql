select
    md5(region_code_clean) as region_id,
    region_code_clean as region_code,
    region_name_clean as region_name,
    region_level
from {{ ref('stg_region_codes') }}
where region_level = 'kreis'
