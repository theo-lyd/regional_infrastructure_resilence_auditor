with maturity as (
    select region_code, region_name, year, service_maturity_index
    from {{ ref('mart_service_maturity_index') }}
),
underserved as (
    select region_code, year, underserved_region_score
    from {{ ref('mart_underserved_region_score') }}
),
gap as (
    select region_code, year, coverage_gap_index
    from {{ ref('mart_coverage_gap_index') }}
),
growth as (
    select region_code, year, avg_capacity_yoy_growth
    from {{ ref('mart_growth_and_concentration') }}
)
select
    m.region_code,
    m.region_name,
    m.year,
    m.service_maturity_index,
    u.underserved_region_score,
    g.coverage_gap_index,
    gr.avg_capacity_yoy_growth,
    (
        0.40 * coalesce(m.service_maturity_index, 0)
        + 0.20 * (1 - coalesce(u.underserved_region_score, 0))
        + 0.20 * (1 - least(coalesce(g.coverage_gap_index, 0), 1))
        + 0.20 * least(greatest(coalesce(gr.avg_capacity_yoy_growth, 0), -1), 1)
    ) as resilience_score
from maturity m
left join underserved u
    on m.region_code = u.region_code and m.year = u.year
left join gap g
    on m.region_code = g.region_code and m.year = g.year
left join growth gr
    on m.region_code = gr.region_code and m.year = gr.year
