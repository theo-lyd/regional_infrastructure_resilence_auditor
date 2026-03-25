with invalid as (
    select
        'stg_childcare_22541' as model_name,
        line_number,
        snapshot_date_raw,
        snapshot_year,
        extract(year from snapshot_date) as snapshot_year_from_date
    from {{ ref('stg_childcare_22541') }}
    where snapshot_year is null
       or snapshot_date is null
       or snapshot_year != extract(year from snapshot_date)
       or snapshot_year < 1900
       or snapshot_year > 2100

    union all

    select
        'stg_youth_22542' as model_name,
        line_number,
        snapshot_date_raw,
        snapshot_year,
        extract(year from snapshot_date) as snapshot_year_from_date
    from {{ ref('stg_youth_22542') }}
    where snapshot_year is null
       or snapshot_date is null
       or snapshot_year != extract(year from snapshot_date)
       or snapshot_year < 1900
       or snapshot_year > 2100

    union all

    select
        'stg_hospital_23111' as model_name,
        line_number,
        snapshot_date_raw,
        snapshot_year,
        extract(year from snapshot_date) as snapshot_year_from_date
    from {{ ref('stg_hospital_23111') }}
    where snapshot_year is null
       or snapshot_date is null
       or snapshot_year != extract(year from snapshot_date)
       or snapshot_year < 1900
       or snapshot_year > 2100
)
select * from invalid
