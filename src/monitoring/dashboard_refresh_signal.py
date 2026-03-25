#!/usr/bin/env python3
"""Emit a dashboard refresh signal file for downstream consumers."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]
SIGNAL_PATH = ROOT_DIR / "data" / "reports" / "dashboard_refresh_signal.json"


def main() -> None:
    SIGNAL_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "signal": "dashboard_refresh",
        "emitted_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": "airflow_phase10_pipeline",
    }
    SIGNAL_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Dashboard refresh signal written to: {SIGNAL_PATH}")


if __name__ == "__main__":
    main()
