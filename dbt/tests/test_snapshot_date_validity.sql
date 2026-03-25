with invalid as (
    select 'stg_childcare_22541' as model_name, line_number, snapshot_date_raw
    from {{ ref('stg_childcare_22541') }}
    where try_strptime(snapshot_date_raw, '%d.%m.%Y') is null

    union all

    select 'stg_youth_22542' as model_name, line_number, snapshot_date_raw
    from {{ ref('stg_youth_22542') }}
    where try_strptime(snapshot_date_raw, '%d.%m.%Y') is null

    union all

    select 'stg_hospital_23111' as model_name, line_number, snapshot_date_raw
    from {{ ref('stg_hospital_23111') }}
    where try_strptime(snapshot_date_raw, '%d.%m.%Y') is null
)
select * from invalid
