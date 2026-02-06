from __future__ import annotations

from pathlib import Path
from typing import Any
import json


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        import yaml  # type: ignore
    except Exception as exc:  # pragma: no cover - dependency error
        raise RuntimeError(
            "PyYAML is required. Install with: pip install pyyaml"
        ) from exc
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"config must be a mapping: {path}")
    return data


def dump_json(data: dict[str, Any]) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False)


def get_required(cfg: dict[str, Any], path: list[str], name: str) -> Any:
    cur: Any = cfg
    for p in path:
        if not isinstance(cur, dict) or p not in cur:
            raise ValueError(f"missing required config: {name}")
        cur = cur[p]
    return cur


def set_if_provided(cfg: dict[str, Any], path: list[str], value: Any) -> None:
    if value is None:
        return
    cur = cfg
    for p in path[:-1]:
        if p not in cur or not isinstance(cur[p], dict):
            cur[p] = {}
        cur = cur[p]
    cur[path[-1]] = value


def import_ultralytics():
    try:
        from ultralytics import YOLO  # type: ignore
    except Exception as exc:  # pragma: no cover - dependency error
        raise RuntimeError(
            "ultralytics is required. Install with: pip install ultralytics"
        ) from exc
    return YOLO
