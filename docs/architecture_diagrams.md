# Architecture and Defense Diagrams

This document provides diagram assets for defense, thesis, and interview walkthroughs.

## 1. End-to-End Architecture

```mermaid
flowchart LR
    A[Raw CSV Sources\nchildcare youth hospital] --> B[Python Ingestion\nsrc/ingest_raw_duckdb.py]
    B --> C[DuckDB Raw Schema\nraw.*]
    C --> D[dbt Staging\nanalytics_staging.*]
    D --> E[dbt Intermediate\nanalytics_intermediate.*]
    E --> F[dbt Dimensions and Facts\nanalytics_dimensions.*\nanalytics_facts.*]
    F --> G[dbt Marts\nanalytics_marts.*]
    G --> H[Forecasting\nanalytics_predictions.*]
    H --> I[Streamlit Dashboard\npolicy_decision_dashboard.py]

    G --> J[SLA Monitoring\nsrc/monitoring/pipeline_sla_monitor.py]
    H --> J
    J --> K[Monitoring Outputs\nanalytics_monitoring.*\ndata/reports/*]

    L[Airflow DAG] --> B
    L --> G
    L --> H
    L --> J

    M[GitHub Actions CI] --> D
    M --> E
    M --> F
    M --> G
```

## 2. KPI Composition Diagram

```mermaid
flowchart TD
    A[Domain Metrics\nchildcare youth hospital] --> B[Coverage and Growth Metrics]
    B --> C[Service Maturity Index]
    B --> D[Underserved Region Score]
    B --> E[Coverage Gap Index]
    B --> F[Growth and Concentration]
    C --> G[Composite Resilience Score]
    D --> G
    E --> G
    F --> G
```

## 3. Data Lineage Diagram

```mermaid
flowchart LR
    A[data/raw/*.csv] --> B[raw.raw_22541_01_01_4\nraw.raw_22542_01_02_4\nraw.raw_23111_01_04_4]
    B --> C[stg_childcare_22541\nstg_youth_22542\nstg_hospital_23111]
    C --> D[stg_clean_childcare_22541\nstg_clean_youth_22542\nstg_clean_hospital_23111]
    D --> E[int_childcare_regional\nint_youth_regional\nint_hospital_regional]
    E --> F[int_regional_sector_metrics\nint_regional_sector_yoy]
    F --> G[fct_regional_sector_capacity]
    G --> H[mart_service_maturity_index\nmart_underserved_region_score\nmart_coverage_gap_index\nmart_resilience_score\nmart_data_quality_status]
    F --> I[pred_capacity_growth_forecast]
    H --> J[Dashboard Views]
    I --> J
```

## 4. Orchestration Sequence Diagram

```mermaid
sequenceDiagram
    participant AF as Airflow DAG
    participant IN as Ingestion Script
    participant DBT as dbt Run/Test
    participant FC as Forecast Script
    participant MON as SLA Monitor
    participant DS as Dashboard Signal

    AF->>IN: ingest_raw_data
    IN-->>AF: raw tables refreshed
    AF->>DBT: dbt_run_models
    DBT-->>AF: marts refreshed
    AF->>DBT: dbt_test_models
    DBT-->>AF: tests pass
    AF->>FC: refresh_predictive_models
    FC-->>AF: prediction tables refreshed
    AF->>DS: emit_dashboard_refresh_signal
    DS-->>AF: signal file written
    AF->>MON: pipeline_sla_checks
    MON-->>AF: SLA report + monitoring rows
```
