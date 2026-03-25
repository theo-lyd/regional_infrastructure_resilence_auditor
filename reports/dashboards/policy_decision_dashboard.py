import os
from pathlib import Path

import duckdb
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Regional Resilience Policy Dashboard", page_icon="RR", layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(120deg, #f7f5ef 0%, #e8f0ea 48%, #e4edf6 100%);
    }
    .kpi-box {
        border-radius: 14px;
        border: 1px solid rgba(36, 51, 77, 0.15);
        padding: 14px;
        background: rgba(255, 255, 255, 0.84);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.06);
    }
    .policy-note {
        border-left: 5px solid #2f5d62;
        background: rgba(255, 255, 255, 0.85);
        padding: 12px;
        border-radius: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def resolve_duckdb_path() -> str:
    env_path = os.getenv("DUCKDB_PATH")
    if env_path:
        candidate = Path(env_path)
        if candidate.is_absolute():
            return str(candidate)
        repo_root = Path(__file__).resolve().parents[2]
        return str(repo_root / candidate)

    return "/workspaces/regional_infrastructure_resilence_auditor/data/processed/regional_resilience.duckdb"


@st.cache_resource
def get_connection(db_path: str) -> duckdb.DuckDBPyConnection:
    return duckdb.connect(db_path, read_only=True)


@st.cache_data(ttl=300)
def run_query(sql: str) -> pd.DataFrame:
    connection = get_connection(resolve_duckdb_path())
    return connection.execute(sql).df()


def policy_narrative(latest_exec: pd.Series, top_risk: pd.DataFrame) -> list[str]:
    notes = []
    notes.append(
        f"The latest system-wide maturity indicator is {latest_exec['avg_service_maturity']:.3f} "
        f"with resilience at {latest_exec['avg_resilience_score']:.3f}."
    )
    notes.append(
        f"Data quality status is {latest_exec['data_quality_status']}, with capacity completeness at "
        f"{latest_exec['capacity_completeness_rate']:.1%}."
    )

    if not top_risk.empty:
        regions = ", ".join(top_risk['region_name'].head(3).tolist())
        notes.append(
            f"Near-term high-risk capacity pressure is concentrated in: {regions}. "
            "These regions should be prioritized for early intervention review."
        )

    return notes


st.title("Phase 9 Dashboard and Storytelling Layer")
st.caption("Stakeholder-facing decision support across executive, domain, cross-sector, and predictive views")

executive = run_query(
    """
    select *
    from analytics_marts.mart_kpi_summary_executive
    order by year desc
    """
)

if executive.empty:
    st.error("No executive KPI summary data found. Run dbt build before launching this app.")
    st.stop()

latest = executive.iloc[0]
latest_year = int(latest["year"])

risk_ranking = run_query(
    """
    select
        region_code,
        region_name,
        sector_id,
        forecast_year,
        predicted_capacity_growth,
        risk_band
    from analytics_predictions.pred_capacity_growth_forecast
    where forecast_year = (select max(forecast_year) from analytics_predictions.pred_capacity_growth_forecast)
    order by predicted_capacity_growth asc
    """
)

cross_sector = run_query(
    """
    select
        region_name,
        max(case when sector_id = 'childcare' then capacity_value end) as childcare_capacity,
        max(case when sector_id = 'youth' then capacity_value end) as youth_capacity,
        max(case when sector_id = 'hospital' then capacity_value end) as hospital_capacity
    from analytics_intermediate.int_regional_sector_metrics
    where year = (select max(year) from analytics_intermediate.int_regional_sector_metrics)
    group by 1
    """
)

childcare = run_query(
    """
    select region_code, region_name, year, approved_places_total, facility_count_total, places_per_facility
    from analytics_intermediate.int_childcare_regional
    order by year desc, approved_places_total desc
    limit 20
    """
)

youth = run_query(
    """
    select region_code, region_name, year, youth_places_total, youth_facilities_total, places_per_facility
    from analytics_intermediate.int_youth_regional
    order by year desc, youth_places_total desc
    limit 20
    """
)

hospital = run_query(
    """
    select region_code, region_name, year, beds_total, hospitals_total, beds_per_hospital
    from analytics_intermediate.int_hospital_regional
    order by year desc, beds_total desc
    limit 20
    """
)

quality = run_query(
    """
    select *
    from analytics_marts.mart_data_quality_status
    order by year desc
    """
)

underserved = run_query(
    """
    select region_code, region_name, year, underserved_region_score
    from analytics_marts.mart_underserved_region_score
    order by year desc, underserved_region_score desc
    limit 15
    """
)

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "9.1 Executive Overview",
        "9.2 Domain Dashboards",
        "9.3 Cross-Sector Resilience",
        "9.4 Predictive View",
        "9.5 Policy Narrative",
    ]
)

