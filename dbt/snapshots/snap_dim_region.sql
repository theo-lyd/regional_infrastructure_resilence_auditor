{% snapshot snap_dim_region %}

{{
    config(
        target_schema='snapshots',
        unique_key='region_code',
        strategy='check',
        check_cols=['region_name', 'region_level']
    )
}}

select
    region_id,
    region_code,
    region_name,
    region_level
from {{ ref('dim_region') }}

{% endsnapshot %}
