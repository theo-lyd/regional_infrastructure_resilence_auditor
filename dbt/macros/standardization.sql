{% macro to_int_or_null(col_expr) -%}
    try_cast(nullif(trim({{ col_expr }}), '-') as integer)
{%- endmacro %}

{% macro normalize_missing_marker(col_expr) -%}
    case
        when {{ col_expr }} is null then null
        when lower(trim(cast({{ col_expr }} as varchar))) in (
            '-', 'k. a.', 'k.a.', 'ka', 'n/a', 'na', 'null', 'unbekannt', ''
        ) then null
        else trim(cast({{ col_expr }} as varchar))
    end
{%- endmacro %}

{% macro to_double_standardized(col_expr) -%}
    (
        case
            when {{ normalize_missing_marker(col_expr) }} is null then null
            when regexp_matches(lower({{ normalize_missing_marker(col_expr) }}), '^\\d+[\\.,]\\d+\\s*mio\\.?$') then
                try_cast(
                    replace(
                        regexp_replace(lower({{ normalize_missing_marker(col_expr) }}), '\\s*mio\\.?$', ''),
                        ',',
                        '.'
                    ) as double
                ) * 1000000
            when regexp_matches({{ normalize_missing_marker(col_expr) }}, '^\\d+[\\.,]\\d+$') then
                try_cast(replace({{ normalize_missing_marker(col_expr) }}, ',', '.') as double)
            when regexp_matches({{ normalize_missing_marker(col_expr) }}, '^\\d+\\s*-\\s*\\d+$') then
                (
                    try_cast(split_part({{ normalize_missing_marker(col_expr) }}, '-', 1) as double)
                    + try_cast(split_part({{ normalize_missing_marker(col_expr) }}, '-', 2) as double)
                ) / 2
            else try_cast({{ normalize_missing_marker(col_expr) }} as double)
        end
    )
{%- endmacro %}

{% macro to_int_standardized(col_expr) -%}
    try_cast(round({{ to_double_standardized(col_expr) }}, 0) as integer)
{%- endmacro %}

{% macro region_level_from_code(col_expr) -%}
    case
        when trim({{ col_expr }}) = 'DG' then 'national'
        when regexp_matches(trim({{ col_expr }}), '^[0-9]{2}$') then 'state'
        when regexp_matches(trim({{ col_expr }}), '^[0-9]{3}$') then 'regierungsbezirk'
        when regexp_matches(trim({{ col_expr }}), '^[0-9]{5}$') then 'kreis'
        when regexp_matches(trim({{ col_expr }}), '^[0-9]{8}$') then 'special'
        else 'unknown'
    end
{%- endmacro %}

{% macro canonical_region_name(col_expr) -%}
    case
        when {{ col_expr }} is null then null
        else regexp_replace(trim(cast({{ col_expr }} as varchar)), '\\s+', ' ')
    end
{%- endmacro %}

{% macro period_type_from_date(col_expr) -%}
    case
        when {{ col_expr }} is null then 'unknown'
        else 'snapshot'
    end
{%- endmacro %}
