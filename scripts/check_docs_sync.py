#!/usr/bin/env python3
"""Lightweight docs sync checks for CI."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "docs"
DOCS_INDEX = DOCS_DIR / "docs_index.md"

REQUIRED_DOCS = [
    "current_state_capabilities_and_gaps.md",
    "shell_commands_reference.md",
    "release_governance.md",
    "sla_monitoring.md",
    "system_launch_modes.md",
]


def main() -> None:
    if not DOCS_INDEX.exists():
        raise SystemExit("docs sync check failed: docs/docs_index.md is missing")

    index_text = DOCS_INDEX.read_text(encoding="utf-8")
    missing_in_index = [name for name in REQUIRED_DOCS if f"`{name}`" not in index_text]
    missing_files = [name for name in REQUIRED_DOCS if not (DOCS_DIR / name).exists()]

    if missing_files:
        raise SystemExit(
            "docs sync check failed: required docs files missing -> " + ", ".join(missing_files)
        )

    if missing_in_index:
        raise SystemExit(
            "docs sync check failed: required docs not referenced in docs_index.md -> "
            + ", ".join(missing_in_index)
        )

    print("docs sync check passed")


if __name__ == "__main__":
    main()
