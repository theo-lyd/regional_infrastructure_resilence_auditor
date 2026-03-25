from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]
DEFAULT_REGISTRY_PATH = ROOT_DIR / "data" / "reference" / "ingestion_source_registry.json"


@dataclass
class SourceSpec:
    file_name: str
    source_format: str = "csv"
    encoding: str = "iso-8859-1"
    delimiter: str = ";"
    sheet_name: str | int | None = 0
    expected_min_columns: int | None = None
    expected_max_columns: int | None = None
    fail_on_schema_drift: bool = False

    @property
    def file_path(self) -> Path:
        return ROOT_DIR / "data" / "raw" / self.file_name


def _normalize_sheet_name(value: object) -> str | int | None:
    if value is None:
        return 0
    if isinstance(value, int):
        return value
    text = str(value).strip()
    if text == "":
        return 0
    if text.isdigit():
        return int(text)
    return text


def load_source_registry(registry_path: Path | None = None) -> list[SourceSpec]:
    path = registry_path or DEFAULT_REGISTRY_PATH
    if not path.exists():
        return [
            SourceSpec(file_name="22541-01-01-4.csv"),
            SourceSpec(file_name="22542-01-02-4.csv"),
            SourceSpec(file_name="23111-01-04-4.csv"),
        ]

    raw = json.loads(path.read_text(encoding="utf-8"))
    items = raw.get("sources", [])
    specs: list[SourceSpec] = []

    for item in items:
        specs.append(
            SourceSpec(
                file_name=str(item["file_name"]),
                source_format=str(item.get("format", "csv")).lower(),
                encoding=str(item.get("encoding", "iso-8859-1")),
                delimiter=str(item.get("delimiter", ";")),
                sheet_name=_normalize_sheet_name(item.get("sheet_name", 0)),
                expected_min_columns=item.get("expected_min_columns"),
                expected_max_columns=item.get("expected_max_columns"),
                fail_on_schema_drift=bool(item.get("fail_on_schema_drift", False)),
            )
        )

    return specs
