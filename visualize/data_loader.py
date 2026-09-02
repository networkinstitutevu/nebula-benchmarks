"""Discover and parse AIPerf sweep-aggregate artifacts into a tidy DataFrame.

The artifacts live at ``artifacts/{supplier}/{model}/{benchmarkType}/sweep_aggregate/``
and each directory holds ``profile_export_aiperf_sweep.json`` (preferred) or
``.csv``. Nothing about the suppliers, models or benchmark types is hard-coded:
the directory tree and the exported JSON/CSV are the single source of truth, so
adding a new model folder makes it appear automatically in the visualizer.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

_EXPORT_STEM = "profile_export_aiperf_sweep"
_SWEEP_DIR = "sweep_aggregate"


def _parse_record(root: Path, export: Path) -> dict[str, Any] | None:
    parts = export.relative_to(root).parts
    sweep_idx = None
    for i in range(len(parts) - 1, -1, -1):
        if parts[i] == _SWEEP_DIR:
            sweep_idx = i
            break
    if sweep_idx is None or sweep_idx < 3:
        return None
    return {
        "supplier": parts[sweep_idx - 3],
        "model": parts[sweep_idx - 2],
        "benchmarkType": parts[sweep_idx - 1],
        "path": export,
    }


def discover_artifacts(
    artifacts_root: str | Path = "artifacts",
) -> list[dict[str, Any]]:
    root = Path(artifacts_root)
    if not root.exists():
        return []

    json_recs: dict[tuple, dict[str, Any]] = {}
    csv_recs: dict[tuple, dict[str, Any]] = {}
    for export in sorted(root.rglob(f"{_EXPORT_STEM}.*")):
        rec = _parse_record(root, export)
        if not rec:
            continue
        key = (rec["supplier"], rec["model"], rec["benchmarkType"])
        if export.suffix == ".json":
            json_recs[key] = rec
        elif export.suffix == ".csv":
            csv_recs.setdefault(key, rec)

    merged = dict(json_recs)
    for key, rec in csv_recs.items():
        merged.setdefault(key, rec)
    return [merged[k] for k in sorted(merged)]


def _parse_json(rec: dict[str, Any], path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text())
    rows: list[dict[str, Any]] = []
    for combo in data.get("per_combination_metrics", []):
        params = combo.get("parameters", {})
        for param_name, param_value in params.items():
            for metric_name, metric in combo.get("metrics", {}).items():
                rows.append(
                    {
                        "supplier": rec["supplier"],
                        "model": rec["model"],
                        "benchmarkType": rec["benchmarkType"],
                        "sweep_param": param_name,
                        "concurrency": param_value,
                        "metric": metric_name,
                        "mean": metric.get("mean"),
                        "std": metric.get("std"),
                        "min": metric.get("min"),
                        "max": metric.get("max"),
                        "cv": metric.get("cv"),
                        "ci_low": metric.get("ci_low"),
                        "ci_high": metric.get("ci_high"),
                        "unit": metric.get("unit"),
                    }
                )
    return rows


def _parse_csv(rec: dict[str, Any], path: Path) -> list[dict[str, Any]]:
    frame = pd.read_csv(path)
    base_names = {
        c.rsplit("_mean", 1)[0]
        for c in frame.columns
        if c != "concurrency" and c.endswith("_mean")
    }
    rows: list[dict[str, Any]] = []
    for base in sorted(base_names):
        for _, row in frame.iterrows():
            rows.append(
                {
                    "supplier": rec["supplier"],
                    "model": rec["model"],
                    "benchmarkType": rec["benchmarkType"],
                    "sweep_param": "concurrency",
                    "concurrency": row.get("concurrency"),
                    "metric": base,
                    "mean": row.get(f"{base}_mean"),
                    "std": row.get(f"{base}_std"),
                    "min": row.get(f"{base}_min"),
                    "max": row.get(f"{base}_max"),
                    "cv": row.get(f"{base}_cv"),
                    "ci_low": None,
                    "ci_high": None,
                    "unit": None,
                }
            )
    return rows


def _parse_export(rec: dict[str, Any]) -> list[dict[str, Any]]:
    path = Path(rec["path"])
    if path.suffix == ".json":
        return _parse_json(rec, path)
    return _parse_csv(rec, path)


def load_sweep_data(
    artifacts_root: str | Path = "artifacts",
) -> tuple[dict[str, Any], pd.DataFrame]:
    records = discover_artifacts(artifacts_root)
    rows: list[dict[str, Any]] = []
    for rec in records:
        rows.extend(_parse_export(rec))

    if not rows:
        return _empty_index(), pd.DataFrame()

    df = pd.DataFrame(rows)
    df["concurrency"] = pd.to_numeric(df["concurrency"], errors="coerce")
    for col in ("mean", "std", "min", "max", "cv", "ci_low", "ci_high"):
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["concurrency", "mean"])

    units = df.loc[df["unit"].notna(), ["metric", "unit"]].drop_duplicates()
    metric_units = dict(zip(units["metric"], units["unit"]))
    all_metrics = sorted(df["metric"].unique())
    index = {
        "suppliers": sorted(df["supplier"].unique()),
        "models": sorted(df["model"].unique()),
        "benchmarkTypes": sorted(df["benchmarkType"].unique()),
        "concurrency": sorted(df["concurrency"].dropna().unique().tolist()),
        "metrics": all_metrics,
        "metric_units": metric_units,
        "sweep_param": df["sweep_param"].iloc[0] if len(df) else "concurrency",
    }
    return index, df


def _empty_index() -> dict[str, Any]:
    return {
        "suppliers": [],
        "models": [],
        "benchmarkTypes": [],
        "concurrency": [],
        "metrics": [],
        "metric_units": {},
        "sweep_param": "concurrency",
    }
