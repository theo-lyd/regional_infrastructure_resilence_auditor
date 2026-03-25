from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import duckdb
from PIL import Image, ImageDraw, ImageFont

DB_PATH = "/workspaces/regional_infrastructure_resilence_auditor/data/processed/regional_resilience.duckdb"
OUT_DIR = Path("/workspaces/regional_infrastructure_resilence_auditor/reports/storytelling/screenshots")


def load_font(size: int) -> ImageFont.ImageFont:
    try:
        return ImageFont.truetype("DejaVuSans.ttf", size)
    except OSError:
        return ImageFont.load_default()


def create_panel(title: str, subtitle: str, lines: list[str], out_name: str) -> None:
    width, height = 1500, 900
    image = Image.new("RGB", (width, height), color=(240, 245, 250))
    draw = ImageDraw.Draw(image)

    title_font = load_font(44)
    subtitle_font = load_font(24)
    text_font = load_font(22)

    draw.rectangle((40, 40, width - 40, height - 40), fill=(255, 255, 255), outline=(42, 73, 102), width=3)
    draw.text((80, 80), title, fill=(25, 41, 65), font=title_font)
    draw.text((80, 150), subtitle, fill=(63, 80, 99), font=subtitle_font)

    y = 220
    for line in lines:
        draw.text((90, y), line, fill=(35, 35, 35), font=text_font)
        y += 40

    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    draw.text((90, height - 90), f"Generated: {generated}", fill=(90, 90, 90), font=subtitle_font)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    image.save(OUT_DIR / out_name)


def top_rows_to_lines(rows: list[tuple], labels: list[str], limit: int = 10) -> list[str]:
    lines = []
    lines.append(" | ".join(labels))
    lines.append("-" * 120)
    for row in rows[:limit]:
        lines.append(" | ".join(str(v) for v in row))
    return lines


def main() -> None:
    con = duckdb.connect(DB_PATH, read_only=True)

    executive = con.execute(
        """
        select year, avg_service_maturity, avg_resilience_score, data_quality_status
        from analytics_marts.mart_kpi_summary_executive
        order by year desc
        limit 6
        """
    ).fetchall()

    underserved = con.execute(
        """
        select region_name, year, underserved_region_score
        from analytics_marts.mart_underserved_region_score
        order by year desc, underserved_region_score desc
        limit 12
        """
    ).fetchall()

    predictive = con.execute(
        """
        select region_name, sector_id, forecast_year, predicted_capacity_growth, risk_band
        from analytics_predictions.pred_capacity_growth_forecast
        order by predicted_capacity_growth asc
        limit 12
        """
    ).fetchall()

    create_panel(
        title="Phase 9 Executive Overview Snapshot",
        subtitle="Service maturity, resilience, and data quality summary",
        lines=top_rows_to_lines(executive, ["year", "maturity", "resilience", "quality_status"], limit=8),
        out_name="phase9_executive_overview.png",
    )

    create_panel(
        title="Phase 9 Underserved Regions Snapshot",
        subtitle="Highest underserved scores for latest observations",
        lines=top_rows_to_lines(underserved, ["region_name", "year", "underserved_score"], limit=10),
        out_name="phase9_underserved_regions.png",
    )

    create_panel(
        title="Phase 9 Predictive Risk Snapshot",
        subtitle="Lowest predicted capacity growth and risk bands",
        lines=top_rows_to_lines(predictive, ["region_name", "sector", "forecast_year", "pred_growth", "risk"], limit=10),
        out_name="phase9_predictive_risk.png",
    )

    print("Phase 9 screenshot assets generated in reports/storytelling/screenshots")


if __name__ == "__main__":
    main()
