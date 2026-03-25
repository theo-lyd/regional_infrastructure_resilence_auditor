{% snapshot snap_dim_sector %}

{{
    config(
        target_schema='snapshots',
        unique_key='sector_key',
        strategy='check',
        check_cols=['sector_description', 'benchmark_unit']
    )
}}

select
    sector_key,
    sector_description,
    benchmark_unit
from {{ ref('dim_sector') }}

{% endsnapshot %}