with tab1:
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("<div class='kpi-box'>", unsafe_allow_html=True)
        st.metric("Latest Year", latest_year)
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='kpi-box'>", unsafe_allow_html=True)
        st.metric("Avg Service Maturity", f"{latest['avg_service_maturity']:.3f}")
        st.markdown("</div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='kpi-box'>", unsafe_allow_html=True)
        st.metric("Avg Resilience", f"{latest['avg_resilience_score']:.3f}")
        st.markdown("</div>", unsafe_allow_html=True)
    with c4:
        st.markdown("<div class='kpi-box'>", unsafe_allow_html=True)
        st.metric("Data Quality", str(latest["data_quality_status"]).upper())
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("#### Service Maturity by Year")
    st.line_chart(executive.set_index("year")[["avg_service_maturity", "avg_resilience_score"]], use_container_width=True)

    st.markdown("#### Top Underserved Regions")
    st.dataframe(underserved, use_container_width=True, hide_index=True)

    st.markdown("#### Data Quality Status")
    st.dataframe(quality, use_container_width=True, hide_index=True)

with tab2:
    st.markdown("#### Childcare View")
    st.dataframe(childcare, use_container_width=True, hide_index=True)

    st.markdown("#### Youth Welfare View")
    st.dataframe(youth, use_container_width=True, hide_index=True)

    st.markdown("#### Hospital Capacity View")
    st.dataframe(hospital, use_container_width=True, hide_index=True)

with tab3:
    st.markdown("#### Cross-Sector Matrix")
    matrix = cross_sector.copy()
    if not matrix.empty:
        matrix = matrix.set_index("region_name")
        styled = matrix.style.background_gradient(cmap="YlGnBu", axis=0)
        st.dataframe(styled, use_container_width=True)
    else:
        st.info("No cross-sector rows available.")

with tab4:
    st.markdown("#### Forecasted Pressure and Risk Ranking")
    st.dataframe(risk_ranking, use_container_width=True, hide_index=True)

    if not risk_ranking.empty:
        risk_counts = (
            risk_ranking.groupby("risk_band", as_index=False)
            .size()
            .rename(columns={"size": "region_sector_count"})
            .sort_values("region_sector_count", ascending=False)
        )
        st.bar_chart(risk_counts.set_index("risk_band")["region_sector_count"], use_container_width=True)

with tab5:
    st.markdown("#### Narrative Annotations for Policymakers")
    notes = policy_narrative(latest, risk_ranking[risk_ranking["risk_band"] == "high_risk"])
    for idx, note in enumerate(notes, start=1):
        st.markdown(
            f"<div class='policy-note'><strong>Policy Note {idx}:</strong> {note}</div>",
            unsafe_allow_html=True,
        )

    st.markdown("#### Suggested Attention List")
    attention = risk_ranking[risk_ranking["risk_band"] == "high_risk"].head(10)
    if attention.empty:
        st.info("No high-risk rows in current forecast output.")
    else:
        st.dataframe(attention, use_container_width=True, hide_index=True)

st.caption(
    "Sources: analytics_marts.mart_kpi_summary_executive, analytics_marts.mart_data_quality_status, "
    "analytics_intermediate.int_*_regional, analytics_predictions.pred_capacity_growth_forecast"
)
