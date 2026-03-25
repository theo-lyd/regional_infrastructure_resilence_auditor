{% macro to_int_or_null(col_expr) -%}
    try_cast(nullif(trim({{ col_expr }}), '-') as integer)
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
