import os
from pathlib import Path

import duckdb
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Regional Resilience Executive Overview", page_icon="RR", layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        background: radial-gradient(circle at top right, #f5efe6 0%, #e4ecf3 50%, #d8e2dc 100%);
    }
    .metric-card {
        border-radius: 14px;
        padding: 14px;
        background: rgba(255, 255, 255, 0.78);
        border: 1px solid rgba(20, 40, 70, 0.15);
        box-shadow: 0 8px 20px rgba(20, 40, 70, 0.08);
    }
    .status-good {
        color: #1b6e3a;
        font-weight: 700;
    }
    .status-watch {
        color: #915600;
        font-weight: 700;
    }
    .status-critical {
        color: #a12622;
        font-weight: 700;
    }
    .status-insufficient {
        color: #4b5563;
        font-weight: 700;
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


st.title("Regional Infrastructure Resilience Auditor")
st.subheader("Phase 8 - Executive Overview (Batch D1)")

quality = run_query(
    """
    select *
    from analytics_marts.mart_data_quality_status
    order by year desc
    limit 1
    """
)

resilience = run_query(
    """
    select
        year,
        avg(resilience_score) as avg_resilience_score,
        avg(service_maturity_index) as avg_service_maturity
    from analytics_marts.mart_resilience_score
    group by 1
    order by year desc
    """
)

underserved = run_query(
    """
    select
        region_code,
        region_name,
        year,
        underserved_region_score
    from analytics_marts.mart_underserved_region_score
    order by year desc, underserved_region_score desc
    limit 10
    """
)

if resilience.empty:
    st.error("No mart data found. Run dbt build before launching this dashboard.")
    st.stop()

latest_year = int(resilience.iloc[0]["year"])
latest_resilience = float(resilience.iloc[0]["avg_resilience_score"])
latest_maturity = float(resilience.iloc[0]["avg_service_maturity"])

q_status = "insufficient"
capacity_completeness = 0.0
if not quality.empty:
    q_status = quality.iloc[0]["data_quality_status"]
    capacity_completeness = float(quality.iloc[0]["capacity_completeness_rate"])

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.metric("Latest Year", latest_year)
    st.markdown("</div>", unsafe_allow_html=True)
with c2:
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.metric("Avg Resilience Score", f"{latest_resilience:.3f}")
    st.markdown("</div>", unsafe_allow_html=True)
with c3:
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.metric("Avg Service Maturity", f"{latest_maturity:.3f}")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("### Data Quality Status")
st.markdown(
    f"Capacity completeness for {latest_year}: **{capacity_completeness:.1%}**  |  Status: "
    f"<span class='status-{q_status}'>{q_status.upper()}</span>",
    unsafe_allow_html=True,
)

st.markdown("### Resilience Trend")
st.line_chart(
    resilience.set_index("year")[["avg_resilience_score", "avg_service_maturity"]],
    use_container_width=True,
)

st.markdown("### Top 10 Underserved Regions (Latest Snapshot)")
st.dataframe(underserved, use_container_width=True, hide_index=True)

st.caption(
    "Sources: analytics_marts.mart_resilience_score, analytics_marts.mart_underserved_region_score, "
    "analytics_marts.mart_data_quality_status"
)
