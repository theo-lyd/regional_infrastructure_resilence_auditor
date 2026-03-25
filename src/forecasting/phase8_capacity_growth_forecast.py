from __future__ import annotations

import argparse
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score


@dataclass
class ModelArtifacts:
    forecast_df: pd.DataFrame
    evaluation_df: pd.DataFrame
    coefficients_df: pd.DataFrame


def resolve_duckdb_path() -> str:
    env_path = os.getenv("DUCKDB_PATH")
    if env_path:
        p = Path(env_path)
        if p.is_absolute():
            return str(p)
        return str(Path(__file__).resolve().parents[2] / p)

    return "/workspaces/regional_infrastructure_resilence_auditor/data/processed/regional_resilience.duckdb"


def build_feature_dataset(con: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    query = """
    with base as (
        select
            m.region_code,
            m.region_name,
            m.sector_id,
            m.year,
            m.capacity_value,
            coalesce(y.capacity_yoy_growth, 0.0) as prior_year_growth,
            coalesce(m.concentration_ratio, 0.0) as service_concentration,
            avg(m.capacity_value) over (
                partition by m.region_code, m.sector_id
                order by m.year
                rows between 2 preceding and current row
            ) as moving_avg_3y,
            coalesce(g.coverage_gap_index, 0.0) as coverage_gap_index,
            coalesce(
                g.coverage_gap_index
                - lag(g.coverage_gap_index) over (partition by m.region_code order by m.year),
                0.0
            ) as regional_deficit_trend,
            lead(m.capacity_value) over (
                partition by m.region_code, m.sector_id
                order by m.year
            ) as next_capacity
        from analytics_intermediate.int_regional_sector_metrics m
        left join analytics_intermediate.int_regional_sector_yoy y
            on m.region_code = y.region_code
            and m.sector_id = y.sector_id
            and m.year = y.year
        left join analytics_marts.mart_coverage_gap_index g
            on m.region_code = g.region_code
            and m.year = g.year
    )
    select
        region_code,
        region_name,
        sector_id,
        year,
        capacity_value,
        prior_year_growth,
        moving_avg_3y,
        service_concentration,
        regional_deficit_trend,
        case
            when next_capacity is null or capacity_value = 0 then null
            else (next_capacity - capacity_value) / capacity_value
        end as target_growth_next_year
    from base
    """
    return con.execute(query).df()


def train_and_forecast(feature_df: pd.DataFrame) -> ModelArtifacts:
    feature_cols = [
        "prior_year_growth",
        "moving_avg_3y",
        "service_concentration",
        "regional_deficit_trend",
    ]

    train_df = feature_df.dropna(subset=["target_growth_next_year", *feature_cols]).copy()
    # If no next-year target exists in current history, fall back to an interpretable score model.
    if train_df.empty:
        latest_features = (
            feature_df.sort_values(["region_code", "sector_id", "year"])
            .groupby(["region_code", "sector_id"], as_index=False)
            .tail(1)
            .copy()
        )

        for col in feature_cols:
            latest_features[col] = latest_features[col].fillna(0.0)

        ma_delta_ratio = np.where(
            latest_features["moving_avg_3y"] > 0,
            (latest_features["capacity_value"] - latest_features["moving_avg_3y"])
            / latest_features["moving_avg_3y"],
            0.0,
        )

        # Transparent weighted score-based extrapolation when supervised labels are unavailable.
        latest_features["predicted_capacity_growth"] = (
            0.50 * latest_features["prior_year_growth"]
            + 0.30 * ma_delta_ratio
            - 0.15 * latest_features["regional_deficit_trend"]
            - 0.05 * latest_features["service_concentration"]
        )

        latest_features["forecast_year"] = latest_features["year"] + 1
        latest_features["predicted_capacity"] = latest_features["capacity_value"] * (
            1 + latest_features["predicted_capacity_growth"]
        )

        latest_features["risk_band"] = pd.cut(
            latest_features["predicted_capacity_growth"],
            bins=[-np.inf, -0.05, 0.02, np.inf],
            labels=["high_risk", "watch", "stable_or_growth"],
        ).astype(str)

        generated_at = datetime.now(timezone.utc).isoformat()

        forecast_df = latest_features[
            [
                "region_code",
                "region_name",
                "sector_id",
                "year",
                "forecast_year",
                "capacity_value",
                "predicted_capacity_growth",
                "predicted_capacity",
                "risk_band",
            ]
        ].copy()
        forecast_df.rename(columns={"year": "source_year", "capacity_value": "source_capacity"}, inplace=True)
        forecast_df["model_name"] = "score_based_extrapolation"
        forecast_df["trained_until_year"] = int(feature_df["year"].max())
        forecast_df["generated_at_utc"] = generated_at

        evaluation_df = pd.DataFrame(
            {
                "model_name": ["score_based_extrapolation"],
                "target_name": ["capacity_growth_forecast"],
                "trained_until_year": [int(feature_df["year"].max())],
                "holdout_year": [None],
                "trend_fit_r2": [np.nan],
                "trend_fit_mae": [np.nan],
                "directional_accuracy": [np.nan],
                "interpretability_summary": [
                    "Weighted score model from prior growth, moving average delta, deficit trend, and concentration."
                ],
                "business_usefulness_summary": [
                    "Fallback mode used due to insufficient supervised history; useful for transparent early warning only."
                ],
                "generated_at_utc": [generated_at],
            }
        )

        coefficients_df = pd.DataFrame(
            {
                "model_name": ["score_based_extrapolation"] * len(feature_cols),
                "feature_name": feature_cols,
                "coefficient_value": [0.50, 0.30, -0.05, -0.15],
                "intercept_value": [0.0] * len(feature_cols),
                "generated_at_utc": [generated_at] * len(feature_cols),
            }
        )

        return ModelArtifacts(forecast_df=forecast_df, evaluation_df=evaluation_df, coefficients_df=coefficients_df)

    trained_until_year = int(train_df["year"].max())
    holdout_year = trained_until_year

    train_split = train_df[train_df["year"] < holdout_year].copy()
    test_split = train_df[train_df["year"] == holdout_year].copy()

    # If data is too short for holdout evaluation, train on all and report NA metrics.
    if train_split.shape[0] < 10 or test_split.empty:
        train_split = train_df.copy()
        test_split = pd.DataFrame(columns=train_df.columns)

    model = LinearRegression()
    model.fit(train_split[feature_cols], train_split["target_growth_next_year"])

    if not test_split.empty:
        y_true = test_split["target_growth_next_year"].to_numpy()
        y_pred = model.predict(test_split[feature_cols])
        trend_fit_r2 = float(r2_score(y_true, y_pred))
        trend_fit_mae = float(mean_absolute_error(y_true, y_pred))
        directional_accuracy = float(np.mean(np.sign(y_true) == np.sign(y_pred)))
    else:
        trend_fit_r2 = np.nan
        trend_fit_mae = np.nan
        directional_accuracy = np.nan

    latest_features = (
        feature_df.sort_values(["region_code", "sector_id", "year"]) 
        .groupby(["region_code", "sector_id"], as_index=False)
        .tail(1)
        .copy()
    )

    for col in feature_cols:
        latest_features[col] = latest_features[col].fillna(0.0)

    latest_features["predicted_capacity_growth"] = model.predict(latest_features[feature_cols])
    latest_features["forecast_year"] = latest_features["year"] + 1
    latest_features["predicted_capacity"] = latest_features["capacity_value"] * (
        1 + latest_features["predicted_capacity_growth"]
    )

    latest_features["risk_band"] = pd.cut(
        latest_features["predicted_capacity_growth"],
        bins=[-np.inf, -0.05, 0.02, np.inf],
        labels=["high_risk", "watch", "stable_or_growth"],
    ).astype(str)

    generated_at = datetime.now(timezone.utc).isoformat()

    forecast_df = latest_features[
        [
            "region_code",
            "region_name",
            "sector_id",
            "year",
            "forecast_year",
            "capacity_value",
            "predicted_capacity_growth",
            "predicted_capacity",
            "risk_band",
        ]
    ].copy()
    forecast_df.rename(columns={"year": "source_year", "capacity_value": "source_capacity"}, inplace=True)
    forecast_df["model_name"] = "linear_regression"
    forecast_df["trained_until_year"] = trained_until_year
    forecast_df["generated_at_utc"] = generated_at

    evaluation_df = pd.DataFrame(
        {
            "model_name": ["linear_regression"],
            "target_name": ["capacity_growth_forecast"],
            "trained_until_year": [trained_until_year],
            "holdout_year": [holdout_year if not np.isnan(trend_fit_r2) else None],
            "trend_fit_r2": [trend_fit_r2],
            "trend_fit_mae": [trend_fit_mae],
            "directional_accuracy": [directional_accuracy],
            "interpretability_summary": [
                "Interpretable linear model with explicit feature coefficients for prior growth, moving average, concentration, and deficit trend."
            ],
            "business_usefulness_summary": [
                "Forecasts can flag high-risk regions when predicted growth is below -5 percent for proactive planning."
            ],
            "generated_at_utc": [generated_at],
        }
    )

    coefficients_df = pd.DataFrame(
        {
            "model_name": ["linear_regression"] * len(feature_cols),
            "feature_name": feature_cols,
            "coefficient_value": model.coef_,
            "intercept_value": [model.intercept_] * len(feature_cols),
            "generated_at_utc": [generated_at] * len(feature_cols),
        }
    )

    return ModelArtifacts(forecast_df=forecast_df, evaluation_df=evaluation_df, coefficients_df=coefficients_df)


def persist_outputs(
    con: duckdb.DuckDBPyConnection,
    artifacts: ModelArtifacts,
    csv_output_path: Path,
) -> None:
    con.execute("create schema if not exists analytics_predictions")

    con.register("forecast_df", artifacts.forecast_df)
    con.register("evaluation_df", artifacts.evaluation_df)
    con.register("coefficients_df", artifacts.coefficients_df)

    con.execute("create or replace table analytics_predictions.pred_capacity_growth_forecast as select * from forecast_df")
    con.execute("create or replace table analytics_predictions.pred_capacity_growth_evaluation as select * from evaluation_df")
    con.execute("create or replace table analytics_predictions.pred_capacity_growth_coefficients as select * from coefficients_df")

    csv_output_path.parent.mkdir(parents=True, exist_ok=True)
    artifacts.forecast_df.to_csv(csv_output_path, index=False)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Phase 8 predictive modeling: capacity growth forecast")
    parser.add_argument(
        "--duckdb-path",
        default=resolve_duckdb_path(),
        help="Path to DuckDB database file.",
    )
    parser.add_argument(
        "--csv-output",
        default="data/processed/pred_capacity_growth_forecast.csv",
        help="CSV path for forecast export.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    con = duckdb.connect(args.duckdb_path)

    feature_df = build_feature_dataset(con)
    artifacts = train_and_forecast(feature_df)
    persist_outputs(con, artifacts, Path(args.csv_output))

    print("Phase 8 forecasting completed.")
    print(f"DuckDB table: analytics_predictions.pred_capacity_growth_forecast ({len(artifacts.forecast_df)} rows)")
    print("DuckDB table: analytics_predictions.pred_capacity_growth_evaluation (1 row)")
    print(f"CSV output: {args.csv_output}")


if __name__ == "__main__":
    main()
